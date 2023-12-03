apk add --no-cache expect

expect << EOF
spawn python manage.py createsuperuser --username "$DJANGO_SUPERUSER_USERNAME" --email "$DJANGO_SUPERUSER_EMAIL"
expect "Password:"
send "$DJANGO_SUPERUSER_PASSWORD\r"

expect "Password \(again\):"
send "$DJANGO_SUPERUSER_PASSWORD\r"

expect eof
EOF