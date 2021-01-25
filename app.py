from flask import Flask, render_template, url_for, redirect, request

from flask_bootstrap import Bootstrap
#Modulo para manejo del ORM SQALCHEMY
from flask_sqlalchemy import SQLAlchemy
#manejo de fechas  con python
from datetime import datetime

app = Flask(__name__) #<----Es el objeto que nos dice que es una aplicacion flask
app.debug = True
Bootstrap(app)

#configuracion para la conexion con postgres
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://postgres:aezcjrm1@localhost:5432/escolares'
app.config['SQLALCHEMY_DATABASE_URI']='postgres://ndyuqqrbeiptbk:0906566b1882c40155124c7b5a790eb8e608f44e15f8deb28bc8f9f0e8ec20b6@ec2-52-205-61-60.compute-1.amazonaws.com:5432/dev2e89se7dots'
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)


class Alumnos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30))
    apellido = db.Column(db.String(100))


lista =["Nosotros","Contacto","Preguntas frecuentes"]


@app.route('/', methods=['GET', 'POST']) 
def index():
    print("index")
    if request.method == "POST":
        print("request")
        campo_nombre = request.form['nombre']
        campo_apellido = request.form['apellido']
        alumno = Alumnos(  
                nombre=campo_nombre,
                apellido=campo_apellido)
        db.session.add(alumno)
        db.session.commit()
        mensaje = "Alumno Registrado"
        return render_template("index.html",mensaje = mensaje)     
    return render_template("index.html", variable = lista)
    #return redirect(url_for('acerca'))

@app.route('/acerca')  #<---Punto de acceso
def acerca():          #<---Nombre de la funcion
    consulta = Alumnos.query.all()
    print(consulta)
    return render_template("acerca.html", variable = consulta) #<---Nombre del archivo html

@app.route('/editar/<id>')
def editar(id):
    alumno = Alumnos.query.filter_by(id=int(id)).first()
    return render_template("editar.html", alumno = alumno)

@app.route('/actualizar', methods=['POST'])
def actualizar():
    if request.method == "POST":
        consulta = Alumnos.query.get(request.form['id'])
        consulta.nombre = request.form['nombre'] 
        consulta.apellido = request.form['apellido']
        db.session.commit()
        return redirect('/acerca')


@app.route('/eliminar/<id>')
def eliminar(id):
     alumno = Alumnos.query.filter_by(id=int(id)).delete()
     db.session.commit()
     return redirect('/acerca')    


if __name__ == "__main__":
    app.run()
