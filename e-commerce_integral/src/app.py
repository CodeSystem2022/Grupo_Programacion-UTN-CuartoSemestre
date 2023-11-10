from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response, session
from flask_wtf import FlaskForm
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from wtforms import StringField, SelectField
from config import config
import json
import secrets # libreria para crear claves seguras CSRF Token
 
app = Flask(__name__)
db = MySQL(app)

app.config['SECRET_KEY'] = '7811cb752097e9ea4a8ca184582ef8649a27aaab6648fc41' #clave secreta CSRF Token

carrito = []
productos_para_preferencia = []
precio_total_carrito = 0


@app.route('/', methods=['GET','POST'])
def home():
    mensaje = request.args.get('mensaje')
    return render_template('index.html', mensaje=mensaje)


@app.route('/agregar_al_carrito/<string:nombre_producto>/<int:producto_id>', methods=['POST'])
def agregar_al_carrito(nombre_producto, producto_id):
    # Verifica si el producto ya está en el carrito
    producto_existente = next((producto for producto in carrito if producto['nombre'] == nombre_producto), None)

    if producto_existente:
        producto_existente['cantidad'] += 1
    else:
        # Agrega el producto al carrito si no existe
        carrito.append({'nombre': nombre_producto, 'producto_id': producto_id, 'cantidad': 1})

    # Redirige de nuevo a la página del carrito
    return redirect('/ver_carrito')


@app.route('/ver_carrito', methods=['GET', 'POST'])
def ver_carrito():
    productos_en_carrito = []
    # Obtén la información de la compra almacenada en la cookie
    compra_cookie = request.cookies.get('compra')
    
    # Si hay información de compra en la cookie, puedes procesarla y agregarla al carrito
    if compra_cookie:
        compra = json.loads(compra_cookie)
        nombre_producto = compra['nombre_producto']
        producto_id = compra['producto_id']
        
        # Realiza las operaciones necesarias en el carrito con esta información
        producto_existente = next((producto for producto in carrito if producto['nombre'] == nombre_producto), None)
        
        if producto_existente:
            producto_existente['cantidad'] += 1
        else:
            # Agrega el producto al carrito si no existe
            carrito.append({'nombre': nombre_producto, 'producto_id': producto_id, 'cantidad': 1})

        # Limpia la cookie después de procesar la compra
        response = make_response(render_template('ver_carrito.html'))
        response.delete_cookie('compra')
        return response

    for item in carrito:
        producto_nombre = item['nombre']

        if producto_nombre == "Hamburguesas":
            producto_id = 1
            precio_producto = 3000
        elif producto_nombre == "Pizzas":
            producto_id = 2
            precio_producto = 3000
        elif producto_nombre == "Pastas":
            producto_id = 3
            precio_producto = 5000
        elif producto_nombre == "Parrillada":
            producto_id = 4
            precio_producto = 9000
        elif producto_nombre == "Tablas":
            producto_id = 5
            precio_producto = 8000
        elif producto_nombre == "Ensaladas":
            producto_id = 6
            precio_producto = 5000
        elif producto_nombre == "Pescados":
            producto_id = 7
            precio_producto = 12000
        elif producto_nombre == "Pizzanesas":
            producto_id = 8
            precio_producto = 6000
        elif producto_nombre == "Empanadas":
            producto_id = 9
            precio_producto = 500
        elif producto_nombre == "Tostados":
            producto_id = 10
            precio_producto = 4000
        elif producto_nombre == "Lomo":
            producto_id = 11
            precio_producto = 10000
        elif producto_nombre == "Pollo":
            producto_id = 12
            precio_producto = 8500
        else:
            # Si no coincide con ningún producto conocido, asigna un valor predeterminado
            producto_id = 0
            precio_producto = 0

        cantidad = item['cantidad']
        precio_total_producto = precio_producto * cantidad

        productos_en_carrito.append({
            'id': producto_id,
            'nombre': producto_nombre,
            'precio': precio_producto,
            'cantidad': cantidad,
            'precio_total': precio_total_producto
        })

    if request.method == 'POST':
        nombre_producto = request.form.get('producto_id')
        action = request.form.get('action')
        if nombre_producto:
            for item in carrito:
                if item['nombre'] == nombre_producto:
                    if action == 'sumar':
                        item['cantidad'] += 1
                    elif action == 'restar':
                        if item['cantidad'] > 0:
                            item['cantidad'] -= 1

    precio_total_carrito = sum(item['precio_total'] for item in productos_en_carrito)
    # Convierte productos_en_carrito en una cadena JSON
    productos_en_carrito_json = json.dumps(productos_en_carrito)
    
    estado_carrito = 0
    # base de datos
    cur=db.connection.cursor()
    cur.execute("INSERT INTO `clientes` (`pedido_carrito`, `total_precio`, `estado_carrito`) VALUES (%s,%s,%s)",(productos_en_carrito_json, precio_total_carrito, estado_carrito))
    cur.execute("SELECT LAST_INSERT_ID()")
    id_carrito = cur.fetchone()[0]
    session['id_carrito'] = id_carrito# Almacena el ID del carrito en la sesión
    session['precio_total_carrito'] = precio_total_carrito
    db.connection.commit()
    cur.close()
    # agrego a clientes estado del carrito, y guardo un boolean
    # id = id
    return render_template('ver_carrito.html', productos=productos_en_carrito, precio_total_carrito=precio_total_carrito)


