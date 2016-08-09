from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def print_song_page():
    return render_template("song.html")
