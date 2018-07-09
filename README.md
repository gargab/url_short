# URL shortener

This is a Rest framework based Django app.<br />
You need to have the following on your system before you can run the app :<br />
Python2<br />
Postgres<br />
Anaconda<br />

1. Once these are installed:<br />
i) setup python2 based virtual environment in Anaconda<br />
ii) conda activate 'Virtual_env_name'<br />

2. Create a Database in Postgres under a particular user<br />
i) in settings.py file in zomato_main edit the database config:<br />

DATABASES = {  ####Give your own db configurations<br />
    'default': {#        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.#<br />        
    'NAME': #'db_calypso',                      # Or path to database file if using sqlite3.<br />
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.<br />
        #        'NAME': #'db_calypso',                      # Or path to database file if using sqlite3.<br />
        'NAME': 'url_short',                      # Or path to database file if using sqlite3.<br />
        'USER': 'vagrant',                      # Not used with sqlite3.<br />
        'PASSWORD': 'admin',                  # Not used with sqlite3.<br />
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.<br />
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.<br/>
    }<br />
}<br />

ii) In root directory run:<br />
python manage.py shell<br />
from django.contrib.auth.models import User;<br />
User.objects.create_superuser('{username}', '{email}', '{password}');<br />


3. First start the rest server using command:<br />
gunicorn main_app.wsgi --workers 2 --timeout 10000 --bind 0.0.0.0:8000  (If on Unix based system)<br />

else  (If on Windows system)<br/>
python manage.py runserver<br/>


4. Once the Server is up you can POST to:<br/>
http://localhost:8000/create_url/ <br/>

JSON structure <br/>
{"url":"https://www.fabric.io/gameberrylabs/android/apps/com.boardgame.rent.business.landlord/issues?time=last-seven-days&event_type=crash&subFilter=state&state=open&build%5B0%5D=top-builds","created_by":"user1","expiry":"1000","allowed_users":"user1,user2", "short_url":"abcv"}<br/>

expiry is optional: default is 10 sec, also the value of this paramter should be an integer in sec. <br/>
allowed_users is optional: list of allowed users<br/>
short_url is optional: used to give custom URL<br/>

and create a URL for shortening. It returns the shortened URL as well<br />

5.  Now, if the shortened URL is http://localhost:8000/B/short_url/ <br/>
You can directly get it if its public <br/>
Else if it is private, You will have to give user as the query parameter like this: <br/>
http://localhost:8000/B/short_url/?user=user1<br/>

6. You can go to http://localhost:8000/abcv/get_stats/ to track the usage of particular URL <br />

7. To see the DB, there is an admin platform. You can go to http://localhost:8000/admin/<br/>
The username and password are ones you created in step 2 part (ii) <br/>
This will open a basic Django CRUD App <br/>

P.S.- A better access control could be implemented for the users using some token based system but that would be a lot of heavy lifting for the given scope.<br/>

# Approach:
The project follows Rest framework. This approach was followed basically to make flexible microservices which can later on serve various platforms.<br />
To look at it from scaling perspective, I am using gunicorn and deploying multiple workers in addition, the shortened URLs are directly stored in DB for fast access.
All the additional features have also been implemented.<br/>

Finally, I have used BASE62 encoding to shorten URLs. The approach basically is to encode the DB id's of URLs to BASE62. BASE62 because a total 0f 62 characters can be used to create URLs in all.<br />
There is just one table for simplicity<br/>

One important thing to note is if a user creates his/her custom URL that clashes with current short URL or in future may clash with short URL. The URL created latest will be given proprity assuming old may have expired or will expire sooner. This is not the best approach sth. can be done in case of collisions like not giving the URL if it is a clash or giving the next hash in case of clash. As the scope for this app was limited, I have not implemented this technique. <br/>
The short URL structure is http://localhost:8000/{BASE62Encoding}/short_url/<br/>
The get Stats URL structure is http://localhost:8000/{BASE62Encoding}/get_stats/<br/>
