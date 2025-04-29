import requests
import json
import sys
import os

# BASE_URL = 'http://localhost:8000/'  # Adjust based on your server address
BASE_URL = 'http://sc21xz2.pythonanywhere.com/'
TOKEN_FILE = '.token'

# Save token to a file
def save_token(token):
    with open(TOKEN_FILE, 'w') as f:
        f.write(token)

# Retrieve saved token
def get_saved_token():
    try:
        with open(TOKEN_FILE, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("❌ Token file not found. Please log in first.")
        return None

# Remove token file (logout)
def logout_user():
    try:
        os.remove(TOKEN_FILE)
        print("✅ Logged out successfully.")
    except FileNotFoundError:
        print("ℹ️ No active session to log out from.")

# Register user
def register_user(username, email, password):
    url = BASE_URL + 'register/'
    data = {'username': username, 'email': email, 'password': password}
    response = requests.post(url, data=data)
    if response.status_code == 201:
        print("✅ Registration successful.")
    else:
        print(f"❌ Registration failed: {response.text}")

# Log in user
def login_user(username, password):
    url = BASE_URL + 'login/'
    data = {'username': username, 'password': password}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        token = response.json().get('access')
        save_token(token)
        print("✅ Login successful, token saved.")
    else:
        print(f"❌ Login failed: {response.text}")

# List modules and professors
def list_modules():
    token = get_saved_token()
    if not token:
        return
    url = BASE_URL + 'api/modules/'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Failed to retrieve data: {response.text}")

# View all professor ratings
def view_ratings():
    token = get_saved_token()
    if not token:
        return
    url = BASE_URL + 'api/professors/ratings/'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        ratings = response.json()
        if ratings:
            for prof_id, rating in ratings.items():
                print(f"Professor {prof_id}: {rating}")
        else:
            print("⚠️ No ratings found.")
    else:
        print(f"❌ Failed to retrieve ratings: {response.text}")

# View average rating of a professor in a module
def get_average(professor_id, module_code):
    token = get_saved_token()
    if not token:
        return
    url = BASE_URL + f'api/professor/{professor_id}/module/{module_code}/'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and result:
            print(f"Average Rating: {result[0]}")
        else:
            print("⚠️ No rating records found.")
    else:
        print(f"❌ Failed to retrieve data: {response.text}")

# Rate a professor
def rate_professor(professor_id, module_code, year, semester, rating):
    token = get_saved_token()
    if not token:
        return
    url = BASE_URL + 'api/rate/'
    headers = {'Authorization': f'Bearer {token}'}
    
    # Validate rating input
    if not (1 <= rating <= 5):
        print("❌ Rating must be between 1 and 5.")
        return
    
    data = {
        'professor_id': professor_id,
        'code': module_code,
        'year': year,
        'semester': semester,
        'rating': rating
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print(f"✅ Successfully rated {professor_id} in {module_code}: {rating}")
    else:
        print(f"❌ Rating failed: {response.text}")

# Command-line entry point
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python wp3.py <command> [parameters]")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'register':
        if len(sys.argv) != 5:
            print("Usage: register <username> <email> <password>")
        else:
            register_user(sys.argv[2], sys.argv[3], sys.argv[4])

    elif command == 'login':
        if len(sys.argv) != 4:
            print("Usage: login <username> <password>")
        else:
            login_user(sys.argv[2], sys.argv[3])

    elif command == 'logout':
        logout_user()

    elif command == 'list':
        list_modules()

    elif command == 'view':
        view_ratings()

    elif command == 'average':
        if len(sys.argv) != 4:
            print("Usage: average <professor_id> <module_code>")
        else:
            get_average(sys.argv[2], sys.argv[3])

    elif command == 'rate':
        if len(sys.argv) != 7:
            print("Usage: rate <professor_id> <module_code> <year> <semester> <rating>")
        else:
            try:
                rating = int(sys.argv[6])
                rate_professor(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), rating)
            except ValueError:
                print("❌ Rating must be an integer.")
            else:
                print("Usage: rate <professor_id> <module_code> <year> <semester> <rating>")

    else:
        print("Unknown command.")
