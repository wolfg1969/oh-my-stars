from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from colorama import Fore, Back, Style

class SearchResultView(object):
    
    def print_search_result(self, search_result, keywords=None):
        
        if search_result is not None:
            for repo in search_result:
                self.print_repo_name(repo)
                self.print_repo_url(repo)
                self.print_repo_language(repo)
                self.print_repo_description(repo)
            
            self.print_summary(search_result)
          
    def print_summary(self, search_result):
        self._print('', end='\n')
        count = len(search_result)
        fore_color = Fore.GREEN if count else Fore.YELLOW
        text = "({} star{} found)".format(count if count else "No", 's' if count > 1 else '')
        self._print(text, fore_color, end='\n')
        
    def print_repo_name(self, repo):
        self._print(repo.full_name, Fore.GREEN)
        
    def print_repo_url(self, repo):
        self._print("[{}]".format(repo.html_url), Fore.YELLOW)
        
    def print_repo_language(self, repo):
        if repo.language:
            self._print(repo.language, Fore.BLUE, end='\n')
            
    def print_repo_description(self, repo):
        if repo.description:
            self._print(repo.description, end='\n')
        
    def _print(self, text='', fore_color=Fore.RESET, end=' '):
        print(fore_color + text, end='')
        print(Fore.RESET + Back.RESET + Style.RESET_ALL, end=end)
