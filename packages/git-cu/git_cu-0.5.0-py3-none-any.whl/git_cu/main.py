'''
Clones a git repository into a directory structure based on the URL.
'''
import argparse
import logging
import os
import sys
from argparse import Namespace
from pathlib import PurePath
from typing import List
from urllib.parse import urlparse

from git_cu import __version__ as VERSION

logger = logging.getLogger(__name__)


class UrlParseError(Exception):
    '''Raised when parsing a URL fails'''


def parse_args(args: List) -> Namespace:
    '''Parses command line options. Returns a Namespace.'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version=VERSION)
    parser.add_argument('-d',
                        '--debug',
                        action='store_true',
                        help='print debug information')
    parser.add_argument('-n',
                        '--dry-run',
                        action='store_true',
                        help='''don't actually run git-clone''')
    parser.add_argument('url')
    parser.add_argument(
        'args',
        nargs=argparse.REMAINDER,
        help='all further arguments are passed directly to git-clone')
    return parser.parse_args(args)


def git_cu(url: str, clone_args: List, dry_run: bool) -> None:
    '''Invokes git clone for 'url' with arguments 'clone_args'.
    If 'dry_run' is True git clone is not actually executed'''
    if '..' in url:
        print('\n'.join([
            '''Sorry, but URLs containing '..' are not currently supported by git-cu.''',
            'Please create an issue at https://gitlab.com/3point2/git-cu/-/issues',
            'describing your use case if you would like to see this supported in a future version.'
        ]),
              file=sys.stderr)
        sys.exit(1)
    try:
        dest_dir = get_dest_dir(url)
    except UrlParseError as exc:
        logger.debug('parsing %s caused UrlParseError', url, exc_info=exc)
        print(f'{url}: error parsing URL', file=sys.stderr)
        print('\n'.join([
            'Please create an issue at https://gitlab.com/3point2/git-cu/-/issues with',
            'the URL you are using if you would like to see it supported in a future version.'
        ]))
        sys.exit(1)
    cu_dir = os.environ.get('GIT_CU_DIR')
    if cu_dir:
        print(f'GIT_CU_DIR is {cu_dir}', file=sys.stderr)
        dest_dir = PurePath(cu_dir) / dest_dir
    cmd = ['git', 'clone']
    cmd.extend(clone_args)
    cmd.append('--')
    cmd.append(url)
    cmd.append(str(dest_dir))
    logger.debug(cmd)
    if not dry_run:
        try:
            os.execvp(cmd[0], cmd)
        except OSError as exc:
            logger.debug('OSError executing git', exc_info=exc)
            print(f'Error executing git: {exc}', file=sys.stderr)
            sys.exit(1)


def main() -> None:
    '''Entry point. Parses command line arguments, sets up logging, and runs application.'''
    args = parse_args(sys.argv[1:])
    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.WARNING
    logging.basicConfig(
        level=log_level,
        format='%(levelname)s:%(name)s:%(funcName)s:%(message)s')
    git_cu(args.url, args.args, args.dry_run)


def assemble_path(host: str, urlpath: str) -> PurePath:
    '''Returns a PurePath to clone into given a hostname and url path'''
    path = urlpath
    if path.endswith('.git'):
        path = path[:-4]
    components = path.split('/')
    result = PurePath(host, *components)
    logger.debug('%s -> %s', urlpath, result)
    return result


def parse(url: str) -> PurePath:
    '''Returns a destination path from a URL.'''
    try:
        parsed = urlparse(url)
    except ValueError as exc:
        raise UrlParseError(f'''{url}: couldn't parse URL''') from exc
    logger.debug(parsed)
    host = ''
    if parsed.netloc:
        host = parsed.netloc.split('@')[-1]
        logger.debug('host after removing user: %s', host)
        host = host.split(':')[0]
        logger.debug('host after removing port: %s', host)
    return assemble_path(host, parsed.path)


def parse_scp(url: str) -> PurePath:
    '''Returns a destination path from an scp-style URL.'''
    host, path = url.split(':', maxsplit=1)
    logger.debug('host: %s path: %s', host, path)
    host = host.split('@')[-1]
    logger.debug('host after removing user: %s', host)
    return assemble_path(host, path)


def is_url(url: str) -> bool:
    '''Returns True if url looks like a URL, otherwise False.
    See https://www.git-scm.com/docs/git-clone#URLS for details'''
    return '://' in url


def is_scp(url: str) -> bool:
    '''Returns True if url looks like an scp-style URL, otherwise False.
    See https://www.git-scm.com/docs/git-clone#URLS for details'''
    return ':' in url and not '/' in url.split(':')[0]


def get_dest_dir(url: str) -> PurePath:
    '''Returns a destination directory based on url.'''
    if is_url(url):
        parser = parse
    elif is_scp(url):
        parser = parse_scp
    else:
        raise UrlParseError(f'''{url}: unrecognized URL''')
    return parser(url)
