from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


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

    def search_tag(self, tag, size=10):
        """
        Devuelve los documentos que contienen cierto tag
        """    
        s = Search(using=self.client)
        s = s.query("match_phrase", Tags=tag)
        s = s[0:size]
        return s.execute()

if __name__ == "__main__":
    lyricsearcher = LyricSearcher()
    lyricsearcher.test_search()
