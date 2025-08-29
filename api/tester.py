import requests
import json

# Define the API endpoint URLs
register_url = 'http://localhost:8000/api/register/'
login_url = 'http://localhost:8000/api/login/'
protected_url = 'http://localhost:8000/api/ride/'  # Replace with a protected endpoint

# Define the registration data
register_data = {
    'username': 'testuser',
    'email': 'testuser@example.com',
    'password': 'password123'
}

# Send a POST request to the registration endpoint
response = requests.post(register_url, json=register_data)
print('Registration Response:', response.status_code)
print('Registration Response Data:', response.json())

# Define the login data
login_data = {
    'username': 'testuser',
    'password': 'password123'
}

# Send a POST request to the login endpoint
response = requests.post(login_url, json=login_data)
print('Login Response:', response.status_code)
print('Login Response Data:', response.json())

# Get the token from the login response
token = response.json().get('token')
if token:
    # Use the token to access a protected endpoint
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(protected_url, headers=headers)
    print('Protected Endpoint Response:', response.status_code)
    print('Protected Endpoint Response Data:', response.json())
else:
    print('No token received')