#!/bin/bash

cp /app/issue /etc/issue
cp /app/issue /etc/issue.net
rm issue
mv /app/inetd.conf /etc/inetd.conf
mv /app/telnetlogin.sh /
rm kickoff.sh Dockerfile
/usr/sbin/inetutils-inetd -d /etc/inetd.conf
