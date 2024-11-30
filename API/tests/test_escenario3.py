import json
from flask_jwt_extended import create_access_token
from DB.Extension import db
from DB.Models import Category, Book, User

#En este escenario, un usuario interactúa con un sistema de gestión de libros. Primero, intenta registrarse con una contraseña
# que no cumple los requisitos de seguridad (sin mayúsculas o dígitos), lo que resulta en respuestas de error. En su tercer intento,
# el usuario registra su cuenta con éxito, cumpliendo con los requisitos de contraseña. Luego, el usuario intenta iniciar sesión
# con un formato incorrecto de correo electrónico, lo que también resulta en un error. Después de un inicio de sesión exitoso,
# crea una categoría de libros llamada "Fiction" y luego registra un libro titulado "Principito" dentro de esa categoría. Finalmente,
# el usuario realiza un préstamo del libro creado, registrando las fechas de préstamo y devolución.


# Prueba unitria para verificar registro con contraseña sin mayúsculas.
def test_register_password_without_uppercase(client):

    response = client.post('/api/auth/register', json={
        'name': 'John Doe',
        'email': 'johndoe@example.com',
        'password': 'securepass1'
    })

    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Password must contain at least one uppercase letter' in data['errors']

# Prueba unitaria para verificar registro con contraseña sin Digitos.
def test_register_password_without_lowercase(client):

    response = client.post('/api/auth/register', json={
        'name': 'John Doe',
        'email': 'johndoe@example.com',
        'password': 'SecurePass'
    })

    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Password must contain at least one digit' in data['errors']

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


# Prueba unitaria para formato inválido en el inicio de sesión.
def test_login_invalid_format(client):
    
    response = client.post('/api/auth/login', json={
        'email': 'invalidemail',
        'password': 'SecurePass123'
    })

    assert response.status_code == 404  # Email inválido, no coincide con un usuario existente

def test_create_book_success(client, app):
    # Crear una categoría para asignarla al libro
    with app.app_context():
        category = Category(name="Fiction")
        db.session.add(category)
        db.session.commit()
        access_token = create_access_token(identity={"user_id": 1})

    # Crear un token JWT válido
    headers = {"Authorization": f"Bearer {access_token}"}

    # Datos válidos del libro
    book_data = {
        "title": "Principito",
        "author": "F. Scott Fitzgerald",
        "category_id": 1,  # ID de la categoría creada
        "description": "A novel set in the 1920s.",
        "publication_date": "1925-04-10",
    }

    # Enviar solicitud POST para crear un libro
    response = client.post("/api/book/create", json=book_data, headers=headers)

    # Verificaciones
    assert response.status_code == 201
    
def test_create_loan_success(client, app, accessToken):
    # Crear una categoría para asignarla al libro
    with app.app_context():
        category = Category(name="Fiction")
        db.session.add(category)
        db.session.commit()
        access_token = create_access_token(identity={"user_id": 1})

        # Crear un libro y asignar la categoría creada
        book = Book(
            title="Principito",
            author="F. Scott Fitzgerald",
            category_id= 1,  # Asignar la categoría creada
            description="A novel set in the 1920s.",
            publication_date="1925-04-10"
        )
        db.session.add(book)
        db.session.commit()
        
           
    headers = {"Authorization": f"Bearer {access_token}"}

    # Datos válidos del préstamo
    loan_data = {
        "book_id": 1,
        "loan_date": "2024-11-29",
        "return_date": "2024-12-29"
    }

    # Enviar solicitud POST para crear un préstamo
    response = client.post("/api/loan/create",
    json=loan_data, headers={"Authorization": f"Bearer {accessToken}"})

    # Verificaciones
    assert response.status_code == 201
