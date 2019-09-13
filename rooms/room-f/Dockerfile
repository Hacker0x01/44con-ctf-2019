FROM python:2

RUN apt-get update && apt-get install -y telnetd inetutils-inetd links
RUN useradd -m -p pa8fg5oAyLo8g user
# user:<none>

RUN pip install requests

WORKDIR /app

#ADD requirements.txt /app/

#RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN chmod -x /etc/update-motd.d/*

ADD . /app
RUN gcc -fno-stack-protector -z execstack -o /app/main -g /app/main.c
RUN rm /app/main.c
RUN chmod a+x /app/telnetlogin.sh /app/kickoff.sh /app/main
RUN chmod a-rwx /app/flag
RUN chmod u+r /app/flag
RUN chown user /app/message
RUN chmod a-rwx /app/message
RUN chmod u+s /app/main

CMD ["/app/kickoff.sh"]
