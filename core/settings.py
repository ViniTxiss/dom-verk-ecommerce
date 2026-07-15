"""
DOM VERK — Django Settings
"""

import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-me')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,.railway.app,.up.railway.app').split(',')
RAILWAY_PUBLIC_DOMAIN = os.getenv('RAILWAY_PUBLIC_DOMAIN')
if RAILWAY_PUBLIC_DOMAIN and RAILWAY_PUBLIC_DOMAIN not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RAILWAY_PUBLIC_DOMAIN)

CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'https://*.up.railway.app',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]
for host in ALLOWED_HOSTS:
    host_clean = host.strip()
    if host_clean and host_clean not in ('localhost', '127.0.0.1', '*'):
        origin = f'https://{host_clean}' if not host_clean.startswith('http') else host_clean
        if origin not in CSRF_TRUSTED_ORIGINS:
            CSRF_TRUSTED_ORIGINS.append(origin)

# Informa ao Django que o Railway lida com SSL no proxy reverso
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party
    'django_extensions',
    'encrypted_model_fields',
    'axes',
    # Local apps
    'apps.products',
    'apps.cart',
    'apps.orders',
    'apps.accounts',
    'apps.dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'axes.middleware.AxesMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.cart.context_processors.cart_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database — usa DATABASE_URL em produção (Railway PostgreSQL), SQLite localmente
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Auth
AUTH_USER_MODEL = 'accounts.CustomUser'
LOGIN_URL = '/conta/entrar/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Cart session key
CART_SESSION_ID = 'cart'

# ── Segurança HTTP ──────────────────────────────────────────────────────────
# Cabeçalhos ativos em TODOS os ambientes
X_FRAME_OPTIONS = 'SAMEORIGIN'            # Permite framing na mesma origem
SECURE_CONTENT_TYPE_NOSNIFF = True        # Anti-MIME sniffing
SECURE_BROWSER_XSS_FILTER = True          # XSS filter (legado, mantido para suporte)

# Configurações APENAS para produção (quando DEBUG=False)
if not DEBUG:
    SECURE_SSL_REDIRECT = True            # Redireciona HTTP → HTTPS
    SECURE_HSTS_SECONDS = 31536000        # HSTS por 1 ano
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True          # Cookie de sessão apenas via HTTPS
    CSRF_COOKIE_SECURE = True             # Cookie CSRF apenas via HTTPS

# Cookies seguros em todos os ambientes
SESSION_COOKIE_HTTPONLY = True            # JS não acessa cookie de sessão
SESSION_COOKIE_AGE = 7200                 # Sessão expira em 2 horas

# ── Criptografia de campos sensíveis (LGPD — M3) ─────────────────────────────
FIELD_ENCRYPTION_KEY = os.getenv('FIELD_ENCRYPTION_KEY') or 'kyrW-pP3FOT3DmLRFakZ7Urv39wIHErjkd4ZINIg12k='

# ── django-axes — Rate Limiting de Login (B1) ─────────────────────────────────
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AXES_FAILURE_LIMIT = 5              # Bloqueia após 5 tentativas falhas
AXES_COOLOFF_TIME = 1               # Período de bloqueio: 1 hora
AXES_LOCKOUT_PARAMETERS = ['ip_address', 'username']  # Bloqueia por IP + usuário
AXES_RESET_ON_SUCCESS = True        # Reseta contagem após login bem-sucedido
AXES_ENABLE_ADMIN = True            # Exibe tentativas no Django Admin
AXES_VERBOSE = False                # Não polui os logs em produção
AXES_LOCKOUT_TEMPLATE = 'accounts/lockout.html'  # Template de feedback amigável

