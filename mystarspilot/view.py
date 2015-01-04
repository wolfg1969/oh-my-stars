# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from colorama import Fore, Back, Style
import re

class SearchResultView(object):
    
    def print_search_result(self, search_result, 
                            keywords=None, alfred_format=False):
        
        if search_result is not None:
            
            if alfred_format:
                """
<?xml version="1.0"?>
<items>
    <item uid="desktop" arg="~/Desktop" valid="YES" autocomplete="Desktop" type="file">
        <title>Desktop</title>
        <subtitle>~/Desktop</subtitle>
        <icon type="fileicon">~/Desktop</icon>
    </item>
</items>
                """
                print(u"<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
                print(u"<items>")
                for repo in search_result:
                    full_name = repo.get('full_name')
                    url = repo.get('url')
                    language = repo.get('language')
                    description = repo.get('description')
                    print(u"\t<item uid=\"{}\" arg=\"{}\">".format("", url))
                    print(u"\t\t<title>{}</title>".format(full_name))
                    
                    if description:
                        print(u"<subtitle>", end='')
                        print(description.encode('utf-8'), end=' ')
                        if language:
                            print(language, end='')
                        print(u"</subtitle>")
                    # print(u"\t\t<icon type=\"fileicon\">GitHub.png</icon>")
                    print(u"\t</item>")
                print(u"</items>")
            else:
                for repo in search_result:
                    self._print('', end='\n')
                    self.print_repo_name(repo, keywords)
                    self.print_repo_url(repo)
                    self.print_repo_language(repo)
                    self.print_repo_description(repo, keywords)
            
                self.print_summary(search_result)
          
    def print_summary(self, search_result):
        self._print('', end='\n')
        count = len(search_result)
        fore_color = Fore.GREEN if count else Fore.YELLOW
        
        text = "({} star{} found)".format(
            count if count else "No", 's' if count > 1 else '')
            
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
                keyword = unicode(keyword, 'utf8')
                regex = re.compile(keyword, re.I | re.U | re.M)
                color = fore_color + Back.RED + Style.BRIGHT
                text = regex.sub(
                    color + keyword + Back.RESET + Style.NORMAL, text)
        return text
