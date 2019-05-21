# set FLASK_APP=app.py # for windows
export FLASK_APP=app.py # for linux
#set FLASK_ENV=development
export FLASK_ENV=development

ip_address=$(ifconfig eth0 | awk 'NR==2' | awk '{print $2}')
echo $ip_address

python -m flask run
