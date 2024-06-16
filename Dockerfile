FROM atomhub.openatom.cn/amd64/python:3.11.5-slim-bullseye

WORKDIR /app

COPY ./app /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["./run.sh"]
