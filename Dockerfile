FROM python:3.8-slim-buster

RUN pip install --upgrade pip \
    pip install discord.py==2.3.2 && \ 
    pip install python-dotenv

WORKDIR /bot

COPY *.py .env ./

CMD ["python3", "bot.py"]