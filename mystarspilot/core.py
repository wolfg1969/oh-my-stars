# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from colorama import Fore, Back, Style
from getpass import getpass, getuser
from github3 import login
from .db import StarredDB
from . import __version__
import argparse
import os
import sys
try:
    import readline
except ImportError:
    import pyreadline as readline
    
STAR_PILOT_HOME = os.path.join(os.path.expanduser("~"), ".starpilot")


def main():
    
    if not os.path.exists(STAR_PILOT_HOME):
        os.makedirs(STAR_PILOT_HOME)
    
    parser = argparse.ArgumentParser(description="a CLI tool to search your starred Github repositories.")
    parser.add_argument("keywords", nargs='*', help="search keywords")
    parser.add_argument("-l", "--language", help="filter by language", nargs='+')
    parser.add_argument("-u", "--update", action="store_true", help="create(first time) or update the local stars index")
    parser.add_argument("-r", "--reindex", action="store_true", help="re-create the local stars index")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    
    args = parser.parse_args()
    
    if args.update or args.reindex:
        
        try:
            user = raw_input('GitHub username: ')
        except KeyboardInterrupt:
            user = getuser()
        else:
            if not user:
                user = getuser()
            
        password = getpass('GitHub password for {0}: '.format(user))
        
        if not password:
            print(Fore.RED + "password is required.")
            sys.exit(1)
            
        g = login(user, password)
        
        with StarredDB(STAR_PILOT_HOME, mode='t' if args.reindex else 'w') as db:
            for repo in g.iter_starred():
                print(repo.full_name)
                db.update(repo)
                
        sys.exit(0)
       
    if not args.keywords and not args.language:
        parser.print_help()
        sys.exit(0)
    
    with StarredDB(STAR_PILOT_HOME, mode='r') as db:
        search_results = db.search(args.language, args.keywords)
    
    for repo in search_results:
        print(Fore.GREEN + repo.full_name, 
            Fore.YELLOW + "({})".format(repo.html_url), 
            Fore.BLUE + "{}".format(repo.language if repo.language else '')
        )
        if repo.description:
            print(Fore.RESET + Back.RESET + Style.RESET_ALL + repo.description)
        print()
        
    count = len(search_results)
    
    print("{}{} star{} found.".format(Fore.GREEN if count else Fore.YELLOW,
        count if count else "No", 's' if count > 1 else '' ))
        
    print(Fore.RESET + Back.RESET + Style.RESET_ALL)
        
     
if __name__ == "__main__":
    main()
