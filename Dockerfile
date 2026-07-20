FROM --platform=linux/amd64 quay.io/jupyter/scipy-notebook:latest

WORKDIR /home/jovyan/work

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
