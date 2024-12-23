from flask import Flask, jsonify, render_template, request, redirect, url_for, json,  flash, session
from flask_mysqldb import MySQL
from modelo.login import RegistrationForm, LoginForm
from config import MConfig
from modelo.whitelist import DomConfig
from passlib.hash import pbkdf2_sha256
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from modelo.scraper import CatalogosScraper
from flask_caching import Cache
import requests

app = Flask(__name__, template_folder = 'templates')
app.config.from_object(MConfig)

cache = Cache(app)
mysql = MySQL(app)

validacionCAPTCHA = DomConfig()

limitador = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per second"]
)

@app.route("/")
def index_get():
    return render_template("index.html")

@limitador.limit("85 per minute")
@app.route('/catalogos')
@cache.cached(timeout=420)
def catalogos_get():
    scraper = CatalogosScraper(mysql)
    products_plazavea = scraper.scrape_plazavea(scraper.plazavea_urls[0])
    products_franco = scraper.scrape_franco(scraper.franco_urls[0])

    return render_template('catalogos.html', products=products_plazavea, products2=products_franco)

@limitador.limit("85 per minute")
@app.route('/aceites')
@cache.cached(timeout=420)
def aceites_get():
    scraper = CatalogosScraper(mysql)
    products_plazavea = scraper.scrape_plazavea(scraper.plazavea_urls[1])
    products_franco = scraper.scrape_franco(scraper.franco_urls[1])

    return render_template('catalogos.html', products=products_plazavea, products2=products_franco)

@limitador.limit("85 per minute")
@app.route('/azucares')
@cache.cached(timeout=420)
def azucares_get():
    scraper = CatalogosScraper(mysql)
    products_plazavea = scraper.scrape_plazavea(scraper.plazavea_urls[2])
    products_franco = scraper.scrape_franco(scraper.franco_urls[2])

    return render_template('catalogos.html', products=products_plazavea, products2=products_franco)

@limitador.limit("85 per minute")
@app.route('/pastas')
@cache.cached(timeout=420)
def pastas_get():
    scraper = CatalogosScraper(mysql)
    products_plazavea = scraper.scrape_plazavea(scraper.plazavea_urls[3])
    products_franco = scraper.scrape_franco(scraper.franco_urls[3])

    return render_template('catalogos.html', products=products_plazavea, products2=products_franco)

@limitador.limit("85 per minute")
@app.route('/condimentos')
@cache.cached(timeout=10)
def condimentos_get():
    scraper = CatalogosScraper(mysql)
    products_plazavea = scraper.scrape_plazavea(scraper.plazavea_urls[4])
    products_franco = scraper.scrape_franco(scraper.franco_urls[4])

    return render_template('catalogos.html', products=products_plazavea, products2=products_franco)

@limitador.limit("85 per minute")
@app.route('/menestras')
@cache.cached(timeout=420)
def menestras_get():
    scraper = CatalogosScraper(mysql)
    products_plazavea = scraper.scrape_plazavea(scraper.plazavea_urls[5])
    products_franco = scraper.scrape_franco(scraper.franco_urls[5])

    return render_template('catalogos.html', products=products_plazavea, products2=products_franco)

@limitador.limit("85 per minute")
@app.route('/conservas')
@cache.cached(timeout=420)
def conservas_get():
    scraper = CatalogosScraper(mysql)
    products_plazavea = scraper.scrape_plazavea(scraper.plazavea_urls[6])
    products_franco = scraper.scrape_franco(scraper.franco_urls[6])

    return render_template('catalogos.html', products=products_plazavea, products2=products_franco)

@limitador.limit("85 per minute")
@app.route('/frutas')
@cache.cached(timeout=420)
def frutas_get():
    scraper = CatalogosScraper(mysql)
    products_plazavea = scraper.scrape_plazavea(scraper.plazavea_urls[7])
    products_franco = scraper.scrape_franco(scraper.franco_urls[7])

    return render_template('catalogos.html', products=products_plazavea, products2=products_franco)

@limitador.limit("85 per minute")
@app.route('/verduras')
@cache.cached(timeout=420)
def verduras_get():
    scraper = CatalogosScraper(mysql)
    products_plazavea = scraper.scrape_plazavea(scraper.plazavea_urls[8])
    products_franco = scraper.scrape_franco(scraper.franco_urls[8])

    return render_template('catalogos.html', products=products_plazavea, products2=products_franco)

