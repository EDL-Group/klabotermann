# -*- Mode: Python; tab-width: 8; python-indent-offset: 4 -*-
# This Source Code Form is subject to the terms of the MIT License.
# If a copy of the ML was not distributed with this
# file, You can obtain one at https://opensource.org/licenses/MIT

# author: JackRed <jackred@tuta.io>

from scholarly import scholarly
from . import database


def request_publication(keywords):
    res = scholarly.search_pubs(' '.join(keywords), to_sort=1)
    return res


def compile_until_last_article(publications, last_titles, max_title=9):
    pub = next(publications)
    res = []
    while ((pub.bib['title'] not in last_titles)
           and (publications._pos < max_title)):
        res.append(pub)
        pub = next(publications)
    return res


def build_message_new_articles(new_articles):
    return '\n'.join([art.bib['title'] for art in new_articles])


def get_last_article_for_search(keywords, db):
    last_titles = database.get_title_known_articles(keywords, db)
    pubs = request_publication(keywords)
    new_articles = compile_until_last_article(pubs, last_titles)
    new_titles = [art.bib['title'] for art in new_articles]
    database.update_articles(keywords, new_titles, db)
    if len(last_titles) == 0:
        res = "Invalid request, keywords not registered"
    else:
        if len(new_articles) == 0:
            res = 'No new articles'
        else:
            res = build_message_new_articles(new_articles)
    return res