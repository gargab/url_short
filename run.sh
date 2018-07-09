#!binsh
echo "------ Starting APP ------"
USER="abhinavGarg"
MAIL="abh.garg@example.com"
PASS="main_appapis"

if [-z $VCAP_APP_PORT];
	then SERVER_PORT=5000;
	else SERVER_PORT=$VCAP_APP_PORT;
fi

echo ------ Create database tables ------
python manage.py makemigrations shorterning_app
python manage.py migrate --noinput

echo "from django.contrib.auth.models import User; User.objects.create_superuser('${USER}', '${MAIL}', '${PASS}')" | python manage.py shell

echo ------Starting server ------
#python manage.py runserver 0.0.0.0:$SERVER_PORT --noreload
#gunicorn main_app.wsgi --workers 2 --timeout 10000 --bind 0.0.0.0:8000
