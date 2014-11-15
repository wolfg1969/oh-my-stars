# -*- coding: utf-8 -*-
#!/bin/env python

from github3 import login
from getpass import getpass, getuser
from .db import StarredDB
import argparse
import os
import sys
try:
    import readline
except ImportError:
    pass
    
STAR_PILOT_HOME = os.path.join(os.path.expanduser("~"), ".starpilot")


def main():
    
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("action")
    parser.add_argument("-t", "--recreate", action="store_true", help="Recreate the star database")
    parser.add_argument("-l", "--language", help="Search by language", nargs='+')
    parser.add_argument("-k", "--keywords", type=lambda s: unicode(s, 'utf8'), help="Search by keywords", nargs='+')
    
    args = parser.parse_args()
    
    if not os.path.exists(STAR_PILOT_HOME):
        os.makedirs(STAR_PILOT_HOME)
    
    if args.action == "sync":
        
        try:
            user = raw_input('GitHub username: ')
        except KeyboardInterrupt:
            user = getuser()
            
        password = getpass('GitHub password for {0}: '.format(user))
        
        if not (user and password):
            print("Cowardly refusing to login without a username and password.")
            sys.exit(1)
            
        g = login(user, password)
        
        with StarredDB(STAR_PILOT_HOME, mode='t' if args.recreate else 'w') as db:
            for repo in g.iter_starred():
                print repo.full_name
                db.update(repo)
       
    elif args.action == "search":
        
        if not args.language and not args.keywords:
            parser.print_help()
            sys.exit(0)
        
        with StarredDB(STAR_PILOT_HOME, mode='t' if args.recreate else 'w') as db:
            search_results = db.search(args.language, args.keywords)
        
        for repo in search_results:
            #repo = json.loads(value)
            print repo.full_name, repo.html_url, repo.language, repo.description
            
        print "Found", len(search_results)
        
     
if __name__ == "__main__":
    main()
