import markovify
import db_manager
import re
import search
import nltk

class LyricsGenerator(object):
    """Clase encargada de obtener y procesar el texto de la
    base de datos y obtener las letras nuevas.
    """

    def __init__(self):
        self.text_data = []
        self.search_engine = search.LyricSearcher()

    def preprocess_lyric(self, lyric):
        """Se encarga de transformar un texto especifico para modificar
        cosas como saltos de linea, entre otros
        """
        new_lyric = re.sub(r"\r", r"\n", lyric)
        return new_lyric.lower()
        return lyric

    def join_lyrics(self):
        """Une todas las letras almacenadas en el objeto
       """
        self.text = '\n'.join(self.text_data)
        self.text_data = None

    def get_lyrics_from_db(self, limit=0, tags=""):
        """Obtiene todas las letras de la base de datos
      hasta el limite dado y las agrega a los datos
      """
        lyric_iterator = self.search_engine.search_tag(tags, limit)
        for song in lyric_iterator:
            try:
                lyric = song.Letra
                new_song = self.preprocess_lyric(lyric)
                self.text_data.append(new_song)
            except(AttributeError):
                print("Error agregando letra")
                pass
            except:
                print("Error agregando letra")
                raise

    def feed_lyrics_to_model(self, text_class=markovify.Text, states=2):
        """Agrega las letras al modelo de markov usando
       el tipo de modelo dado por text_class y con
       un tamano de estado dado por states
       """
        self.text_model = text_class(self.text, state_size=states)
        self.text = None

    def get_generated_sentence(self):
        """A partir del modelo obtiene una oracion random
       """
        sentence = self.text_model.make_sentence(
            max_overlap_ratio=100, max_overlap_total=100)
        return sentence

    def markovify_songs(self, limit=0, text_type=markovify.Text, states=2, tags=""):
        """Hace todos los pasos para obtener el modelo
       """
        self.get_lyrics_from_db(limit, tags)
        self.join_lyrics()
        self.feed_lyrics_to_model(text_type, states)


class TitleGenerator(LyricsGenerator):
    """Genera titulos en base a lo que esta en la base de
    datos
    """

    def __init__(self):
        super(TitleGenerator, self).__init__()

    def get_lyrics_from_db(self, limit=0, tags=""):
        self.get_titles_from_db(limit, tags)

    def get_titles_from_db(self, limit=0, tags=""):
        """Obtiene los titulos de la base de datos
        """
        lyric_iterator = self.search_engine.search_tag(tags, limit)
        for song in lyric_iterator:
            try:
                lyric = song.Titulo
                new_song = self.preprocess_lyric(lyric)
                self.text_data.append(new_song)
            except(AttributeError):
                print("Error agregando Titulo")
                pass
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
                 lyric_limit=0,
                 title_limit=0,
                 lyric_type=markovify.NewlineText,
                 title_type=markovify.NewlineText,
                 tags=""):
        self.lyric_gen = LyricsGenerator()
        self.lyric_gen.markovify_songs(limit=lyric_limit,
                                       text_type=lyric_type,
                                       tags=tags)

        self.title_gen = TitleGenerator()
        self.title_gen.markovify_songs(limit=title_limit,
                                       text_type=title_type,
                                       tags=tags)

    def generate_song(self, sentence_number=10):
        """Crea una cancion completa.
        La devuelve por partes, esto es, un titulo y
        una lista de oraciones
        """
        title = self.title_gen.get_generated_sentence()

        sentences = []
        for i in range(0, sentence_number):
            sentences.append(self.lyric_gen.get_generated_sentence())

        return title, sentences

    def print_song(self, sentence_number=10):
        """Crea una cancion completa y la
        imprime en pantalla
        """
        print("TITULO: " + self.title_gen.get_generated_sentence())
        for i in range(1, sentence_number):
            print(self.lyric_gen.get_generated_sentence())


class POSNewlineText(markovify.NewlineText):
    """
    Hace un generador usando Part-of-Speech. Basado en el ejemplo del
    github de markovify.
    """

    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


if __name__ == '__main__':
    print("Creando SongGenerator")
    song_gen = SongGenerator()

    allowed_to_generate = input(
        "\nEscriba algo para generar una cancion\nC-c para salir\n")
    while (allowed_to_generate):
        song_gen.print_song(sentence_number=10)
        allowed_to_generate = input(
            "\nEscriba algo para generar una cancion\nC-c para salir\n")
