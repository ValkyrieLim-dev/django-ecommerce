import os
from pathlib import Path
import dj_database_url

<<<<<<< HEAD
# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------
# SECURITY & DEBUG
# -------------------------
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'group1-chocodelight.onrender.com'
]

# -------------------------
# INSTALLED APPS
# -------------------------
=======
# --- Base directory ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Security ---
SECRET_KEY = os.environ.get('SECRET_KEY', 'b5ad0b64886295bab64694a2232d1c8c')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'group1-chocodelight.onrender.com']

# --- Installed apps ---
>>>>>>> f5cf99b5d32f306c95c07b04d1b11df2b53c84cd
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
    'cloudinary',
    'cloudinary_storage',  # ✅ Cloudinary app
]

<<<<<<< HEAD
# -------------------------
# MIDDLEWARE
# -------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static files (Render)
=======
# --- Middleware ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # static files on Render
>>>>>>> f5cf99b5d32f306c95c07b04d1b11df2b53c84cd
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -------------------------
# URLS / WSGI
# -------------------------
ROOT_URLCONF = 'shop.urls'
WSGI_APPLICATION = 'shop.wsgi.application'

# -------------------------
# TEMPLATES
# -------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

<<<<<<< HEAD
# -------------------------
# DATABASE (SQLite)
# -------------------------
=======
WSGI_APPLICATION = 'shop.wsgi.application'

>>>>>>> f5cf99b5d32f306c95c07b04d1b11df2b53c84cd
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # This tells Django to use SQLite
        'NAME': BASE_DIR / 'db.sqlite3',         # Path to the SQLite database file
    }
}
<<<<<<< HEAD

# -------------------------
# PASSWORD VALIDATION
# -------------------------
=======
# --- Password validation ---
>>>>>>> f5cf99b5d32f306c95c07b04d1b11df2b53c84cd
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------
# INTERNATIONALIZATION
# -------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_TZ = True

<<<<<<< HEAD
# -------------------------
# STATIC FILES
# -------------------------

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# -------------------------
# MEDIA FILES (LOCAL DEFAULT)
# -------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
=======
# --- Static files ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- Cloudinary storage for media ---
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', 'dwo2okdbu'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY', '415216595646991'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', 'YB9GTKCv9DBgs8j1KKegtBsJvEo'),
}
>>>>>>> f5cf99b5d32f306c95c07b04d1b11df2b53c84cd

# -------------------------
# CLOUDINARY CONFIG
# -------------------------

USE_CLOUDINARY = (
    os.environ.get('CLOUDINARY_CLOUD_NAME') and
    os.environ.get('CLOUDINARY_API_KEY') and
    os.environ.get('CLOUDINARY_API_SECRET')
)

if USE_CLOUDINARY:
    INSTALLED_APPS += ['cloudinary', 'cloudinary_storage']

    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
        'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
        'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
    }

# -------------------------
# DEFAULT PRIMARY KEY FIELD
# -------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
<<<<<<< HEAD

LOGIN_URL = 'store:login'
LOGIN_REDIRECT_URL = 'store:product_list'
LOGOUT_REDIRECT_URL = 'store:login'

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "store/static",
]
=======
>>>>>>> f5cf99b5d32f306c95c07b04d1b11df2b53c84cd
