#!/usr/bin/env python3
"""HealthChecker: check sites health and publish results in Github or POST notify.

Requirements:
- Python 3.7+
- PyGithub 1.43+
- requests 2.21+

Description:
Use it as CLI in an infinite loop or a cron/timerd service. The JSON file with
the operation result is pretty printed in 2-space convention and is always a
list of objects containing the service URL, its status, the result of checks
over its response and an ID to represent the object (generated as the first 8
chars of md5(url) where the full URL is UTF-8 encoded).

"""

# -----------------------------------------------------------------------------
# Copyright (C) 2019 HacKan (https://hackan.net)
#
# This file is part of HealthChecker.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------

import asyncio
import json
import os
import sys
import typing
from argparse import ArgumentParser

# noinspection PyPackageRequirements
import github  # PyGithub

from . import __version__
from . import settings
from .core import healthcheck_urls
from .core import notify
from .objects import ServiceStatusList
from .utils import logger
from .utils import parse_url

__header__ = (
    f'HealthChecker v{__version__}\nby HacKan (https://hackan.net) '
    f'FOSS under GNU GPL v3.0 or newer'
)

EXIT_SUCCESS: int = 0
EXIT_FAILURE: int = 1


def _get_github_handler(github_api_token: str) -> github.Github:
    """Get github api handler."""
    if github_api_token.find(',') != -1:
        client_id, client_secret = github_api_token.split(',')
        return github.Github(client_id=client_id, client_secret=client_secret)

    return github.Github(login_or_token=github_api_token)


def _to_github(
    repo_name: str,
    github_api_token: str,
    filename: str,
    statuses: ServiceStatusList,
    branch: str = settings.GITHUB_BRANCH,
    author_email: str = settings.GITHUB_COMMITTER_EMAIL,
) -> bool:
    """Store results in a file in a Github repo.

    :return True if execution was successful, False otherwise.
    """
    if not github_api_token:
        logger.error(
            'Repository %s indicated to store results but Github '
            'API Token is missing',
            repo_name,
        )
        return False

    if not filename:
        logger.error(
            'Repository %s indicated to store results but '
            'filename is missing',
            repo_name,
        )
        return False

    logger.info('Getting repository information...')
    gh = _get_github_handler(github_api_token)

    try:
        repo = gh.get_repo(repo_name)
    except github.UnknownObjectException:
        logger.error('Repository %s not found', repo_name)
        return False

    except github.BadCredentialsException:
        logger.error('Bad credentials for repository %s', repo_name)
        return False

    author = github.InputGitAuthor(name='HealthChecker', email=author_email)
    content = statuses.as_json(pretty=True) + '\n'
    try:
        file = repo.get_contents(filename)
    except github.UnknownObjectException:
        # Create file
        action = 'created'
        details = repo.create_file(
            path=filename,
            message=f'[HealthChecker] Create {filename}',
            content=content,
            branch=branch,
            committer=author,
        )
        info = details['commit'].sha
    else:
        if isinstance(file, list):
            raise ValueError('can not handle a list of files from github')

        # Update file if it changed
        if file.decoded_content.decode('utf-8') == content:
            action = 'kept unchanged'
            info = 'no changes detected'
        else:
            action = 'updated'
            details = repo.update_file(
                path=file.path,
                message=f'[HealthChecker] Update {filename}',
                content=content,
                sha=file.sha,
                branch=branch,
                committer=author,
            )
            info = details['commit'].sha

    logger.info('File %s %s: %s', filename, action, info)

    return True


def _parse_notify_headers(
    *,
    headers: typing.Optional[typing.Dict[str, str]],
    use_json: bool,
) -> typing.Dict[str, str]:
    """Parse headers used for the notify function."""
    if headers:
        notify_headers = headers.copy()
        if use_json:
            notify_headers['content-type'] = 'application/json'
    elif use_json:
        notify_headers = {
            'content-type': 'application/json',
        }
    else:
        notify_headers = {}

    return notify_headers


