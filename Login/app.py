from flask import Flask
from flask import render_template, request, redirect, url_for, flash, jsonify
from flaskext.mysql import MySQL
from flask import send_from_directory
from datetime import datetime


import os
import pymysql
import json


app = Flask(__name__)
app.secret_key = "my_secret_key"

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'login'
mysql.init_app(app)

CARPETA = os.path.join('uploads')
app.config['CARPETA'] = CARPETA # Referencia a una variable, para almacenar la ruta 
                                # especifica(uploads)

@app.route('/uploads/<nombre_foto>')
def uploads(nombre_foto):
   return send_from_directory(app.config['CARPETA'], nombre_foto)

@app.route('/')
def index():

    sql = "SELECT * FROM `users`; "
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    users = cursor.fetchall() # Selecciona todos los registros
    conn.commit()

    return render_template('/index.html', users = users)


@app.route('/delete/<int:id>')
def delete(id):

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT foto FROM users WHERE id = %s", id)
    fila = cursor.fetchall()

    # Borra la foto de la BD y tambien de la carpeta uploads
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))

    cursor.execute("DELETE FROM users WHERE id = %s", (id))
    conn.commit()

    return redirect('/')


@app.route('/edit/<int:id>')
def edit(id):

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (id))
    users = cursor.fetchall()
    conn.commit()

    return render_template('/edit.html', users = users)


@app.route('/update', methods=['POST'])
def update():

    _User = request.form['txtUsername']
    _Pass = request.form['txtPass']
    _Correo = request.form['txtCorreo']
    _Img = request.files['txtFoto']
    id = request.form['txt_id']

    sql = '''UPDATE `users` SET `username` = %s,
                                `password` = %s,
                                `correo` = %s
                                WHERE id = %s; '''

    datos = (_User, _Pass, _Correo, id)

    conn = mysql.connect()
    cursor = conn.cursor()

    now = datetime.now()
    tiempo = now.strftime("%Y-%H-%M-%S")

    if _Img.filename != '':
        nuevoNombreImg = tiempo + "_" + _Img.filename
        _Img.save("uploads/"+nuevoNombreImg)

        cursor.execute("SELECT foto FROM users WHERE id = %s", id)
        fila = cursor.fetchall()

        # Actualiza la foto en la BD, le cambia el nombre y remueve la foto anterior
        # que se encuentra en la carpeta uploads y deja la actual
        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        cursor.execute("UPDATE users SET foto = %s WHERE id = %s", (nuevoNombreImg, id))
        conn.commit()


    cursor.execute(sql, datos)
    conn.commit()
   
    return redirect('/')

@app.route('/create')
def create():
   return render_template('/create.html')

@app.route('/store', methods=['POST'])
def storage():

    _User = request.form['txtUsername']
    _Pass = request.form['txtPass']
    _Correo = request.form['txtCorreo']

    _Img = request.files['txtFoto']

    # Validaciones
    if _User == '' or _Pass == '' or _Correo == '' or _Img.filename == '' or _Img.filename == None:
        flash('Por favor llena todos los campos! ')
        return redirect( url_for('create') )

    if _User == '' or _Pass == '' or _Correo == '' or _Img.filename == '' or _Img.filename == None:
        flash('Por favor llena todos los campos! ')
        return redirect( url_for('edit') )


    now = datetime.now()    # Se obtiene el formato del tiempo actual 
    tiempo = now.strftime("%Y-%H-%M-%S")
                        # %Year, %Horas, %Month, %Segundos

    if _Img.filename != '':
        nuevoNombreImg = tiempo + "_" + _Img.filename # Se obtiene el nombre del tiempo y se le concatena al nombre de la foto
        _Img.save("uploads/"+nuevoNombreImg) # Se guarda la imagen y se guarda en la ruta designada(uploads)

    sql = '''INSERT INTO `users` (`id`, `username`, `password`, `correo`, `foto`)
          VALUES (NULL, %s, %s, %s, %s);'''

    datos = (_User, _Pass, _Correo, nuevoNombreImg)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')

@app.route('/desarrolladores')
def desarrolladores():

   return render_template('/desarrolladores.html')


# ************       AGENDA      ****************

@app.route('/agenda')
def home():
	return render_template('agenda.html')

@app.route('/agenda')
def agenda():
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)

		cursor.execute('''SELECT id, title, url, class,
                        UNIX_TIMESTAMP(start_date)*1000 as start,
                        UNIX_TIMESTAMP(end_date)*1000 as end 
                        FROM login.event''')

		rows = cursor.fetchall()
		resp = jsonify({'success' : 1, 'result' : rows})
		resp.status_code = 200
		return resp
        
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


@app.route('/create-agenda')
def create_agenda():
   return render_template('/create-agenda.html')


@app.route('/storage-agenda', methods=['POST'])
def storage_agenda():

    _Titulo = request.form['txtTitulo']
    _Correo = request.form['txtCorreo']
    _TipoEvento = request.form['select_event']
    _FechaIni = request.form['txtFechaIni']
    _FechaTimeIni = request.form['txtFechaIniTime']
    _FechaFin = request.form['txtFechaFin']
    _FechaTimeFin = request.form['txtFechaFinTime']

    _fechaInicio = _FechaIni+" "+_FechaTimeIni
    _fechaFin = _FechaFin+" "+_FechaTimeFin


    # Validaciones
    if (_Titulo == '' or _Correo == '' or _TipoEvento == ''
        or _TipoEvento == 0 or _FechaIni == ' ' or _FechaTimeIni == ''
        or _FechaFin == '' or _FechaTimeFin == ''):

        flash('Por favor llena todos los campos! ')
        return redirect( url_for('create_agenda') )


    #Insertar Datos
    sql = '''INSERT INTO `event` (`id`, `title`, `url`, `class`, `start_date`, `end_date`)
          VALUES (NULL, %s, %s, %s, %s, %s);'''

    datos = (_Titulo, _Correo, _TipoEvento, _fechaInicio, _fechaFin)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
   
    return redirect('/agenda')



if __name__ == '__main__':
    app.run(debug=True, port=5000)