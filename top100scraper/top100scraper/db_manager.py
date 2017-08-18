import pymongo as pmongo
import json

class LyricDatabase:
    def connect(self):
       """Se conecta a la base de datos de mongodb"""
       try:
           self.client = pmongo.MongoClient(connect = False)
           self.lyric_db = self.client.lyrics
           self.lyric_collection = self.lyric_db.lyric_collection
       except:
           print("Error de conexion")
           raise
       else:
           self.connected = True
    def remove_dups(self):
        """Elimina elementos duplicados de la
        colleccion de letras.
        """
        aggregation = self.lyric_collection.aggregate([
            {"$group": {
                "_id": {"Cantante":"$Cantante","Titulo":"$Titulo"},
                "dups": {"$push": "$_id"},
                "count": {"$sum":1}
            }},
            {"$match":{"count": {"$gt":1}}}
        ])
        for doc in aggregation:
            print(doc)
            doc["dups"] = doc["dups"][1:]
            self.lyric_collection.delete_many({"_id":{"$in":doc["dups"]}})
    def delete_collection(self):
        """Elimina todas las canciones de la base de datos"""
        self.lyric_collection.delete_many({})
    def format_lyric(self, cantante, titulo, letra, tags = []):
        """Crea el objeto de cancion a partir de
        los parametros dados como strings
        """
        song_object = {"Cantante":cantante, "Titulo":titulo, "Letra":letra, "Tags": tags}
        return song_object
    def add_lyric(self, cantante, titulo, letra, tags = []):
        """Agrega la cancion dada a la base de datos"""
        song_object = self.format_lyric(cantante, titulo, letra, tags)
        filter_object = {k:song_object[k] for k in ["Cantante","Titulo"]}
        result = self.lyric_collection.replace_one(filter_object,song_object,upsert=True)
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
        fields = {"_id":0, "Letra":1, "Titulo":1}
        if limit > 0:
            results_cursor = self.lyric_collection.aggregate([
                {"$sample":{"size":limit}},
                {"$project": fields}
            ])
        else:
            results_cursor = self.lyric_collection.find({},fields)
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
