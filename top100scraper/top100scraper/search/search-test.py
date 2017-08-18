import search
from nose.tools import assert_equal

def setup_module():
    global test_es
    test_es = search.LyricSearcher()
    assert test_es is not None

def search_tag_test():
    s = test_es.search_tag("metal")     
    for hit in s:
        print(hit.Cantante)