import top100scraper.search as search
from nose.tools import assert_equal

def setup_module():
    global test_es
    test_es = search.LyricSearcher()
    assert test_es is not None

def search_tag_test():
    s = test_es.search_tag("metal", 10)
    print(len(s.hits))
    for hit in s:
        print(hit.Cantante)
    assert len(s.hits) == 10
