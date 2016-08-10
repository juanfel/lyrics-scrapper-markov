import requests
import re
import db_manager
from lxml import html
from lxml import etree

lyrics_database = db_manager.LyricDatabase()
lyrics_database.connect()
try:
    page = requests.get('http://www.musica.com/letras.asp?topmusica=musica')
except Exception as error:
    print("Problem connecting to page", error)
    raise
tree = html.fromstring(page.content)

xpath_all_artists = "/html/body/table[1]/tr/td/table/tr[3]/td/table/tr/td[3]/table/tr[3]/td/table/tr/td/table/tr[11]/td/table/tr/td[1]/table/tr/td[5]/a[contains(@href,'letras.asp?letras')]"
artistas = tree.xpath(xpath_all_artists)

# Se asegura que los artistas sean unicos en ID
artistas = list(set(artistas))

def obtener_paginas_artistas(artistas):
    """ Obtiene las paginas de los artistas a partir de la lista generada
    por el xpath de la pagina principal
    """
    page_names = []
    for artista in artistas:
        info_artista = artista.values()[0]
        page_names.append("http://www.musica.com/" + info_artista)
    return page_names

lyrics_page_names = obtener_paginas_artistas(artistas)

def obtener_letras_paginas_artistas(paginas_artistas):
    """Obtiene las letras de cada pagina obtenida como string"""
    id_letras = []
    for artista in paginas_artistas:
        print("obteniendo letras de: " + artista)
        paginas_letra, nombre_artista = obtener_letras_pagina(artista)
        print("Nombre del artista:" + nombre_artista)
        for element_letra in paginas_letra:
            pagina_letra = "http://www.musica.com/" + element_letra.values()[0]
            letra, titulo = obtener_letra(pagina_letra)
            print("\tTitulo:" + titulo)
            if letra is not None:
                id_letra = lyrics_database.add_lyric(nombre_artista,titulo,letra)
                id_letras.append(id_letra.upserted_id)
    return id_letras
def obtener_letras_pagina(pagina_artista):
    """ Obtiene todas las letras de la pagina de un artista dado.
    La pagina es un string
    """
    letras = []
    content_pagina = requests.get(pagina_artista).content
    tree_pagina = html.fromstring(content_pagina)

    xpath_letras = "/html/body/table[1]/tr/td/table/tr[3]/td/table/tr/td[3]/table/tr[3]/td/table/tr/td/table/tr[4]/td/table/tr[1]/td/table/tr/td[1]/p/font/a[contains(@href,'letras.asp?letra=')]"
    letras = tree_pagina.xpath(xpath_letras)

    xpath_nombre_artista = "/html/body/table[1]/tr/td/table/tr[3]/td/table/tr/td[3]/table/tr[3]/td/table/tr/td/table/tr[3]/td/table/tr/td/h2/font/b"
    artista = tree_pagina.xpath(xpath_nombre_artista)
    try:
        artista_string = etree.tostring(artista[0],
                                        encoding="unicode",
                                        method="text")
        artista_string = re.sub(r"LETRAS DE (.*)", r"\1", artista_string)
    except:
        artista_string = "No encontrado"
    return letras, artista_string

def obtener_letra(pagina_letra):
    """Obtiene la letra que se encuentra en una pagina"""
    print("\tobteniendo letra de: " + pagina_letra)
    content_pagina = requests.get(pagina_letra).content
    tree_pagina = html.fromstring(content_pagina)
    xpath_letra = "/html/body/table[1]/tr/td/table/tr[3]/td/table/tr/td[3]/table/tr[3]/td/table/tr/td/table/tr[4]/td/table/tr[4]/td/table/tr/td[2]/p"
    xpath_titulo = "/html/body/table[1]/tr/td/table/tr[3]/td/table/tr/td[3]/table/tr[3]/td/table/tr/td/table/tr[3]/td/table/tr/td/h2/font/b"
    
    try:
        letra_paragraph = tree_pagina.xpath(xpath_letra)
        letra = etree.tostring(letra_paragraph[0],
                               encoding="unicode",
                               pretty_print = True,
                               method="text")
        titulo_paragraph = tree_pagina.xpath(xpath_titulo)
        titulo = etree.tostring(titulo_paragraph[0],
                                encoding="unicode",
                                method="text")
    except:
        letra = None
        titulo = "No encontrado"
    else:
        titulo = re.sub(r'LETRA \'(.*)\'', r'\1', titulo)
    return letra, titulo

id_lyrics = obtener_letras_paginas_artistas(lyrics_page_names)
