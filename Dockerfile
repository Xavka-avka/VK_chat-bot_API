FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py", "--host=0.0.0.0"]