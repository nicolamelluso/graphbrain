#   Copyright (c) 2016 CNRS - Centre national de la recherche scientifique.
#   All rights reserved.
#
#   Written by Telmo Menezes <telmo@telmomenezes.com>
#
#   This file is part of GraphBrain.
#
#   GraphBrain is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   GraphBrain is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with GraphBrain.  If not, see <http://www.gnu.org/licenses/>.


import json
import gb.hypergraph.symbol as sym
import gb.hypergraph.edge as ed
from gb.reader.extractor import Extractor


def comments_to_text(comments):
    chunks = []
    for comment in comments:
        if comment:
            if 'body' in comment:
                chunks.append(comment['body'])
            if 'comments' in comment:
                chunks.append(comments_to_text(comment['comments']))
    return '\n'.join(chunks)


def generate_aux_text(post):
    text = None
    if 'comments' in post:
        text = '%s\n%s' % (text, comments_to_text(post['comments']))
    return text


class RedditReader(object):
    def __init__(self, hg):
        self.hg = hg
        self.extractor = Extractor(hg, stages=('alpha', 'beta', 'gamma', 'delta', 'epsilon'))
        self.main_edges = 0
        self.extra_edges = 0
        self.ignored = 0

    def process_comments(self, post, parses):
        if 'body' in post:
            parses += self.extractor.read_text(post['body'], reset_context=False)
        if 'comments' in post:
            for comment in post['comments']:
                if comment:
                    self.process_comments(comment, parses)

    def process_post(self, post):
        author = sym.build(post['author'], 'reddit_user')
        print('author: %s' % author)

        aux_text = generate_aux_text(post)

        # self.extractor.debug = True
        parses = self.extractor.read_text(post['title'], aux_text)
        # self.process_comments(post, parses)
        for p in parses:
            print('\n')
            print('sentence: %s' % p[0])
            print(ed.edge2str(p[1].main_edge))
            if len(p[1].main_edge) < 8:
                self.hg.add_belief(author, p[1].main_edge)
                self.main_edges += 1
                print('== extra ==')
                for edge in p[1].edges:
                    print(ed.edge2str(edge))
                    self.hg.add_belief('gb', edge)
                    self.extra_edges += 1
            else:
                self.ignored += 1

    def read_file(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                post = json.loads(line)
                self.process_post(post)

        print('main edges created: %s' % self.main_edges)
        print('extra edges created: %s' % self.extra_edges)
        print('ignored edges: %s' % self.ignored)


if __name__ == '__main__':
    from gb.hypergraph.hypergraph import HyperGraph
    hgr = HyperGraph({'backend': 'leveldb', 'hg': 'wikidata.hg'})
    RedditReader(hgr).read_file('reddit-wordlnews-27032017-28032017.json')
