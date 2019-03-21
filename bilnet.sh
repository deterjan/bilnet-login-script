#!/bin/bash

STUDENT_ID=""
PASSWORD=""

COOKIE_REQUEST=$(curl -s -c - 'https://auth.bilkent.edu.tr/auth/login?next=%2Fauth%2Fstatus')

LINE=$(echo "$COOKIE_REQUEST" | grep 'bilnet-user')
COOKIE=$(echo $LINE | cut -d ' ' -f7)

LOGIN_REQUEST_1="curl 'https://auth.bilkent.edu.tr/auth/login' -H 'Upgrade-Insecure-Requests: 1' -H 'Cookie: bilnet-user="
LOGIN_REQUEST_2="' --data 'next=%2Fauth%2Fstatus&UserName=$STUDENT_ID&Password=$PASSWORD&agree=on' --compressed"
FULL_LOGIN_REQUEST="$LOGIN_REQUEST_1$COOKIE$LOGIN_REQUEST_2"

RESPONSE=$(eval "$FULL_LOGIN_REQUEST" 2> /dev/null) # discard curl's output to stderr

if [ "$RESPONSE" == "" ]; then
   echo Login successful.
else
   echo Login failed.
fi
