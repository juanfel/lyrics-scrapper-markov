import pymongo as pmongo
import json

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

        try:
            letra = results_cursor["Letra"]
        except:
            print("Letra no encontrada")
            return ""
        return letra
    def get_lyric_iterator(self, limit = 0):
        """Permite obtener un cursor que itere con las
        canciones
        """
        results_cursor = self.lyric_collection.find({},{"_id":0, "Letra":1, "Titulo":1})
        if limit > 0:
            results_cursor = results_cursor.limit(limit)
        return results_cursor
    def get_lyric_count(self):
        """Obtiene cuantas canciones hay en la bd"""
        results_cursor = self.lyric_collection.find()
        return results_cursor.count()
    def delete_lyric(self, cantante, titulo):
       """Elimina el primer resultado que tenga a dicho
       cantante y dicho titulo.
       """
       song_query = {"Cantante":cantante, "Titulo":titulo}
       self.lyric_collection.delete_one(song_query)