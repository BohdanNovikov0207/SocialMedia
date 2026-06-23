# Social Network Project
# ENG

## 1. Project Purpose

The goal of this project is to build a beginner-friendly social network that helps

- understand Django web application architecture
- learn authentication and authorization
- implement post and chat systems
- gain team development experience

## 2. Team Members

- **Bohdan Novikov**
    GitHub: https://github.com/BohdanNovikov0207/

- **Alina Sorukhan**
    GitHub: https://github.com/AlinaSoruhan/

- **Ivan Mykhailiuk**
    GitHub: https://github.com/Ivan55555555555/

## 3. Modules

- **Django** - backend framework
- **Daphne** - ASGI server
- **Channels** - WebSocket and real-time features
- **Pillow** - image processing

## 4. How to Run the Project

```
- 1. Type in an opened terminal
    git clone https://github.com/BohdanNovikov0207/SocialMedia.git

- 2. Move to directory of cloned repository, the command should be next
    cd SocialMedia

- 3. Make virtual environment, activate it and install dependencies
    python -m venv venv
    source venv/Scripts/activate - if you are on Windows OS
    source venv/bin/activate - if you are on Linux based OS
    pip install -r requirements.txt

- 4. Move to a directory of django project
    cd Social_Network

- 5. Make migrations to database, run project
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
```

## 5. Project Structure (Applications)

![Project Structure](https://imgur.com/a/MXtQX0U)

### chat_app
- private chats
- group chats
- real-time messaging
- online/offline status view

### home_app
- main feed
- posts from all users

### post_app
- personal posts page

### user_app
- registration and login
- friends system

## 6. Conclusion

During the development process, the team:

- learned Django
- built a multi-app project
- implemented core social network features
- improved teamwork skills

Possible future improvements:
- likes and comments
- UI improvements


# UA

## 1. Мета проєкту

Метою цього проєкту є створення дружньої до початківців соціальної мережі, яка допомагає:

- зрозуміти архітектуру вебзастосунків на Django
- вивчити аутентифікацію та авторизацію
- реалізувати систему постів і чатів
- отримати досвід командної розробки

## 2. Учасники команди

- **Bohdan Novikov**
    GitHub: https://github.com/BohdanNovikov0207/

- **Alina Sorukhan**
    GitHub: https://github.com/AlinaSoruhan/

- **Ivan Mykhailiuk**
    GitHub: https://github.com/Ivan55555555555/

## 3. Модулі

- **Django** — backend-фреймворк
- **Daphne** — ASGI-сервер
- **Channels** — WebSocket та можливості роботи в реальному часі
- **Pillow** — обробка зображень

## 4. Як запустити проєкт

```
- 1. Введіть у відкритому терміналі
    git clone https://github.com/BohdanNovikov0207/SocialMedia.git

- 2. Перейдіть у директорію клонованого репозиторію
    cd SocialMedia

- 3. Створіть віртуальне середовище, активуйте його та встановіть залежності
    python -m venv venv
    source venv/Scripts/activate - якщо ви на Windows OS
    source venv/bin/activate - якщо ви на Linux-подібній OS
    pip install -r requirements.txt

- 4. Перейдіть у директорію Django-проєкту
    cd Social_Network

- 5. Виконайте міграції бази даних та запустіть проєкт
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
```

## 5. Структура проєкту (додатки)

![Структура проєкту](https://imgur.com/a/MXtQX0U)

### chat_app
- приватні чати  
- групові чати  
- обмін повідомленнями в реальному часі  
- відображення статусу онлайн/офлайн  

### home_app
- головна стрічка  
- пости всіх користувачів  

### post_app
- сторінка особистих публікацій  

### user_app
- реєстрація та вхід  
- система друзів  

## 6. Висновок

Під час розробки проєкту команда:

- вивчила Django  
- побудувала багатододатковий проєкт  
- реалізувала базовий функціонал соціальної мережі  
- покращила навички командної роботи  

Можливі напрями подальшого розвитку:
- лайки та коментарі
- покращення користувацького інтерфейсу