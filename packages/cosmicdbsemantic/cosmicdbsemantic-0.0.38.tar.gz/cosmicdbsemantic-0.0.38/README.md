# CosmicDBSemantic Django App

## Install
```
virtualenv demoenv --no-site-packages
demoenv\Scripts\activate
pip install cosmicdbsemantic --no-cache-dir
django-admin startproject demo
```

### Add cosmicdb and requirements to your INSTALLED_APPS setting like this (your app must be first to override)
```
INSTALLED_APPS = (
    'YOURAPPHERE',
    'cosmicdb',
    'crispy_forms',
    'sitetree',
    'django_tables2',
    ... (rest of django apps)
)
```

### Add cosmicdb.urls to your urls.py like this (put cosmicdb urls last)
```
from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    re_path(r'^', include('cosmicdb.urls')),
    path('admin/', admin.site.urls),
]
```

### Add cosmicdb settings to your settings.py like this
```
LANGUAGE_CODE = 'en-au'
COSMICDB_SITE_TITLE = 'Demo Site'
CRISPY_TEMPLATE_PACK = 'semanticui'
CRISPY_ALLOWED_TEMPLATE_PACKS = (CRISPY_TEMPLATE_PACK)
DJANGO_TABLES2_TEMPLATE = 'django_tables2/semantic.html'
COSMICDB_ALLOW_SIGNUP = True
AUTH_USER_MODEL = 'cosmicdb.CosmicUser'
LOGIN_URL = '/login/'
EMAIL_USE_TLS = True
EMAIL_HOST = 'mysmtp.smtp.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'mysmtpuser'
EMAIL_HOST_PASSWORD = 'mysmtppw'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL_NAME = COSMICDB_SITE_TITLE
SITETREE_MODEL_TREE = 'cosmicdb.CosmicDBTree'
SITETREE_MODEL_TREE_ITEM = 'cosmicdb.CosmicDBTreeItem'
```

### Run
```
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

### Load sitetree from site-packages for now
```
python manage.py sitetreeload SITE_PACKAGES_DIR/cosmicdb/treedump.json
```

### Installation Complete!

## See the demo project at https://bitbucket.org/davidbradleycole/demosemantic/src/master/

## Optional

## Custom Semantic UI Themes

### NodeJS (npm)

### Gulp
```
npm install -g gulp
npm install -g gulp-cli
```

### Add NODE_PATH env

### Semantic UI
```
cd PROJECT_DIR\cosmicdb\res\
npm install semantic-ui --save
```

### Put semanticui in semantic
```
cd semantic/
gulp build
```

## Now you can copy your own theme from dist to cosmicdb\static\
```
cd PROJECT ROOT
cp -rf cosmicdb/res/semanticui/semantic/dist cosmicdb/static/cosmicdb/semantic
```

## Site Tree

### Generate sitetree
```
python manage.py sitetreedump > treedump.json
```


## Dev Notes

### adjust cosmicdb/__init__.py for version number
```
rm -rf build
python setup.py sdist bdist_wheel
```
### replace the following line with version number
```
twine upload dist/cosmicdbsemantic-0.0.1*
```
