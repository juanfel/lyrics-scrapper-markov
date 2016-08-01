import scrapper

def html_requests_test():
    assert scrapper.page is not None 
def html_tree_test():
    assert scrapper.tree is not None
    assert len(scrapper.artistas) > 1
    print(scrapper.artistas[0].items())
def artists_are_unique_test():
    assert len(scrapper.artistas) == len(set(scrapper.artistas))
def get_lyric_page_name_test():
    assert len(scrapper.lyrics_page_names) > 1
    print(scrapper.lyrics_page_names[0])
def get_lyric_page_test():
    pagina = "http://www.musica.com/letras.asp?letras=3573"
    lyrics_pages, artista = scrapper.obtener_letras_pagina(pagina)
    
    print(lyrics_pages[0].items(), artista)
    assert lyrics_pages is not None
    assert len(lyrics_pages) > 0
    assert artista == "CARLOS VIVES"
def get_lyrics_test():
    pagina = "http://www.musica.com/letras.asp?letra=801505"
    letra, titulo = scrapper.obtener_letra(pagina)

    print(titulo)
    print(letra)
    assert letra is not None
    assert titulo is not None
    assert titulo == "19 DE NOVIEMBRE"
def all_lyrics_test():
    test_lyric_page_names = scrapper.lyrics_page_names[1:3]
    test_lyrics = scrapper.obtener_letras_paginas_artistas(test_lyric_page_names)

    lyric_db = scrapper.lyrics_database
    assert len(test_lyrics) > len(test_lyric_page_names)
    assert lyric_db.get_lyric_count() > len(test_lyrics)

    # lyric_db.delete_collection()
