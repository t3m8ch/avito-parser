# Avito Parser

A bot that allows you to receive notifications about new ads on Avito. 
Written in Python using the Aiogram library 🐍

## 🏃 How do I run it?

### 1. Clone this repository 🚀
```bash
git clone https://github.com/t3m8ch/aiogram-template.git
cd aiogram-template
```

### 2. Copy **-example.env* to *.env* 🔄 
```bash
cp minimal-example.env .env
# OR
cp full-example.env .env
```

### 3. Edit the *.env* file using a text editor 📋
If you use webhooks and use the minimal example,
you need to add the **TG_WEBHOOK_HOST** parameter,
which specifies the host to which Telegram will send requests.

Default values:
```dotenv
TG_SKIP_UPDATES=NO
TG_WEBHOOK_PATH=/bot
WEBAPP_HOST=localhost
WEBAPP_PORT=3000
LOG_LEVEL=INFO
DB_URL="postgresql+asyncpg://localhost/avito_parser"
CHECK_INTERVAL_SECONDS=180
```

Valid values of **TG_SKIP_UPDATES**: `YES/Y/TRUE/1` or `NO/N/FALSE/0`

Webhooks can be used without setting SSL options if you use Certbot 
certificates or a certificate purchased from a Certificate Authority 
or if you use **Ngrok**.

### 4. Install the necessary dependencies with the help of **poetry** 🔽
```bash
poetry install
```

### 5. Copy *alembic.example.ini* to *alembic.ini* 🔄
```bash
cp alembic.example.ini alembic.ini
```

### 6. If you changed the default value of *DB_URL*, change it in *alembic.ini* as well ❗ 
```ini
sqlalchemy.url = insert://connection:string@to/postgres_here
```

### 7. Create a database in Postgresql 🎩
```bash
psql -c "create database avito_parser"
```

### 8. Do the migrations 🐦
```bash
poetry run alembic upgrade head
```

### 9. Now you can run the bot! 🎉
```bash
poetry run python3 bot
```
