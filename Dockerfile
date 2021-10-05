FROM python:3
copy . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV FLASK_APP=app
ENTRYPOINT [ "flask", "run"]