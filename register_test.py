import requests

def register_user(username, email, password):
    url = 'http://localhost:8000/api/register/'  # Replace with your registration endpoint
    data = {
        'username': username,
        'email': email,
        'password': password
    }

    response = requests.post(url, json=data)

    if response.status_code == 201:
        print(f"User '{username}' created successfully!")
    else:
        print(f"Error creating user: {response.text}")

# Example usage:
username = "johnDoe"
email = "john@example.com"
password = "password123"

register_user(username, email, password)