def _notify(
    url: str,
    statuses: ServiceStatusList,
    payload: typing.Optional[str] = None,
    headers: typing.Optional[typing.Dict[str, str]] = None,
    use_json: bool = False,
) -> bool:
    """Send a notification with given statues."""
    notify_headers = _parse_notify_headers(headers=headers, use_json=use_json)

    if use_json:
        failed_urls = json.dumps([status.url for status in statuses if not status])
    else:
        failed_urls = ','.join([status.url for status in statuses if not status])

    if payload and 'HEALTHCHECKER_FAILED_URLS' in payload:
        notify_payload = payload.replace('HEALTHCHECKER_FAILED_URLS', failed_urls)
    elif payload:
        notify_payload = payload + failed_urls
    else:
        notify_payload = failed_urls

    logger.debug(
        'Notifying %s with headers: %s and payload: %s',
        url,
        notify_headers,
        notify_payload,
    )
    if notify(url, notify_payload, notify_headers, log=True):
        logger.info('Notified %s successfully', url)
        return True

    logger.error('Could not notify %s', url)
    return False


def _to_file(filename: str, statuses: ServiceStatusList) -> bool:
    """Store results in a file (or standard output).

    :return True if execution was successful, False otherwise.
    """
    results = statuses.as_json(pretty=True)
    if filename == '-':
        print(results)
    else:
        filename_ = os.path.abspath(filename)
        if os.path.exists(filename_) and not os.path.isfile(filename_):
            logger.error('File "%s" is not a file!', filename_)
            return False

        with open(filename_, 'wt') as file:
            file.write(results)
        logger.info('Result stored as "%s"', filename_)

    return True


def _get_arguments_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog='healthchecker',
        description=f'{__header__}. '
        'Checks URLs through HTTP GET requests to verify '
        'their availability. Optionally writes the status result '
        'to a file in Github. Using Github requires the repository '
        'name, the filename and an API token. Besides the ones '
        'listed below, the following env vars exist: '
        'HEALTHCHECKER_LOG_LEVEL sets the minimal logging level '
        'and defaults to info (can be: debug, info, warning, error, '
        'critical); HEALTHCHECKER_REQUESTS_TIMEOUT sets the amount '
        'of time in seconds to wait for services to respond and '
        'defaults to 10 seconds (setting a very low value might '
        'cause several false positives). Note: command-line '
        'parameters will always supersede env vars.',
    )
    github_group = parser.add_argument_group('github options')
    github_group.add_argument(
        '--gh-repo',
        type=str,
        default=settings.GITHUB_REPO,
        help='(HEALTHCHECKER_GITHUB_REPO) repository in the form of '
        '<user|org>/<repo> (case insensitive), i.e.: HacKanCuBa/b2rsum',
    )
    github_group.add_argument(
        '--gh-filename',
        type=str,
        default=settings.GITHUB_FILENAME,
        help='(HEALTHCHECKER_GITHUB_FILENAME) filename to modify (include '
        'path if it is in a subdir such as path/to/file.ext)',
    )
    github_group.add_argument(
        '--gh-branch',
        type=str,
        default=settings.GITHUB_BRANCH,
        help='(HEALTHCHECKER_GITHUB_BRANCH) branch where commits are done '
        '(defaults to main)',
    )
    github_group.add_argument(
        '--gh-token',
        type=str,
        default=settings.GITHUB_API_TOKEN,
        help='(HEALTHCHECKER_GITHUB_API_TOKEN) API token or '
        'client_id,client_secret (bypasses the one supplied through the '
        'environment)',
    )
    github_group.add_argument(
        '--gh-email',
        type=str,
        default=settings.GITHUB_COMMITTER_EMAIL,
        help='(HEALTHCHECKER_GITHUB_COMMITTER_EMAIL) git committer email '
        '(the committer name is hardcoded to HealthChecker)',
    )
    notify_group = parser.add_argument_group('notify options')
    notify_group.add_argument(
        '--notify-url',
        type=str,
        default=settings.NOTIFY_URL,
        help='(HEALTHCHECKER_NOTIFY_URL) URL to POST the status notification',
    )
    notify_group.add_argument(
        '--notify-payload',
        type=str,
        default=settings.NOTIFY_PAYLOAD,
        help='(HEALTHCHECKER_NOTIFY_PAYLOAD) payload to send to the notify URL: '
        'it is prepended to the comma-separated list of URLs that failed '
        'validation, unless that it contains the string '
        'HEALTHCHECKER_FAILED_URLS (case sensitive), where it will '
        'replace that string by the comma-separated list of URLs, and '
        'send the entire payload',
    )
    notify_group.add_argument(
        '--notify-header',
        type=str,
        action='append',
        help='(HEALTHCHECKER_NOTIFY_HEADERS (comma-separated)) header to send '
        'to the notify URL, which must be specified as name and value '
        'separated by a semicolon: <header name>:<header value> (this '
        'parameter can be repeated as needed)',
    )
    notify_group.add_argument(
        '--notify-json',
        action='store_true',
        help='(HEALTHCHECKER_NOTIFY_JSON (true/false)) send the payload JSON '
        'encoded (it also adds the proper Content-Type header)',
    )
    parser.add_argument(
        '--version',
        action='store_true',
        help='show version and exit',
    )
    parser.add_argument(
        '--validation',
        type=str,
        action='append',
        help='(HEALTHCHECKER_URLS_VALIDATION (comma-separated)) string to find '
        'in the body of a request to an URL as a validation, one per URL '
        '(or the last one is used for the remaining URLs) (this parameter '
        'can be repeated as needed)',
    )
    parser.add_argument(
        '--output',
        '-o',
        type=str,
        help='(HEALTHCHECKER_OUTPUT) store result in a file, overwriting if exists '
        '(use `-` for standard output)',
    )
    parser.add_argument(
        'url',
        type=str,
        nargs='*',
        help='(HEALTHCHECKER_URLS (comma-separated)) URL to check',
    )
    return parser


