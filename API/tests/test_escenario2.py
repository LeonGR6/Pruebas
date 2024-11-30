import json
from flask_jwt_extended import create_access_token
from DB.Extension import db
from DB.Models import Category

# En este escenario, un usuario intenta registrarse en una plataforma en línea, pero primero se enfrenta a un inconveniente
# relacionado con el formato incorrecto de su correo electrónico. Después de corregir este problema, el registro
# se realiza de forma exitosa y el usuario inicia sesión en su cuenta. Posteriormente, el usuario intenta crear una categoría,
# pero se encuentra con una categoría que ya existe, lo que genera un conflicto. Luego, el usuario continúa creando un libro
# correctamente, y finalmente elimina un libro de la plataforma. Todo esto ocurre en un flujo de acciones validadas por el sistema.


# Prueba Unitaria El usuario intenta registrarse con el formato del correo incorrecto-
# se registra correctamente e inicia sesion exitosamente  

# Prueba unitaria para validar formato de correo inválido.
def test_register_invalid_email(client):
    
    response = client.post('/api/auth/register', json={
        'name': 'John Doe',
        'email': 'invalidemail',
        'password': 'SecurePass123'
    })

    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Invalid email format' in data['errors']


# Prueba unitaria para validar que el usuario se registra correctamente.
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


def test_create_existing_category(client, app, accessToken):
    
    with app.app_context():
        category = Category(name="Books")
        db.session.add(category)
        db.session.commit()

    
    headers = {"Authorization": f"Bearer {accessToken}"}

    # Intentar crear una categoría duplicada
    category_data = {"name": "Books"}
    response = client.post("/api/category/create", json=category_data, headers=headers)

    # Verificaciones
    assert response.status_code == 409, f"Expected 409, got {response.status_code}"
    data = response.get_json()
    assert data["message"] == "Category already exists", f"Unexpected message: {data.get('message')}"




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
    data = response.get_json()
    assert data["title"] == book_data["title"]
    assert data["author"] == book_data["author"]
    
    
def test_delete_book_success(client, app):
    with app.app_context():
        category = Category(name="Science")
        db.session.add(category)
        db.session.commit()
        access_token = create_access_token(identity={"user_id": 1})

    # Crear un libro
    book_data = {
        "title": "Cosmos",
        "author": "Carl Sagan",
        "category_id": 1,
        "description": "A space exploration journey.",
        "publication_date": "1980-01-01"
    }

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/api/book/create", json=book_data, headers=headers)
    book_id = json.loads(response.data)["id"]

    # Eliminar el libro
    response = client.delete(f"/api/book/delete/{book_id}", headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Book deleted successfully'
