FROM python:2

RUN apt-get update && apt-get install -y openssh-server telnetd
RUN mkdir /var/run/sshd
RUN useradd -m -p pa1IK8JGvLMjY eldon
# eldon:chess
RUN useradd -m -p pa8fg5oAyLo8g guest
# guest:<none>
RUN apt-get install -y docker.io inetutils-inetd telnet

RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
RUN usermod --shell /app/main.py eldon
RUN usermod --shell /app/main.py guest
RUN usermod eldon -aG docker
RUN chmod -x /etc/update-motd.d/*
RUN rm /etc/issue /etc/issue.net /etc/motd

WORKDIR /app

ADD requirements.txt /app/

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ADD . /app
RUN chmod a+x /app/main.py /app/telnetlogin.sh /app/kickoff.sh

CMD ["/app/kickoff.sh"]
