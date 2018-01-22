# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)
from builtins import *
from xml.sax.saxutils import escape
from colorama import Fore, Back, Style

import json
import re


class SearchResultView(object):

    def __init__(self, time_consumed, alfred_format=False, alfred_v3=False):
        self.time_consumed = time_consumed
        self.alfred_format = alfred_format or alfred_v3
        self.alfred_v3 = alfred_v3

    def print_search_result(self, search_result, keywords=None):
            
        if self.alfred_format:
            results = []
            count = 0
            
            for repo in search_result:
                count += 1
                if count == 1:
                    continue
                    
                full_name = repo.get('full_name')
                url = repo.get('url')
                language = repo.get('language')
                description = repo.get('description')

                if self.alfred_v3:
                    results.append({
                        "title": full_name,
                        "subtitle": '%s [%s]' % (description, 
                            language if language else ''),
                        "arg": url,
                    })

                else:  # legacy xml format for v2
                    results.append('<item uid="" arg="{}">'.format(url))
                    results.append('<title>{}</title>'.format(escape(full_name)))
                    if description:
                        results.append('<subtitle>{} {}</subtitle>'.format(
                            escape(description),
                            escape(language) if language else ''
                        ))
                    results.append('</item>')

                if count >= 10:
                    break

            if self.alfred_v3:
                alfred_output = json.dumps({
                    "items": results
                })
            else:  # legacy xml format for v2
                results.append('</items>')
                results.insert(0, '<items>')
                results.insert(0, '<?xml version="1.0" encoding="UTF-8"?>')
                alfred_output = '\n'.join(results)

            print(alfred_output)

        else:
            count = 0
            total = 0
            for repo in search_result:

                count += 1

                if count == 1:  # total number
                    total = repo
                    self.print_summary(total)
                    continue

                self._print('', end='\n')
                self.print_repo_name(repo, keywords)
                self.print_repo_url(repo)
                self.print_repo_language(repo)
                self.print_repo_description(repo, keywords)

                if (count - 1) % 10 == 0:
                    self._print('', end='\n')
                    self._print('({} to {} of {})'.format(
                        count - 10, count - 1, total), Fore.GREEN, end='\n')
                    s = input('Press <Enter> key to continue... (\'q\' to quit)')
                    if s == 'q':
                        break
            if total > 10:
                self.print_summary(total)
          
    def print_summary(self, count):
        self._print('', end='\n')
        fore_color = Fore.GREEN if count else Fore.YELLOW
        
        text = "({num} star{suffix} found in {time}s)".format(
            num=count if count else "No",
            suffix='s' if count > 1 else '',
            time='{:3.5f}'.format(self.time_consumed),
        )
            
        self._print(text, fore_color, end='\n')
        
    def print_repo_name(self, repo, keywords):
        text = self._highlight_keywords(repo.get('full_name'), keywords)
        self._print(text, Fore.GREEN)
        
    def print_repo_url(self, repo):
        self._print("[{}]".format(repo.get('url')), Fore.YELLOW)
        
    def print_repo_language(self, repo):
        lang = repo.get('language')
        if lang:
            self._print(lang, Fore.BLUE, end='\n')
            
    def print_repo_description(self, repo, keywords):
        desc = repo.get('description')
        if desc:
            text = self._highlight_keywords(desc, keywords, fore_color=Fore.WHITE)
            self._print(text, Fore.WHITE, end='\n')
        
    def _print(self, text='', fore_color=Fore.WHITE, end=' '):
        print(fore_color + text, end='')
        print(Fore.RESET + Back.RESET + Style.RESET_ALL, end=end)
        
    def _highlight_keywords(self, text, keywords, fore_color=Fore.GREEN):
        if keywords:
            for keyword in keywords:
                regex = re.compile(keyword, re.I | re.U | re.M)
                color = fore_color + Back.RED + Style.BRIGHT
                text = regex.sub(
                    color + keyword + Back.RESET + Style.NORMAL, text)
        return text
