Avito Parser
============
A bot that allows you to receive notifications about new ads on Avito. 
Written in Python using the Aiogram library. 🐍

🏃 How do I run it?
----------------
#. Clone this repository 🚀

    ::

        git clone https://github.com/t3m8ch/aiogram-template.git
        cd aiogram-template

#. Copy ***-example.env** to **.env** 🔄

    ::

        cp minimal-example.env .env
        # OR
        cp full-example.env .env

#. Edit the **.env** file using a text editor 📋

    If you use webhooks and use the minimal example,
    you need to add the **TG_WEBHOOK_HOST** parameter,
    which specifies the host to which Telegram will send requests.

    Default values:
    ::

        TG_WEBHOOK_PATH=/bot
        WEBAPP_HOST=localhost
        WEBAPP_PORT=3000
        LOG_LEVEL=INFO
        DB_URL="postgresql+asyncpg://localhost/avito_parser"


#. Install the necessary dependencies with the help of **poetry** 🔽

    ::

        poetry install

#. Copy **alembic.example.ini** to **alembic.ini** 🔄

    ::

        cp alembic.example.ini alembic.ini

#. If you changed the default value of **DB_URL**,
   change it in **alembic.ini** as well ❗

    ::

        sqlalchemy.url = insert://connection:string@to/postgres_here

#. Create a database in Postgresql 🎩

    ::

        psql -c "create database avito_parser"

#. Do the migrations 🐦

    ::

        poetry run alembic upgrade head

#. Now you can run the bot! 🎉

    ::

        poetry run python3 bot
