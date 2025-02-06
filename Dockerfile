FROM europe-west2-docker.pkg.dev/ons-sdx-ci/sdx-apps/sdx-gcp:1.4.4
RUN apt-get update && apt-get install -y gnupg
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "./run.py"]
