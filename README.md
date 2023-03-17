<h2>YAMDb API</h2>
<h3>Сервис с рецензиями на произведения</h3>

## Возможности
- Оставляй рецензии на произведения разных категорий и жанров - кино, книги, музыку etc.
- Ставь оценку работам
- Коментируй рецензии других пользователей

## Технологии
[![My Skills](https://skillicons.dev/icons?i=python,django,postgres,nginx,bootstrap&theme=light)](https://skillicons.dev)

## Как запустить проект на тестовом сервере:
Клонировать репозиторий, перейти в директорию с проектом.
```
git clone https://github.com/tiya001/infra_sp2.git
```
Cоздать и активировать виртуальное окружение:
```
python -m venv venv
```
```
source venv/source/activate
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
## Cоздание файла с переменными окружения:
```
cd infra
```
```
touch .env
```
```
nano .env
```
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=test_base
POSTGRES_USER=test_user
POSTGRES_PASSWORD=test_pass
DB_HOST=127.0.0.1
DB_PORT=5432
```
## Запуск контейнеров:
```
docker-compose up -d --build
```
Выполнение миграций:
```
docker-compose exec web python manage.py migrate
```
Создание superuser
```
docker-compose exec web python manage.py createsuperuser
```
Статика:
```
docker-compose exec web python manage.py collectstatic --no-input 
```
Заполнение БД из фикстуры:
```
docker-compose exec web python manage.py loaddata fixtures.json
```
