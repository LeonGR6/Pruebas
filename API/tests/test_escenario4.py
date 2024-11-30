import json
import json
from flask_jwt_extended import create_access_token
from DB.Extension import db
from DB.Models import Category

#En este escenario, el usuario realiza varias acciones en un sistema de autenticación y gestión de libros. Primero,
# el usuario intenta registrarse con un nombre vacío, lo que genera un error indicando que el nombre es obligatorio.
# Luego, intenta registrarse con un correo vacío, lo que también genera un error con un mensaje similar. En su tercer
# intento, el usuario se registra correctamente con los datos completos, y su cuenta se crea con éxito.

# El usuario intenta iniciar sesión con una contraseña incorrecta, lo que da como resultado un mensaje
# de error de "Credenciales inválidas". Luego, realiza una prueba de inicio de sesión con campos vacíos, lo que genera un error
# debido a los campos faltantes. Finalmente, el usuario realiza un inicio de sesión exitoso con las credenciales correctas,
# obteniendo un token de acceso.

# El flujo continúa con la creación de un libro, pero el usuario envía datos inválidos (faltando la fecha de publicación),
# lo que genera un error de validación. Este flujo asegura que las entradas de usuario sean validadas correctamente
# y que se manejen los casos de error de manera adecuada en el sistema.

# Prueba unitaria para verificar registro con nombre vacío.
def test_register_empty_name(client):

    response = client.post('/api/auth/register', json={
        'name': '',
        'email': 'johndoe@example.com',
        'password': 'SecurePass123'
    })

    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Name is required' in data['errors']
    

# Prueba unitaria para verificar registro con correo vacío.
def test_register_empty_email(client):

    response = client.post('/api/auth/register', json={
        'name': 'John Doe',
        'email': '',
        'password': 'SecurePass123'
    })

    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Email is required' in data['errors']
    
    
# Prueba unitaria para registrar usuario.
def test_register_user(client):
    
    response = client.post('/api/auth/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'StrongPassword123'
    })

    assert response.status_code == 201  # Verificacion

    data = json.loads(response.data)
    assert 'id' in data  
    assert data['name'] == 'Test User'
    assert data['email'] == 'test@example.com'

# Prueba unitaria para contraseña incorrecta.
def test_login_invalid_password(client):
    
    client.post('/api/auth/register', json={
        'name': 'John Doe',
        'email': 'johndoe@example.com',
        'password': 'SecurePass123'
    })
    response = client.post('/api/auth/login', json={
        'email': 'johndoe@example.com',
        'password': 'WrongPass'
    })

    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['message'] == 'Invalid credentials'
    
# 
def test_login_missing_fields(client):
    """Prueba unitaria para campos faltantes."""
    response = client.post('/api/auth/login', json={
        'email': '',
        'password': ''
    })

    assert response.status_code == 404
    
#Prueba unitaria para inicio de sesión exitoso.
def test_login_success(client):
    
    client.post('/api/auth/register', json={
        'name': 'John Doe',
        'email': 'johndoe@example.com',
        'password': 'SecurePass123'
    })
    response = client.post('/api/auth/login', json={
        'email': 'johndoe@example.com',
        'password': 'SecurePass123'
    })

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'accessToken' in data
    assert data['name'] == 'John Doe'

def test_create_book_invalid_data(client, app):
    with app.app_context():
        category = Category(name="Science")
        db.session.add(category)
        db.session.commit()
        access_token = create_access_token(identity={"user_id": 1})

    headers = {"Authorization": f"Bearer {access_token}"}

    # Datos inválidos del libro (faltan campos requeridos)
    book_data = {
        "title": "Cosmos",
        "author": "Carl Sagan",
        "category_id": 1,
        "description": "A space exploration journey.",
        # Falta la fecha de publicación
    }

    # Enviar solicitud POST para crear un libro
    response = client.post("/api/book/create", json=book_data, headers=headers)

    # Verificaciones
    assert response.status_code == 400
  