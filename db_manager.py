import pymongo as pmongo
import json
# client = pmongo.MongoClient()
# zips = client.zips
# zip_collection = zips.zip_collection
# zip_collection.insert_one(item)

class LyricDatabase:
    def connect(self):
       """Se conecta a la base de datos de mongodb"""
       try:
           self.client = pmongo.MongoClient()
           self.lyric_db = self.client.lyrics
           self.lyric_collection = self.lyric_db.lyric_collection
       except:
           print("Error de conexion")
           raise
       else:
           self.connected = True
    def delete_collection(self):
        """Elimina todas las canciones de la base de datos"""
        self.lyric_collection.delete_many({})
    def format_lyric(self, cantante, titulo, letra):
        """Crea el objeto de cancion a partir de
        los parametros dados como strings
        """
        song_object = {"Cantante":cantante, "Titulo":titulo, "Letra":letra}
        return song_object
    def add_lyric(self, cantante, titulo, letra):
        """Agrega la cancion dada a la base de datos"""
        song_object = self.format_lyric(cantante, titulo, letra)
        result = self.lyric_collection.insert_one(song_object)
        return result
    def get_lyric(self, cantante, titulo):
        """Obtiene el string de la letra de la cancion de
        cierto cantante con cierto titulo
        """
        song_query = {"Cantante":cantante, "Titulo":titulo}
        projection = {"_id":False, "Letra":True}
        results_cursor = self.lyric_collection.find_one(song_query, projection)
        letra = results_cursor["Letra"]
        return letra
    def get_lyric_count(self):
        """Obtiene cuantas canciones hay en la bd"""
        results_cursor = self.lyric_collection.find()
        return results_cursor.count()
