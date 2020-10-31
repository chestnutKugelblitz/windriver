# Alpine Linux is a security-oriented, lightweight Linux distribution
# This image contains a minimal setup
FROM python:3.8-alpine
RUN apk add build-base
# This is my fork of a popular solution for hardening alpine container
ADD https://raw.githubusercontent.com/chestnutKugelblitz/docker-alpine-hardened/master/harden.sh /root/
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
RUN pip install --no-cache-dir gunicorn
RUN chmod 755 /root/harden.sh && /root/harden.sh
RUN mkdir api
COPY windriver-api.yml /app/
COPY utest_windriver-api.py /app/
COPY windriver_api.py /app/
COPY /api/__init__.py /app/api/
COPY /api/string_processing.py /app/api/
CMD ["gunicorn", "-w 3", "-b", "0.0.0.0:8080", "windriver_api:flask_init()"]
