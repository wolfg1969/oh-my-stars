# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from github3.repos.repo import Repository
from tinydb import TinyDB
import os
import re
            
        
class StarredDB(object):
    
    def __init__(self, my_stars_home, mode):
        self._db = TinyDB(os.path.join(my_stars_home, "mystars.db"))
        self._idx = {
            'language': {},
            'keyword': {}
        }
        self.mode = mode
        
        
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self._db.close()
        
    def _calculate_ngrams(self, word, n):
      return [ u''.join(gram) for gram in zip(*[word[i:] for i in range(n)])]
                
    def _update_inverted_index(self, index_name, key, eid):
        
        index = self._idx.get(index_name)
        
        id_list = index.get(key, [])
        if eid not in id_list:
            id_list.append(eid)
        
        index[key] = id_list
                
    def _build_index(self):
        
        for repo in self._db.all():
            
            name = repo.get('name')
            language = repo.get('language')
            description = repo.get('description')
            
            if language:
                for lang in language.split():
                    self._update_inverted_index('language', lang.lower(), repo.eid)
                
            keywords = re.compile("[_\-]").split(name)
            if description:
                keywords += re.compile("[\s_\-]").split(description)
            for keyword in keywords:
                for n in range(2, len(keyword)+1):
                    for word in self._calculate_ngrams(keyword, n):
                        self._update_inverted_index('keyword', word.lower(), repo.eid)
            
    def update(self, repo_list):
        
        if self.mode == 't':
            self._db.purge_tables()
            
        if repo_list:
            self._db.table('latest_repo').purge()
            self._db.table('latest_repo').insert(repo_list[0])
        
        for repo in repo_list:
        
            # save repo data
            self._db.insert(repo)
        
    def get_latest_repo_full_name(self):
        latest_repo = self._db.table('latest_repo').get(eid='1')
        if latest_repo:
            return latest_repo.get('full_name')
        else:
            return ''
            
        
    def search(self, languages, keywords):
        
        self._build_index()
        
        language_results = []
        if languages:
            for search in languages:
                language_results = language_results + self._idx['language'].get(search.lower(), [])
        
        keywords_results = []
        if keywords:
            for keyword in keywords:
                for term in re.compile("[_\-]").split(keyword):
                    results = self._idx['keyword'].get(unicode(term, 'utf-8').lower(), [])
                    keywords_results.append(results)
        
        if languages and keywords:
            # python > 2.6
            search_results = list(set(
                language_results).intersection(*keywords_results))  
        else:
            if len(keywords_results) > 1:
                # python > 2.6
                final_keywords_results = list(set(
                    keywords_results[0]).intersection(*keywords_results[1:]))  
            else:
                final_keywords_results = []
                for results in keywords_results:
                    for r in results:
                        final_keywords_results.append(r)
                        
            search_results = language_results + final_keywords_results
        
        # remove duplicates then sort by id
        search_results = sorted(list(set(search_results)), key=int)  
        
        repo_results= []
        for eid in search_results:
            repo = self._db.get(eid=eid)
            if repo:
                repo_results.append(repo)
                
        return repo_results
