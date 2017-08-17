from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

client = Elasticsearch()

s = Search(using=client)

s = s.query("match_phrase", Tags="Progressive metal")

resultados = s.execute()

print(resultados.to_dict())
