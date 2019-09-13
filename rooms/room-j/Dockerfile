FROM python:2

RUN apt-get update && apt-get install -y telnetd inetutils-inetd links
RUN useradd -m -p pa8fg5oAyLo8g user
# user:<none>

RUN pip install requests

WORKDIR /app

#ADD requirements.txt /app/

#RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install pycrypto

RUN chmod -x /etc/update-motd.d/*

ADD . /app
RUN gcc -fno-stack-protector -z execstack -o /app/main -g /app/main.c
RUN rm /app/main.c
RUN chmod a+x /app/telnetlogin.sh /app/kickoff.sh /app/main
RUN chmod a-r /app/main
RUN chmod u+sr /app/main
RUN chmod 0400 /app/rmain.py
RUN chmod 0600 /app/key

CMD ["/app/kickoff.sh"]
