import requests
from lxml import html
from lxml import etree

try:
    page = requests.get('http://www.musica.com/letras.asp?letras=canciones')
except Exception as error:
    print("Problem connecting to page", error)
    raise
tree = html.fromstring(page.content)

xpath_all_artists = "/html/body/table[1]/tr/td/table/tr[3]/td/table/tr/td[3]/table/tr[3]/td/table/tr/td/table/tr[3]/td/table/tr[3]/td/table/tr/td[1]/p/font/a[contains(@href,'letras.asp?letras')]"
artistas = tree.xpath(xpath_all_artists)


def obtener_paginas_artistas(artistas):
    "Obtiene las paginas de los artistas a partir de la lista generada por el xpath de la pagina principal"
    page_names = []
    for artista in artistas:
        info_artista = artista.items()[0][1]
        page_names.append("http://www.musica.com/" + info_artista)
    return page_names

lyrics_page_names = obtener_paginas_artistas(artistas)

def obtener_letras_paginas_artistas(paginas_artistas):
    "Obtiene las letras de cada pagina obtenida como string"
    letras = []
    for artista in paginas_artistas:
        print("obteniendo letras de: " + artista)
        for element_letra in obtener_letras_pagina(artista):
            pagina_letra = "http://www.musica.com/" + element_letra.values()[0]
            letra = obtener_letra(pagina_letra)
            if letra is not None:
                letras.append(letra)
    return letras
def obtener_letras_pagina(pagina_artista):
    "Obtiene todas las letras de la pagina de un artista dado. La pagina es un string"
    letras = []
    content_pagina = requests.get(pagina_artista).content
    tree_pagina = html.fromstring(content_pagina)
    xpath_letras = "/html/body/table[1]/tr/td/table/tr[3]/td/table/tr/td[3]/table/tr[3]/td/table/tr/td/table/tr[4]/td/table/tr[1]/td/table/tr/td[1]/p/font/a[contains(@href,'letras.asp?letra=')]"
    letras = tree_pagina.xpath(xpath_letras)
    return letras

def obtener_letra(pagina_letra):
    "Obtiene la letra que se encuentra en una pagina"
    content_pagina = requests.get(pagina_letra).content
    tree_pagina = html.fromstring(content_pagina)
    xpath_letra = "/html/body/table[1]/tr/td/table/tr[3]/td/table/tr/td[3]/table/tr[3]/td/table/tr/td/table/tr[4]/td/table/tr[4]/td/table/tr/td[2]/p"

    try:
        letra_paragraph = tree_pagina.xpath(xpath_letra)
        letra = etree.tostring(letra_paragraph[0], encoding="unicode", method="text")
    except:
        letra = None
    return letra

lyrics = obtener_letras_paginas_artistas(lyrics_page_names)
