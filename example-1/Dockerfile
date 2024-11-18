FROM python:3.11

WORKDIR /app

RUN apt-get -y update && apt-get -y install socat

RUN useradd ctf

COPY hello.py .

RUN chown -R ctf:ctf /app

USER ctf

EXPOSE 8000

CMD ["socat", "-T60", "TCP-LISTEN:8000,reuseaddr,fork", "EXEC:python3 hello.py"]
