# Comon Sit Ca'teltic Backend
This Django backend is designed to provide an api for the [ComonSitFrontend](https://github.com/comonsit/comonsit-frontend), part of the online micro-loans administration web platform
of [Comon Sit Ca'teltic](https://www.comonsitcateltic.com/), a micro loans organization created by indigenous Tseltal producers located in the northern jungle of Chiapas, part of the  [Yomo A'tel](https://yomolatel.org/)  group.

The project provides api endpoints for:

+ Loan request processes (request, verification and evaluation for approval)
+ Loan administration proviging a summary of each loan and their debts, and mechanisms for extension and forgiveness of interest
+ Payments and the calculation of interest (monthly and daily calculation)
+ Bank reconciliation to match the systems information with the accounting
+ Capital contributions management
+ General information of the users and their communities



## Requirements

Python3 & venv, npm & yarn & postgresql & postgis



### Installation

1. Create and activate virtual Environment

   ```bash
   python3 -m venv env
   source env/bin/activate

2. Install back-end requirements (optional requirementsMAC.txt if needed)

   `pip install -r requirements.txt`

5. Create `/comonSitDjango/comonSitDjango/settings_secret.py` with personal django Secret Key, database information and individual requirements. 

   ```python
   SECRET_KEY = 'someSecretKey!@#'
   
   ALLOWED_HOSTS = ['localhost']
   
   DATABASES = {
       'default': {
           'ENGINE': 'django.contrib.gis.db.backends.postgis',
           'NAME': 'database',
           'USER': 'user',
           'PASSWORD': 'password',
           'HOST': 'localhost',
           'PORT': '',
       }
   }
   
   # optional for some mac environments
   # GDAL_LIBRARY_PATH = '/opt/homebrew/Cellar/gdal/3.4.1_1/lib/libgdal.dylib'
   # GEOS_LIBRARY_PATH = '/opt/homebrew/Cellar/geos/3.10.2/lib/libgeos_c.1.16.0.dylib'
   ```
6. Use a posgrtes database with postgis extension:

   ```
   createdb database
   psql database
   > CREATE EXTENSION postgis;
   ```

7. Make initial migrations and superuser
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```


8. Navigate to [Django Admin](http://localhost:8000/admin/) to create some initial Tsumbalil data: communities, regions and cargos/roles.



### Considerations

The project is specific regarding:

+ Coops involved (coffee, honey, soap and workers)
+ Accounting numbers for reconciliation are specific to comonsitcateltic
