# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)
from builtins import *

from datetime import datetime

from colorama import Fore
from getpass import getpass, getuser
from netrc import netrc, NetrcParseError

from github3 import login
from .db import StarredDB, EmptyIndexWarning
from .view import SearchResultView
from . import __version__

import argparse
import os
import subprocess
import sys
import errno

try:
    import readline
except ImportError:
    import pyreadline as readline

    
MY_STARS_HOME = os.path.join(os.path.expanduser('~'), '.oh-my-stars')


def get_auth_from_netrc(hostname):
    """Try to find login auth in ``~/.netrc``. Return ``(user, pwd)`` tuple. """
    try:
        auth = netrc()
    except IOError as cause:
        if cause.errno != errno.ENOENT:
            raise
        return None, None

    username, _, password = auth.hosts.get(hostname, None) or (None,) * 3
    return username, password


def main(args=None):
    
    if not os.path.exists(MY_STARS_HOME):
        os.makedirs(MY_STARS_HOME)
    
    parser = argparse.ArgumentParser(description='a CLI tool to search your starred Github repositories.')
    parser.add_argument('keywords', nargs='*', help='Search by keywords')
    parser.add_argument('-l', '--language', help='Filter by language', nargs='+')
    parser.add_argument('-u', '--update', action='store_true',
                        help='Create(first time) or update the local stars index')
    parser.add_argument('-r', '--reindex', action='store_true', help='Re-create the local stars index')
    parser.add_argument('-a', '--alfred', action='store_true', help='Format search result as Alfred Script Filter output')
    parser.add_argument('-3', '--three', action='store_true', help='Alfred 3 support')
    parser.add_argument('-i', '--install', action='store_true', help='Import Alfred workflow')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    
    parsed_args = parser.parse_args(args)
    
    if parsed_args.update or parsed_args.reindex:

        user, password = get_auth_from_netrc('api.github.com')

        if not user:
            try:
                user = input('GitHub username: ')
            except KeyboardInterrupt:
                user = getuser()
            else:
                if not user:
                    user = getuser()

        if not password:
            password = getpass('GitHub password for {0}: '.format(user))

        if not password:
            print(Fore.RED + 'password is required.')
            sys.exit(1)

        def gh2f():
            code = ''
            while not code:
                code = input('Enter 2FA code: ')
            return code
        g = login(user, password, two_factor_callback=gh2f)
        
        mode = 't' if parsed_args.reindex else 'w'

        with StarredDB(MY_STARS_HOME, mode) as db:
            repo_list = []

            for repo in g.iter_starred(sort='created', direction='desc', number=-1):

                if db.get_latest_repo_full_name() == repo.full_name:
                    break

                print(Fore.BLUE + repo.full_name + Fore.RESET)
                repo_list.append({
                    'full_name': repo.full_name,
                    'name': repo.name,
                    'url': repo.html_url,
                    'language': repo.language,
                    'description': repo.description,
                })
            if repo_list:
                t1 = datetime.now()
                print(Fore.GREEN + 'Saving repo data...')
                db.update(repo_list)

                t2 = datetime.now()
                print(Fore.RED + 'Done. ({:3.3}s)'.format((t2 - t1).total_seconds()) + Fore.RESET)
            else:
                print(Fore.RED + 'No new stars found.' + Fore.RESET)

        sys.exit(0)

    if parsed_args.install:

        if parsed_args.three:
            filename = 'ohmystars.alfredworkflow'
        else:
            filename = 'ohmystars-v2.alfredworkflow'

        ret = subprocess.call(' '.join([
            
            'curl -s -o /tmp/{}'.format(filename),

            '-H "Accept:application/octet-stream"',

            '"{url}{filename}"'.format(
                url='https://raw.githubusercontent.com/wolfg1969/oh-my-stars/master/',
                filename=filename
            ),

            '&& open "/tmp/{}"'.format(filename)
        ]), shell=True)

        sys.exit(ret)
       
    if not parsed_args.keywords and not parsed_args.language:
        parser.print_help()
        sys.exit(0)

    with StarredDB(MY_STARS_HOME, mode='r') as db:
        try:
            t1 = datetime.now()
            search_result = db.search(parsed_args.language, parsed_args.keywords)
            t2 = datetime.now()

            view = SearchResultView(
                    (t2 - t1).total_seconds(), 
                    alfred_format=parsed_args.alfred, 
                    alfred_v3=parsed_args.three)

            view.print_search_result(search_result, parsed_args.keywords)

        except EmptyIndexWarning:
            print(Fore.RED + 'Empty index.' + Fore.RESET)

