#!/bin/bash

cp /app/issue /etc/issue
cp /app/issue /etc/issue.net
rm issue
chmod -x /etc/update-motd.d/*
chmod 0777 /var/run/docker.sock
/usr/sbin/inetutils-inetd -d /app/inetd.conf
