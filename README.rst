Aiogram template
================

Template for creating Python telegram bots using the Aiogram library. 🐍

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
        DB_URL="postgresql+asyncpg://localhost/telegram_bot"


#. Install the necessary dependencies with the help of **poetry** 🔽

    ::

        poetry install

#. Now you can run the bot! 🎉

    ::

        poetry run python3 bot
