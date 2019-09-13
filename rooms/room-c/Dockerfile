FROM python:2

RUN apt-get update && apt-get install -y telnetd inetutils-inetd links
RUN useradd -m -p pa8fg5oAyLo8g user
# user:<none>

RUN pip install requests

WORKDIR /app

#ADD requirements.txt /app/

#RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN usermod --shell /app/main.py user

RUN chmod -x /etc/update-motd.d/*

ADD . /app
RUN chmod a+x /app/telnetlogin.sh /app/kickoff.sh /app/main.py

CMD ["/app/kickoff.sh"]
