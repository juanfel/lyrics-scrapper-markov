import markovify
import db_manager
import re

class LyricsGenerator:
    """Clase encargada de obtener y procesar el texto de la
    base de datos y obtener las letras nuevas.
    """
    def preprocess_lyric(self,lyric):
        """Se encarga de transformar un texto especifico para modificar
        cosas como saltos de linea, entre otros
        """
        new_lyric = re.sub(r"\r",r"\n",lyric)
        return new_lyric
        
