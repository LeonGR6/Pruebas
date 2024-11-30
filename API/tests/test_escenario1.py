import json
from flask_jwt_extended import create_access_token
from DB.Extension import db
from DB.Models import Category

# En este escenario, un usuario intenta registrarse en una plataforma en línea, pero se enfrenta a varios imprevistos.
# Primero, intenta registrarse con un correo electrónico que ya ha sido utilizado por otro usuario.
# Después de resolver este inconveniente, logra registrarse exitosamente con sus datos y recibe una confirmación
# de que su cuenta ha sido creada. Una vez registrado, inicia sesión en la plataforma utilizando su correo y contraseña.

# Al ingresar, el usuario tiene acceso a diferentes funcionalidades dentro de la plataforma, entre ellas, la creación
# de categorías para organizar los libros. Tras crear una categoría con éxito, el usuario agrega un libro a esa categoría.
# Después de completar todo lo que quería hacer, decide cerrar su sesión para salir de la plataforma de manera segura.



# Prueba unitaria El usuario intenta registrar un correo que ya se ha utilizado.
def test_register_duplicate_email(client):

    client.post('/api/auth/register', json={
        'name': 'John Doe',
        'email': 'johndoe@example.com',
        'password': 'SecurePass123'
    })
    response = client.post('/api/auth/register', json={
        'name': 'Jane Doe',
        'email': 'johndoe@example.com',
        'password': 'AnotherPass123'
    })
    assert response.status_code == 400  

def test_register_empty_email(client):

    response = client.post('/api/auth/register', json={
        'name': 'John Doe',
        'email': '',
        'password': 'SecurePass123'
    })

    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Email is required' in data['errors']


# Prueba unitaria El usuario se registra de una manera exitosa.
def test_register_user(client):
    
    response = client.post('/api/auth/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'StrongPassword123'
    })

    assert response.status_code == 201  

    data = json.loads(response.data)
    assert 'id' in data  
    assert data['name'] == 'Test User'
    assert data['email'] == 'test@example.com'

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



def test_create_book_success(client, app):
    
    with app.app_context():
        category = Category(name="Fiction")
        db.session.add(category)
        db.session.commit()
        access_token = create_access_token(identity={"user_id": 1})

    # Crear un token JWT válido
    headers = {"Authorization": f"Bearer {access_token}"}

    # Datos válidos del libro
    book_data = {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "category_id": 1,  # ID de la categoría creada
        "description": "A novel set in the 1920s.",
        "publication_date": "1925-04-10",
    }

    # Enviar solicitud POST para crear un libro
    response = client.post("/api/book/create", json=book_data, headers=headers)

    # Verificaciones
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == book_data["title"]
    assert data["author"] == book_data["author"]

#Prueba unitaria para cierre de sesión exitoso
def test_logout_success(client):
    
    response = client.post('/api/auth/logout')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Logout successful'












    
    