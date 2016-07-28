import scrapper

def html_requests_test():
    assert scrapper.page is not None 
def html_tree_test():
    assert scrapper.tree is not None
    assert len(scrapper.artistas) > 1
