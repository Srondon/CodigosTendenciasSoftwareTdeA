from distutils.command.config import config
from flask import Flask, redirect, render_template, request, url_for, flash
from config import config
from flask_mysqldb import MySQL

#Models
from models.ModelUser import ModelUser

# Entites
from models.entites.User import User

app=Flask(__name__)
# -Para manejo de conexión
conexion = MySQL(app) 

@app.route('/')
def index():
    return redirect (url_for ('login') )

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        print(request.form['username'])
        print(request.form['password'])
        user= User(0, request.form['username'], request.form['password'])
        logged_user=ModelUser.login(conexion, user)
        if logged_user != None:
            if logged_user.password:
                return redirect(url_for('home'))
            else:
                flash ("contraseña invalida...")
                return render_template('auth/login.html')  
        else:
            flash ("No se encuentra usuario...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


#----------- Métodos de los Cursos -----------

#-- Método para mostrar todos los curso de la Base de Datos
@app.route('/cursos', methods=['GET'])
def listarCursos():
    try:
        cursor = conexion.connection.cursor() #SIEMPRE lo usamos para interactuar con la BDD
        sql = "SELECT codigo, nombre, creditos FROM cursos ORDER BY nombre ASC"
        cursor.execute(sql)
        datos = cursor.fetchall() #Fetchall convierte la respuesta en algo entendible para Python        
        cursos =[]
        for fila in datos:
            curso = {'codigo': fila[0], 'nombre': fila[1], 'creditos': fila[2]}
            cursos.append(curso)
        return jsonify({'cursos': cursos, 'mensaje': "Cursos registrado en la Base de Datos."})
    except Exception as ex:
        return jsonify({'mensaje': "Error al listar el curso."})

#-- Método para buscar un curso específico
@app.route('/cursos/<codigo>', methods=['GET'])
def buscarCurso(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT codigo, nombre, creditos FROM cursos WHERE codigo = '{0}'".format(codigo) #Concatenacion simple con Format
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            curso = {'codigo': datos[0], 'nombre': datos[1], 'creditos': datos[2]}
            return jsonify({'Curso': curso, 'mensaje': "Curso encontrado."}) 
        else:
            return jsonify({'mensaje': "Curso no encontrado."})    
    except Exception as ex:
        return jsonify({'mensaje': "Error al listar el curso."})

#-- Método para registrar un curso nuevo
@app.route('/cursos', methods=['POST'])
def registrarCurso():
        try:                                                     
            cursor = conexion.connection.cursor()
            sql = """INSERT INTO cursos (codigo, nombre, creditos) 
            VALUES ('{0}', '{1}', {2})""".format(request.json['codigo'], 
            request.json['nombre'], request.json['creditos'])
            cursor.execute(sql) 
            conexion.connection.commit() #Confirma la acción de inserción        
            return jsonify({'mensaje': "Curso registrado con exito."})
        except Exception as ex:
            return jsonify({'mensaje': "Error al listar el curso."})

#-- Método para actualizar la información un curso
@app.route('/cursos/<codigo>', methods=['PUT'])
def actualizarCurso(codigo):
        try:            
            cursor = conexion.connection.cursor()
            sql = """UPDATE cursos SET nombre = '{0}', creditos = {1}
            WHERE codigo = '{2}'""".format(request.json['nombre'], request.json['creditos'], codigo)
            cursor.execute(sql) 
            conexion.connection.commit()
            return jsonify({'mensaje': "Curso actualizado con exito."})
        except Exception as ex:
            return jsonify({'mensaje': "Error al actualizar el curso."})

#-- Método para eliminar un curso por su ID
@app.route('/cursos/<codigo>', methods=['DELETE'])
def eliminarCurso(codigo):
    try:                
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM cursos WHERE codigo = '{0}'".format(codigo)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje': "Curso eliminado con exito."})                
    except Exception as ex:
        return jsonify({'mensaje': "Error al eliminar el curso."})

#Función para página que no existe
def paginaNoEncontrada(error):
    return "<h1>La página no existe. </h1>", 404

#Vista para ir a Index/Home/Inicio
@app.route('/home')
def home():
    return render_template('auth/home.html')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, paginaNoEncontrada)
    app.run()