pip freeze > requirements.txt
python manage.py makemigrations
python manage.py migrate
## يستخدم في حالة اذا كانت الترجمة موجودة و gettext
#python manage.py makemessages -l ar
#python manage.py compilemessages
python manage.py runserver
