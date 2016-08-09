import markovify
import db_manager
import re

class LyricsGenerator(object):
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
        return new_lyric.lower()
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
    def feed_lyrics_to_model(self, text_class = markovify.Text, states = 2):
       """Agrega las letras al modelo de markov usando
       el tipo de modelo dado por text_class y con
       un tamano de estado dado por states
       """
       self.text_model = text_class(self.text,state_size=2)
    def get_generated_sentence(self):
       """A partir del modelo obtiene una oracion random
       """
       sentence = self.text_model.make_sentence()
       return sentence
    def markovify_songs(self, limit = 0, text_type = markovify.Text, states = 2):
       """Hace todos los pasos para obtener el modelo
       """
       self.get_lyrics_from_db(limit)
       self.join_lyrics()
       self.feed_lyrics_to_model(text_type, states)

class TitleGenerator(LyricsGenerator):
    """Genera titulos en base a lo que esta en la base de
    datos
    """
    def __init__(self):
        super(TitleGenerator,self).__init__()
    def get_lyrics_from_db(self, limit = 0):
        self.get_titles_from_db(limit)
    def get_titles_from_db(self, limit = 0):
        """Obtiene los titulos de la base de datos
        """
        lyric_iterator = self.lyric_collection.get_lyric_iterator(limit)
        for song in lyric_iterator:
            try:
                lyric = song["Titulo"] + '.'
                new_song = self.preprocess_lyric(lyric)
                self.text_data.append(new_song)
            except:
                print("Error agregando Titulo")
                raise 
    def get_generated_sentence(self):
        sentence = super(TitleGenerator, self).get_generated_sentence()
        if sentence == None:
            sentence = "Sin titulo"
        return sentence

class SongGenerator(object):
    """Se encarga de crear una cancion completa
    de acuerdo a ciertos parametros.
    """
    def __init__(self,
                 lyric_limit = 0,
                 title_limit = 0,
                 lyric_type = markovify.NewlineText,
                 title_type = markovify.NewlineText):
        self.lyric_gen = LyricsGenerator()
        self.lyric_gen.markovify_songs(limit = lyric_limit,
                                       text_type = lyric_type)

        self.title_gen = TitleGenerator()
        self.title_gen.markovify_songs(limit = title_limit,
                                       text_type = title_type)
    def generate_song(self, sentence_number = 10):
        """Crea una cancion completa.
        La devuelve por partes, esto es, un titulo y
        una lista de oraciones
        """
        title = self.title_gen.get_generated_sentence()

        sentences = []
        for i in range(0,sentence_number):
            sentences.append(self.lyric_gen.get_generated_sentence())

        return title, sentences
    def print_song(self, sentence_number = 10):
        """Crea una cancion completa y la
        imprime en pantalla
        """ 
        print("TITULO: " + self.title_gen.get_generated_sentence())
        for i in range(0,sentence_number):
            print(self.lyric_gen.get_generated_sentence())
            
if __name__ == '__main__':
    print("Creando SongGenerator")
    song_gen = SongGenerator()

    allowed_to_generate = input("\nEscriba algo para generar una cancion\nEnter para salir\n")
    while(allowed_to_generate):
        song_gen.print_song(sentence_number = 10)
        allowed_to_generate = input("\nEscriba algo para generar una cancion\nEnter para salir\n")