@app.route('/actualizar_carrito', methods=['POST'])
def actualizar_carrito():
    nombre_producto = request.form.get('producto_id')  # Recibo el nombre del producto como cadena
    action = request.form.get('action')

    if nombre_producto:
        producto_existente = next((producto for producto in carrito if producto['nombre'] == nombre_producto), None)

        if producto_existente:
            if action == 'sumar':
                producto_existente['cantidad'] += 1
            elif action == 'restar' and producto_existente['cantidad'] > 0:
                producto_existente['cantidad'] -= 1

    return redirect('/ver_carrito')


@app.route('/eliminar_del_carrito/<int:producto_id>', methods=['POST'])
def eliminar_del_carrito(producto_id):
    if producto_id in carrito:
        del carrito[producto_id]
    return render_template('carrito.html', cart=carrito)


class Checkout(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    phone_number = StringField('Number')
    email = StringField('Email')
    address = StringField('Address')
    
    

@app.route('/checkout', methods=['GET','POST'])
def checkout():         
    form = Checkout()
    first_name = form.first_name.data
    last_name = form.last_name.data
    phone_number = form.phone_number.data
    email = form.email.data
    address = form.address.data
    
    precio_total_carrito = session.get('precio_total_carrito')
    
    return render_template('checkout.html', form=form, precio_total_carrito=precio_total_carrito)

# pasar de 0 a 1
@app.route('/procesar_pago', methods=['POST'])
def procesar_pago():
    form = Checkout()
    id_carrito = session.get('id_carrito')
    id_carrito = 1
    # Verifica si se envió un archivo y lo procesa
    if 'archivosubido' in request.files:
        archivo = request.files['archivosubido']
        if archivo.filename != '':
            contenido_archivo = archivo.read()# Convierte el archivo a una secuencia de bytes (bytes)
            cur = db.connection.cursor()
            cur.execute("UPDATE `clientes` SET `ticket` = %s WHERE id = %s", (contenido_archivo, id_carrito))
            db.connection.commit()
            cur.close()
            

    # Actualizar la base de datos con los datos del cliente
    if request.method == 'POST':
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data
        email = form.email.data
        address = form.address.data
        cur = db.connection.cursor()
        query = "UPDATE `clientes` SET `nombre`=%(first_name)s, `apellido`=%(last_name)s, `telefono`=%(phone_number)s, `email`=%(email)s, `direccion`=%(address)s WHERE id=%(id_carrito)s"
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'phone_number': phone_number,
            'email': email,
            'address': address,
            'id_carrito': id_carrito
        }
        cur.execute(query, data)
        db.connection.commit()
        cur.close()
        carrito.clear()

    mensaje = "Compra exitosa. En unos minutos confirmaremos su compra a través de mensaje de WhatsApp."
    
    return redirect(url_for('home', mensaje=mensaje))   

@app.route('/galeria', methods=['GET'])
def galeria():
    return render_template('galeria.html')

@app.route('/reservas', methods=['GET','POST'])
def reservas():
    mensaje = None
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        presupuesto = request.form['presupuesto']
        orden = request.form['orden']
        direccion = request.form['direccion']
        cur = db.connection.cursor()
        cur.execute("INSERT INTO `reservas` (nombre, email, telefono, presupuesto, orden, direccion) VALUES (%s, %s, %s, %s, %s, %s)",(nombre, email, telefono, presupuesto, orden, direccion))
        db.connection.commit()
        cur.close()

        mensaje = "Reserva exitosa. En unos minutos confirmaremos su reserva a través de mensaje de WhatsApp."

    return redirect(url_for('home', mensaje=mensaje))
# Genera una cadena segura de 24 bytes
# clave_secreta = secrets.token_hex(24)
# print(clave_secreta)

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(debug=True)
    csrf.init_app(app)
