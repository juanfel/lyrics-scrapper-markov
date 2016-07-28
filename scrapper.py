import requests
from lxml import html

page = requests.get('http://www.musica.com/letras.asp?letras=canciones')
tree = html.fromstring(page.content)

xpath_all_artists = "/html/body/table[1]/tr/td/table/tr[3]/td/table/tr/td[3]/table/tr[3]/td/table/tr/td/table/tr[3]/td/table/tr[3]/td/table/tr/td[1]/p/font/a[contains(@href,'letras.asp?letras')]"
artistas = tree.xpath(xpath_all_artists)
