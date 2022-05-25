"""" 
    INTEGRANTES:
- Santiago Rondón Galvis
- Ángela Maria Romero Arrieta
""" 
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)
#Con esto sabemos SI ejecutamos este archivo como principal (clase main)

conexion = MySQL(app) 
#Acá tengo la conexion para trabajar con la BDD y sus tablas

@app.route('/index')
def index():
    return '<h1>Página de inicio. -Sistema de registro de materias, TdeA</h1>'

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
        return jsonify({'cursos': cursos, 'mensaje': "Cursos registrados en la Base de Datos."})
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

def paginaNoEncontrada(error):
    return "<h1>La página no existe. </h1>", 404

#Acá ejecuto la aplicación
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, paginaNoEncontrada)
    app.run()

