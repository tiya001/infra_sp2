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
source venv/Scripts/activate
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
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
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
Заполнение БД из фикстуры:
```
cp fixtures.json container_id:app/fixtures.json
```
```
docker-compose exec web python manage.py loaddata fixtures.json
```
Создание superuser
```
docker-compose exec web python manage.py createsuperuser
```
Статика:
```
docker-compose exec web python manage.py collectstatic --no-input 
```

