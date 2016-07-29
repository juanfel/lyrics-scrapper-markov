import scrapper

def html_requests_test():
    assert scrapper.page is not None 
def html_tree_test():
    assert scrapper.tree is not None
    assert len(scrapper.artistas) > 1
    print(scrapper.artistas[0].items())
def get_lyric_page_name_test():
    assert len(scrapper.lyrics_page_names) > 1
    print(scrapper.lyrics_page_names[0])
def get_lyric_page_test():
    pagina = "http://www.musica.com/letras.asp?letras=3573"
    lyrics_pages = scrapper.obtener_letras_pagina(pagina)
    
    print(lyrics_pages[0].items())
    assert lyrics_pages is not None
    assert len(lyrics_pages) > 0
def get_lyrics_test():
    pagina = "http://www.musica.com/letras.asp?letra=801505"
    letra = scrapper.obtener_letra(pagina)

    print(letra)
    assert letra is not None
def all_lyrics_test():
    assert len(scrapper.lyrics) > len(scrapper.artistas)
