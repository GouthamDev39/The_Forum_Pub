FROM python:3.10-slim

WORKDIR /home/Forum_app

COPY ./requirements.txt .

COPY ./alembic_start.sh .

RUN chmod +x /home/Forum_app/alembic_start.sh

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["./alembic_start.sh"]
