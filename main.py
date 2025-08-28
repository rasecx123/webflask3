from flask import Flask, session, render_template, flash
from config import Config
from forms import TestForm

import os

app = Flask(__name__)
app.config.from_object(Config)

#Headers de Seguridad
@app.after_request
def set_secure_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "style-src 'self' https://cdn.jsdelivr.net;"
        "script-src 'self' https://cdn.jsdelivr.net;"
    )
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

#Errores Personalizados
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

@app.route("/")
def index():
    return render_template("home.html")

@app.route('/test', methods=('GET', 'POST'))
def test():
    form = TestForm()
    if form.validate_on_submit():
       
        nombre = form.nombre.data.strip()
        apellido = form.apellido.data.strip()
        cumpleaños = form.cumpleaños.data.isoformat()

        
        DATA_DIR = os.getenv("DATA_DIR", "data")  # toma la variable de entorno o "data"
        os.makedirs(DATA_DIR, exist_ok=True)      # crea la carpeta si no existe
        ruta_archivo = os.path.join(DATA_DIR, "datos.txt")
        
        #Guardar los datos en un archivo de texto
        with open("datos.txt", "a", encoding="utf-8") as f:
            f.write(f"{nombre}, {apellido}, {cumpleaños}\n")

        return render_template("resultado.html", nombre=nombre, apellido=apellido, cumple=cumpleaños)
    else:

        if form.is_submitted():
            flash("Hubo un problema con el formulario. Verifica los datos", "warning")
    return render_template("formulario.html", form=form)

@app.route("/counter")
def counter():    
    count = session.get('count', 0) + 1
    session['count'] = count
    return f'Conteo: {count}'

if __name__ == "__main__":
    app.run(debug=False) #True cuando estemos en pruebas, False cuando estemos en produccion
    

