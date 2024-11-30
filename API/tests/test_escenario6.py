import json
# Un usuario decide devolver el libro, por lo que el encargado -
# deberá eliminar el registro de dicho prestamo.



# El encargado busca el registro con el id que se le otorgo al -
# usuario cuando realizo su registro.


# Prueba unitaria para verificar registro con contraseña débil.
def test_register_weak_password(client):

    response = client.post('/api/auth/register', json={
        'name': 'John Doe',
        'email': 'johndoe@example.com',
        'password': 'weak'
    })

    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Password must be at least 8 characters long' in data['errors']


# Prueba unitaria para verificar registro con contraseña vacía.
def test_register_empty_password(client):

    response = client.post('/api/auth/register', json={
        'name': 'John Doe',
        'email': 'johndoe@example.com',
        'password': ''
    })

    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Password is required' in data['errors']

# Prueba unitaria para verificar el comportamiento del endpoint de registro de usuarios en una API REST.
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

# Prueba unitaria para usuario inexistente
def test_login_user_not_found(client):
    
    response = client.post('/api/auth/login', json={
        'email': 'notfound@example.com',
        'password': 'SecurePass123'
    })

    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['message'] == 'User not found'
    
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



# Prueba unitaria para encontrar el prestamo de un libro.
def test_search_loan(client, new_loan, accessToken):
    loan_id = new_loan["id"]
    response = client.get(
        f"/api/loan/{loan_id}", 
        headers={"Authorization": f"Bearer {accessToken}"}
    )
    assert response.status_code == 200
    assert response.json == {
        "id": 1,
        "book_id": 1,
        "user_id": 1,
        "loan_date": "2024-11-27 00:00:00",
        "return_date": "2024-12-04 00:00:00",
    }
    
    

#    Una vez encontrado procede a eliminarlo.
def test_delete_loan(client, new_loan, accessToken):
    loan_id = new_loan["id"]
    response = client.delete(
        f"/api/loan/delete/{loan_id}",
        
        headers={"Authorization": f"Bearer {accessToken}"}
    )
    assert response.status_code == 200
    assert response.json == {"message": "Loan deleted successfully"}


# Prueba unitaria para cierre de sesión exitoso
def test_logout_success(client):
    
    response = client.post('/api/auth/logout')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Logout successful'
