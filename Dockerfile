FROM python:3.9-slim-buster

WORKDIR /rss
ENV TZ=Europe/Paris

RUN pip install --upgrade pip && pip install flask PyYAML torrentool

COPY . .

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD [ "main.py" ]