# Welcome to LocalLibrary
This is a Django Web-Framework Library.
# CREATING VIRTUAL ENVIRONMENT
# windows
py -m venv env
# ACTIVATING ENVIRONMENT
# windows
.\env\Scripts\activate
# PACKAGE INSTALLATION
pip install django
# alternatively python -m pip install django

```
add a gitignore file at same level as env folder
create a new file and name as .env at same level as env folder
copy your SECRET_KEY from settings.py into this .env file. Don't forget to remove quotation marks from SECRET_KEY
```
# install python-decouple iot move SECRET_KEy to .env file
pip install python-decouple
go to settings.py, make amendments below
```python
from decouple import config
SECRET_KEY = config('SECRET_KEY')
```

django-admin --version

django-admin startproject dastugo_locallibrary . 
py manage.py migrate
py manage.py runserver
```
click the link with CTRL key pressed in the terminal and see django rocket.
go to terminal, stop project (CTRL + C), add app
```
py manage.py startapp dastugo_catalog_app
```
go to settings.py and add 'dastugo_catalog_app' app to installed apps and add below lines
```python
import os
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
```

go to terminal
```
pip install pillow  #for images
pip freeze > requirements.txt
py manage.py makemigrations
py manage.py migrate
```

# open admin.py in the catalog application

from .models import Author, Genre, Book, BookInstance

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(BookInstance)

# You can create a "superuser" account that has full access to the site and all needed permissions using manage.py.
py manage.py createsuperuser