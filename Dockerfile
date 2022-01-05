FROM python:3.8-slim-buster

RUN pip install --upgrade pip \
    pip install -U discord.py && \ 
    pip install python-dotenv

WORKDIR /bot

COPY *.py .env ./

CMD ["python3", "bot.py"]