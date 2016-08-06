import markovify
import db_manager
import re

class LyricsGenerator:
    """Clase encargada de obtener y procesar el texto de la
    base de datos y obtener las letras nuevas.
    """
    def __init__(self):
        self.text_data = []
        self.lyric_collection = db_manager.LyricDatabase()
        self.lyric_collection.connect()
    def preprocess_lyric(self, lyric):
        """Se encarga de transformar un texto especifico para modificar
        cosas como saltos de linea, entre otros
        """
        new_lyric = re.sub(r"\r",r"\n",lyric + "\n")
        return new_lyric 
    def join_lyrics(self):
       """Une todas las letras almacenadas en el objeto
       """
       self.text = ''.join(self.text_data)
    def get_lyrics_from_db(self, limit = 0):
      """Obtiene todas las letras de la base de datos
      hasta el limite dado y las agrega a los datos
      """
      lyric_iterator = self.lyric_collection.get_lyric_iterator(limit)
      for song in lyric_iterator:
          try:
              lyric = song["Letra"]
              new_song = self.preprocess_lyric(lyric)
              self.text_data.append(new_song)
          except:
              print("Error agregando letra")
              raise 
    def feed_lyrics_to_model(self):
       """Agrega las letras al modelo de markov
       """
       self.text_model = markovify.Text(self.text)
    def get_generated_sentence(self):
       """A partir del modelo obtiene una oracion random
       """
       sentence = self.text_model.make_sentence()
       return sentence
    def markovify_songs(limit = 0):
       """Hace todos los pasos para obtener el modelo
       """ 
    
