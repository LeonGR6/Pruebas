
# import json


#                     ###### Register ######


# # 1°
# # Prueba unitaria para verificar el comportamiento del endpoint de registro de usuarios en una API REST.
# def test_register_user(client):
    
#     response = client.post('/api/auth/register', json={
#         'name': 'Test User',
#         'email': 'test@example.com',
#         'password': 'StrongPassword123'
#     })

#     assert response.status_code == 201  # Verificacion

#     data = json.loads(response.data)
#     assert 'id' in data  
#     assert data['name'] == 'Test User'
#     assert data['email'] == 'test@example.com'

# # 2
# # Prueba unitaria para verificar registro con correo duplicado.
# def test_register_duplicate_email(client):

#     client.post('/api/auth/register', json={
#         'name': 'John Doe',
#         'email': 'johndoe@example.com',
#         'password': 'SecurePass123'
#     })
#     response = client.post('/api/auth/register', json={
#         'name': 'Jane Doe',
#         'email': 'johndoe@example.com',
#         'password': 'AnotherPass123'
#     })
#     assert response.status_code == 400  # No se puede registrar
    
    

# # 3
# # Prueba unitaria para validar formato de correo inválido.
# def test_register_invalid_email(client):
    
#     response = client.post('/api/auth/register', json={
#         'name': 'John Doe',
#         'email': 'invalidemail',
#         'password': 'SecurePass123'
#     })

#     assert response.status_code == 400
#     data = json.loads(response.data)
#     assert 'Invalid email format' in data['errors']

# # 4
# # Prueba unitaria para verificar registro con contraseña débil.
# def test_register_weak_password(client):

#     response = client.post('/api/auth/register', json={
#         'name': 'John Doe',
#         'email': 'johndoe@example.com',
#         'password': 'weak'
#     })

#     assert response.status_code == 400
#     data = json.loads(response.data)
#     assert 'Password must be at least 8 characters long' in data['errors']

# # 5
# # Prueba unitaria para verificar registro con nombre vacío.
# def test_register_empty_name(client):

#     response = client.post('/api/auth/register', json={
#         'name': '',
#         'email': 'johndoe@example.com',
#         'password': 'SecurePass123'
#     })

#     assert response.status_code == 400
#     data = json.loads(response.data)
#     assert 'Name is required' in data['errors']

# # 6
# # Prueba unitaria para verificar registro con correo vacío.
# def test_register_empty_email(client):

#     response = client.post('/api/auth/register', json={
#         'name': 'John Doe',
#         'email': '',
#         'password': 'SecurePass123'
#     })

#     assert response.status_code == 400
#     data = json.loads(response.data)
#     assert 'Email is required' in data['errors']

# # 7
# # Prueba unitaria para verificar registro con contraseña vacía.
# def test_register_empty_password(client):

#     response = client.post('/api/auth/register', json={
#         'name': 'John Doe',
#         'email': 'johndoe@example.com',
#         'password': ''
#     })

#     assert response.status_code == 400
#     data = json.loads(response.data)
#     assert 'Password is required' in data['errors']


# # 8
# # Prueba unitria para verificar registro con contraseña sin mayúsculas.
# def test_register_password_without_uppercase(client):

#     response = client.post('/api/auth/register', json={
#         'name': 'John Doe',
#         'email': 'johndoe@example.com',
#         'password': 'securepass1'
#     })

#     assert response.status_code == 400
#     data = json.loads(response.data)
#     assert 'Password must contain at least one uppercase letter' in data['errors']

# # 9
# # Prueba unitaria para verificar registro con contraseña sin Digitos.
# def test_register_password_without_lowercase(client):

#     response = client.post('/api/auth/register', json={
#         'name': 'John Doe',
#         'email': 'johndoe@example.com',
#         'password': 'SecurePass'
#     })

#     assert response.status_code == 400
#     data = json.loads(response.data)
#     assert 'Password must contain at least one digit' in data['errors']


#                     ###### Login ######


# #1
# #Prueba unitaria para inicio de sesión exitoso.
# def test_login_success(client):
    
#     client.post('/api/auth/register', json={
#         'name': 'John Doe',
#         'email': 'johndoe@example.com',
#         'password': 'SecurePass123'
#     })
#     response = client.post('/api/auth/login', json={
#         'email': 'johndoe@example.com',
#         'password': 'SecurePass123'
#     })

#     assert response.status_code == 200
#     data = json.loads(response.data)
#     assert 'accessToken' in data
#     assert data['name'] == 'John Doe'

# # 2°
# # Prueba unitaria para usuario inexistente
# def test_login_user_not_found(client):
    
#     response = client.post('/api/auth/login', json={
#         'email': 'notfound@example.com',
#         'password': 'SecurePass123'
#     })

#     assert response.status_code == 404
#     data = json.loads(response.data)
#     assert data['message'] == 'User not found'

# # 3
# # Prueba unitaria para contraseña incorrecta.
# def test_login_invalid_password(client):
    
#     client.post('/api/auth/register', json={
#         'name': 'John Doe',
#         'email': 'johndoe@example.com',
#         'password': 'SecurePass123'
#     })
#     response = client.post('/api/auth/login', json={
#         'email': 'johndoe@example.com',
#         'password': 'WrongPass'
#     })

#     assert response.status_code == 401
#     data = json.loads(response.data)
#     assert data['message'] == 'Invalid credentials'

# # 4°
# # 
# def test_login_missing_fields(client):
#     """Prueba unitaria para campos faltantes."""
#     response = client.post('/api/auth/login', json={
#         'email': '',
#         'password': ''
#     })

#     assert response.status_code == 404

# # 5°
# # Prueba unitaria para formato inválido en el inicio de sesión.
# def test_login_invalid_format(client):
    
#     response = client.post('/api/auth/login', json={
#         'email': 'invalidemail',
#         'password': 'SecurePass123'
#     })

#     assert response.status_code == 404  # Email inválido, no coincide con un usuario existente


#                     ###### Logout ######


# # 1°
# # Prueba unitaria para cierre de sesión exitoso
# def test_logout_success(client):
    
#     response = client.post('/api/auth/logout')

#     assert response.status_code == 200
#     data = json.loads(response.data)
#     assert data['message'] == 'Logout successful'


# # 2°
# # Prueba unitaria para verificar múltiples solicitudes de cierre de sesión.
# def test_logout_multiple_requests(client):
   
#     response1 = client.post('/api/auth/logout')
#     response2 = client.post('/api/auth/logout')

#     assert response1.status_code == 200
#     assert response2.status_code == 200

# # 3°
# # Prueba unitaria para cierre de sesión sin token.
# def test_logout_without_token(client):
    
#     response = client.post('/api/auth/logout')

#     assert response.status_code == 200  # Asumiendo que el token no es obligatorio

# # 4°

# def test_logout_invalid_method(client):
    
#     response = client.get('/api/auth/logout')

#     assert response.status_code == 405  # Método no permitido

# # 5
# # Prueba unitaria para verificar que un endpoint inválido retorna error
# def test_logout_invalid_endpoint(client):
    
#     response = client.post('/api/auth/logou')

#     assert response.status_code == 404  # Endpoint no encontrado