@app.route("/sobrenosotros")
def sobrenosotros_get():
    return render_template("sobrenosotros.html")

@limitador.limit("20 per minute")
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        hashed_password = pbkdf2_sha256.hash(password)
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM vufbsdgrb WHERE pvbjdth2l = %s OR mk3u5sno0 = %s", (username, email))
        existing_user = cur.fetchone()
        if existing_user:
            flash('El usuario ya existe. Intente de nuevo.')
            return redirect(url_for('register'))
        else:
            cur.execute("INSERT INTO vufbsdgrb (pvbjdth2l, mk3u5sno0, bfdfshi1d, fi5eb74zg) VALUES (%s, %s, 2, %s)", (username, hashed_password, email))
            mysql.connection.commit()
            flash('Usuario registrado exitosamente')
            return redirect(url_for('login'))
        
    return render_template('register.html', form=form)

@limitador.limit("20 per minute")
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT mk3u5sno0, bfdfshi1d FROM vufbsdgrb WHERE pvbjdth2l = %s', (username,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            user_role = result[1] 
            if pbkdf2_sha256.verify(password, result[0]): 
                session['username'] = username
                session['role'] = user_role

                flash('Inicio de sesión exitoso')

                if user_role == 1:
                    return redirect(url_for('welcomeadmin'))
                else:
                    return redirect(url_for('welcome'))
            else:
                flash('Credenciales incorrectas. Intenta de nuevo.')
        else:
            flash('Credenciales incorrectas. Intenta de nuevo.')
            
    return render_template('login.html', form=form)

@app.route('/welcomeadmin')
def welcomeadmin():
    return f'''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bienvenido</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #231670;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            h1 {{
                color: white;
                text-align: center;
                font-size: 75px;
                font-weight: bold;
                overflow: hidden;
                padding: 50px;
                border-radius: 10px;
                opacity: 0;
                transform: translate;
                animation: appear 0.75s forwards;
            }}

            .hidden {{
                display: none; /* Oculta el contenedor inicialmente */
            }}

            @keyframes appear {{
                to {{
                    opacity: 1; /* Finaliza visible */
                    transform: translateY(0); /* Finaliza en su posición original */
                }}
            }}
        </style>
    </head>
    <body>
        <h1>Bienvenido, Admin</h1>
        <meta http-equiv="refresh" content="2;url=/">
    </body>
    </html>
    '''

@app.route('/welcome')
def welcome():
    return f'''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bienvenido</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #015701;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            h1 {{
                color: white;
                text-align: center;
                font-size: 75px;
                font-weight: bold;
                overflow: hidden;
                padding: 50px;
                border-radius: 10px;
                opacity: 0;
                transform: translate;
                animation: appear 0.75s forwards;
            }}

            .hidden {{
                display: none; /* Oculta el contenedor inicialmente */
            }}

            @keyframes appear {{
                to {{
                    opacity: 1; /* Finaliza visible */
                    transform: translateY(0); /* Finaliza en su posición original */
                }}
            }}
        </style>
    </head>
    <body>
        <h1>Bienvenido, {session["username"]}</h1>
        <meta http-equiv="refresh" content="2;url=/">
    </body>
    </html>
    '''

@app.route('/edit_profile')
def edit_profile():
    return render_template("edit_profile.html")
    
@app.route('/logout')
def logout():
    session.pop('username', None)  # Elimina el nombre de usuario de la sesión
    return f'''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sesión Cerrada</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #015701;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            h1 {{
                color: white;
                text-align: center;
                font-size: 75px;
                font-weight: bold;
                overflow: hidden;
                padding: 50px;
                border-radius: 10px;
                opacity: 0;
                transform: translate;
                animation: appear 0.75s forwards;
            }}

            .hidden {{
                display: none; /* Oculta el contenedor inicialmente */
            }}

            @keyframes appear {{
                to {{
                    opacity: 1; /* Finaliza visible */
                    transform: translateY(0); /* Finaliza en su posición original */
                }}
            }}
        </style>
    </head>
    <body>
        <h1>Vuelve pronto {session["username"]}!</h1>
        <meta http-equiv="refresh" content="2;url=/">
    </body>
    </html>
    '''    

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    #TODO: check if text is valid
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)

@app.errorhandler(429)
def ratelimit_error(e):
    return jsonify(error="ratelimit exceeded", message=str(e.description)), 429

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080, threaded=True)
