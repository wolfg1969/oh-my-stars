# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)
from builtins import *
from tinydb import TinyDB, Query, operations

import os

from .index import update_inverted_index, split_keywords, split_repo_name, split_repo_desc


class EmptyIndexWarning(RuntimeWarning):
    pass


class StarredDB(object):

    def __init__(self, my_stars_home, mode):
        self._db = TinyDB(os.path.join(my_stars_home, 'mystars.db'))

        if mode == 't':
            self._db.purge_tables()

        self._idx = self._db.table('index')

        if not self._idx.contains(Query().name == 'language'):
            self._idx.insert({
                'name': 'language',
                'docs': {}
            })
        if not self._idx.contains(Query().name == 'keyword'):
            self._idx.insert({
                'name': 'keyword',
                'docs': {}
            })

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._db.close()

    def _get_index_docs(self, name):
        return self._idx.get(Query().name == name).get('docs', {})

    def update(self, repo_list):

        if repo_list:
            self._db.table('latest_repo').purge()
            self._db.table('latest_repo').insert(repo_list[0])

        language_docs = self._get_index_docs('language')
        keyword_docs = self._get_index_docs('keyword')

        for repo in repo_list:

            # save repo data
            doc_id = self._db.insert(repo)

            # update index
            name = repo.get('name')
            language = repo.get('language')
            description = repo.get('description')

            if language:
                for lang in language.split():
                    update_inverted_index(language_docs, lang.lower(), doc_id)

            keywords = split_repo_name(name)
            if description:
                keywords += split_repo_desc(description)
            for keyword in split_keywords(keywords):
                update_inverted_index(keyword_docs, keyword.lower(), doc_id)

        self._idx.update(operations.set('docs', language_docs), Query().name == 'language')
        self._idx.update(operations.set('docs', keyword_docs), Query().name == 'keyword')

    def get_latest_repo_full_name(self):
        latest_repo = self._db.table('latest_repo').all()
        if len(latest_repo) > 0:
            return latest_repo[0].get('full_name')

    def search(self, languages, keywords):

        # self._build_index()
        language_docs = self._get_index_docs('language')
        keyword_docs = self._get_index_docs('keyword')

        if not language_docs and not language_docs:
            raise EmptyIndexWarning('empty index')

        language_results = []
        if languages:
            for search in languages:
                language_results += language_docs.get(search.lower(), [])

        keywords_results = []
        if keywords:
            for keyword in keywords:
                for term in split_repo_name(keyword):
                    results = keyword_docs.get(term.lower(), [])
                    keywords_results.append(results)

        if languages and keywords:
            # python > 2.6
            search_results = list(set(language_results).intersection(*keywords_results))
        else:
            if len(keywords_results) > 1:
                # python > 2.6
                final_keywords_results = list(set(keywords_results[0]).intersection(*keywords_results[1:]))
            else:
                final_keywords_results = []
                for results in keywords_results:
                    for r in results:
                        final_keywords_results.append(r)

            search_results = language_results + final_keywords_results

        # remove duplicates then sort by id
        search_results = sorted(list(set(search_results)), key=int)

        yield len(search_results)
        for doc_id in search_results:
            yield self._db.get(doc_id=doc_id)

