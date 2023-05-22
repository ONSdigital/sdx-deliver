FROM eu.gcr.io/ons-sdx-ci/sdx-gcp:1.2.3
RUN apt-get update && apt-get install -y gnupg
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "./run.py"]
