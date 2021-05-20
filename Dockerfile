FROM tiangolo/uvicorn-gunicorn:python3.8
RUN apt-get update && apt-get install -y gnupg
COPY . /app
WORKDIR /app
RUN python -m pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
CMD ['uvicorn', 'app.routes:app', '--host', '0.0.0.0', '--port', '5000', '--workers', '2', '--timeout-keep-alive', '600']
