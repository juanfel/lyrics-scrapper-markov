from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, A


class LyricSearcher(object):
    """
    Se encarga de buscar en la base de datos letras en base a distintos
    atributos.
    """

    def __init__(self):
        self.client = Elasticsearch()

    def test_search(self):
        s = Search(using=self.client)
        s = s.query("match_phrase", Tags="Progressive metal")
        resultados = s.execute()
        print(resultados.to_dict())

    def search_tag(self, tag="", size=10):
        """
        Devuelve los documentos que contienen cierto tag.
        Entrega un iterable donde cada hit tiene como campos:
        Titulo, Cantante y Tags.
        """
        s = Search(using=self.client, index="lyrics")
        if(tag != ""):
            s = s.query("match_phrase", Tags=tag)
        results = s.execute()
        if(size > 0 ):
            s = s[0:size]
        else:
            s.scan()
        return s.execute()

if __name__ == "__main__":
    lyricsearcher = LyricSearcher()
    lyricsearcher.test_search()
