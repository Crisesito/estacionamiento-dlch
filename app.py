import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///estacionamientos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definición del modelo
class Estacionamiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    rut = db.Column(db.String(12), nullable=False)
    numero_estacionamiento = db.Column(db.Integer, nullable=False)
    fecha_hora_ingreso = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_hora_salida = db.Column(db.DateTime, nullable=True)

# Rutas
@app.route('/')
def index():
    ocupados = Estacionamiento.query.filter(Estacionamiento.fecha_hora_salida == None).count()
    total_espacios = 15  # Total de espacios en el estacionamiento
    libres = total_espacios - ocupados
    return render_template('index.html', ocupados=ocupados, libres=libres)

@app.route('/ingreso', methods=['POST'])
def ingreso():
    nombre = request.form['nombre']
    rut = request.form['rut']
    numero_estacionamiento = request.form['numero_estacionamiento']
    nuevo_estacionamiento = Estacionamiento(nombre=nombre, rut=rut, numero_estacionamiento=numero_estacionamiento)
    db.session.add(nuevo_estacionamiento)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/salida', methods=['POST'])
def salida():
    numero_estacionamiento = request.form['numero_estacionamiento']
    estacionamiento = Estacionamiento.query.filter_by(numero_estacionamiento=numero_estacionamiento, fecha_hora_salida=None).first()
    if estacionamiento:
        estacionamiento.fecha_hora_salida = datetime.utcnow()
        db.session.commit()
    return redirect(url_for('index'))

# Crear las tablas si no existen
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
