#API = APLICACIÓN PROGRAMIN INTERFACE
import discord
from discord.ext import commands
import random
import requests
import pyttsx3
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
import random
import os

UPLOAD_FOLDER = os.path.abspath("./uploads/")

def allowed_file(filename):

    return "." in filename and filename.rsplit(".", 1)[1]


app = Flask(__name__)
location = "lima, Perú"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/ProyectoFinal", methods=["GET"])
def Index():
    return render_template("casa.html", location=location)


@app.route("/set_location", methods=["POST"])
def set_location():
    global location
    location = request.form["location"]
    

    return redirect("/ProyectoFinal")

#INICIAR EL MOTOR DE VOZ
def speak(text):
    engine = pyttsx3.init() # Inicializamos el motor de vox
    engine.setProperty('rate', 150)#Le damos una velocidad
    engine.say(text)
    engine.runAndWait()

facts_list = [
    "La mayoría de las personas que sufren adicción tecnológica experimentan un fuerte estrés cuando se encuentran fuera del área de cobertura de la red o no pueden utilizar sus dispositivos",
    "Según un estudio realizado en 2018, más del 50% de las personas de entre 18 y 34 años se consideran dependientes de sus smartphones.",
    "El estudio de la dependencia tecnológica es una de las áreas más relevantes de la investigación científica moderna",
    "Según un estudio de 2019, más del 60% de las personas responden a mensajes de trabajo en sus smartphones en los 15 minutos siguientes a salir del trabajo",
    "Elon Musk afirma que las redes sociales están diseñadas para mantenernos dentro de la plataforma, para que pasemos el mayor tiempo posible viendo contenidos",
    "Elon Musk también aboga por la regulación de las redes sociales y la protección de los datos personales de los usuarios. Afirma que las redes sociales recopilan una enorme cantidad de información sobre nosotros, que luego puede utilizarse para manipular nuestros pensamientos y comportamientos",
    "Las redes sociales tienen aspectos positivos y negativos, y debemos ser conscientes de ambos cuando utilicemos estas plataformas"
    ]
#Suelta una oración aleatoria
@app.route("/random_fact")
def facts():
    return f'''<h1>{random.choice(facts_list)}</h1>
        <a href="/random_fact">Ver otro</a>
        <br>
        <h1><a href="/">home</a></h1>
        </br>
        <a href ="/sorpresa">Ruta Sorpresa</a>
        '''

#APP ROUTE para seleccionar imagen en la página y imágen de la p+agina
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if "ourfile" not in request.files:
            return "The form has no file part."
        f = request.files["ourfile"]
        if f.filename == "":
            return "No file selected!No seleciono archivo o carpeta"
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect(url_for("get_file", filename=filename))
        return "File not allowed|Archivo no permitido"
    
    return """
<form method="POST" enctype="multipart/form-data">
<input type="file" name="ourfile">
<input type="submit" value="UPLOAD">
</form>
"""
@app.route("/uploads/<filename>")
def get_file(filename):

    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
if __name__ == "__main__":
    app.run(debug=True) 
