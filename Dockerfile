FROM python:3.10

ENV AZURE_CLIENT_ID=""
ENV AZURE_CLIENT_SECRET=""
ENV AZURE_TENANT_ID=""

WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN pip install -e . 

ENTRYPOINT ["gunicorn"]
CMD ["src.fastapi_photo.app:app"]