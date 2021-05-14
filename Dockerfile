FROM python:3.9-slim-buster

WORKDIR /rss

ENV TZ=Europe/Paris

COPY requierements.txt requierements.txt
RUN pip install --upgrade pip && pip install -r requierements.txt

COPY . .

EXPOSE 4000

ENTRYPOINT [ "gunicorn" ]
CMD [ "__init__:app", "-b", "0.0.0.0:4000", "-w", "4" ]