async def main() -> int:
    """CLI function for HealthChecker."""
    parser = _get_arguments_parser()
    args = parser.parse_args()

    if args.version:
        print(__header__)
        return EXIT_SUCCESS

    urls = [parse_url(url) for url in args.url or settings.URLS if url.strip()]
    if not urls:
        parser.print_usage()
        return EXIT_FAILURE

    validations = [
        validation for validation in args.validation or settings.URLS_VALIDATION
        if validation.strip()
    ]
    repo_name: str = args.gh_repo
    filename: str = args.gh_filename
    branch: str = args.gh_branch
    author_email: str = args.gh_email
    github_api_token: str = args.gh_token
    notify_url: typing.Optional[str] = (
        parse_url(args.notify_url) if args.notify_url else None
    )
    notify_payload: typing.Optional[str] = args.notify_payload
    notify_json: bool = args.notify_json or settings.NOTIFY_JSON
    output_file: typing.Optional[str] = args.output or settings.OUTPUT
    try:
        notify_headers = {
            header.split(':')[0].strip().lower(): header.split(':')[1].strip()
            for header in args.notify_header or settings.NOTIFY_HEADERS
            if header.strip()
        }
    except IndexError:
        logger.error('At least one header is invalid, skipping...')
        notify_headers = {}

    try:
        timeout = float(settings.REQUESTS_TIMEOUT)
    except ValueError:
        logger.error(
            'HEALTHCHECKER_REQUESTS_TIMEOUT must be a valid float, '
            'default to 10 seconds',
        )
        timeout = 10

    # Check URLs
    statuses = await healthcheck_urls(urls, validations, timeout=timeout, log=True)

    # Save results in Github
    if repo_name:
        _to_github(repo_name, github_api_token, filename, statuses, branch, author_email)

    # Notify negative results
    if notify_url and not statuses:
        _notify(notify_url, statuses, notify_payload, notify_headers, notify_json)

    # Store results in a file
    if output_file:
        _to_file(output_file, statuses)

    return EXIT_SUCCESS


def run() -> int:
    """Console entry point."""
    return asyncio.run(main())


if __name__ == '__main__':
    sys.exit(run())
