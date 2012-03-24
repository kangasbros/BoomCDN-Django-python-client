# Installation

Install redis:

on recent linux:

sudo aptitude install redis-server

or:

wget http://redis.googlecode.com/files/redis-2.4.9.tar.gz
tar xzf redis-2.4.9.tar.gz
cd redis-2.4.9
make
src/redis-server

then install the python stuff

virtualenv bomb-env
source bomb-env/bin/activate
pip install -r requirements.txt

then set your settings to local_settings.py

cp local_settings_example.py local_settings.py

You need to set 4 parameters:

username="worker2"
profile_uuid="KKb1TGTmmqMK2XKYM34kzc"
clientserver_ip="178.73.194.178"
clientserver_port=12313

then you have to initialize the database

python manage.py syncdb

then start celeryd

python manage.py celeryd

and then start the actual server

python manage.py runserver 0.0.0.0:12313

And now you are done! The client will start replicating files and you will start earning money!

