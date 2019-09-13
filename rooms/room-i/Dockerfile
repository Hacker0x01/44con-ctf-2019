FROM python:2

RUN apt-get update && apt-get install -y telnetd inetutils-inetd links
RUN useradd -m -p pa8fg5oAyLo8g user
# user:<none>

RUN pip install requests

WORKDIR /app

ADD requirements.txt /app/

RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN chmod -x /etc/update-motd.d/*
RUN mkdir /home/user/.links2
RUN chmod u+rwx /home/user/.links2
RUN chown user /home/user/.links2

ADD . /app
RUN chmod a+x /app/telnetlogin.sh /app/kickoff.sh
RUN chmod a-rwx /app/main.py
RUN chmod u+rw /app/main.py
RUN chmod 0400 /app/flag

RUN rm /app/requirements.txt

CMD ["/app/kickoff.sh"]
