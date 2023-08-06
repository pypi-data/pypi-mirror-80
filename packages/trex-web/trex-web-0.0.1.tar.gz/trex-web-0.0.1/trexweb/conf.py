'''
Created on 7 Apr 2020

@author: jacklok
'''
import logging, os
from flask.helpers import url_for

APPLICATION_NAME                            = 'Penefit'
APPLICATION_TITLE                           = 'Penefit Membership Platform'
APPLICATION_DESC                            = 'Penefit is a platform to let merchant enroll merchants own membership program'
APPLICATION_HREF                            = 'http://localhost.com:8080/'

APPLICATION_SHOW_DASHBOARD_MESSAGE          = False
APPLICATION_SHOW_DASHBOARD_NOTIFICATION     = False


PRODUCTION_MODE                             = "PROD"
DEMO_MODE                                   = "DEMO"
LOCAL_MODE                                  = "LOCAL"


#DEPLOYMENT_MODE                             = PRODUCTION_MODE
#DEPLOYMENT_MODE                             = DEMO_MODE
DEPLOYMENT_MODE                             = LOCAL_MODE

PAYMENT_GATEWAY_APP_KEY                     = ''
PAYMENT_GATEWAY_SECRET_KEY                  = ''

STRIPE_PAYMENT_GATEWAY_APP_KEY              = ''
STRIPE_PAYMENT_GATEWAY_SECRET_KEY           = ''


STRIPE_PAYMENT_GATEWAY_APP_KEY_FOR_LIVE     = 'pk_live_WEshxo5PrfcOyFxSgKskK5pw'
STRIPE_PAYMENT_GATEWAY_SECRET_KEY_FOR_LIVE  = 'sk_live_PEhkanjtcFRsjp7BE1O0mquC00hrYv1gWB'

STRIPE_PAYMENT_GATEWAY_APP_KEY_FOR_TEST     = 'sk_live_uj6BfYx5zQe5zN64A3w48RWJ00U39cP95h'
STRIPE_PAYMENT_GATEWAY_SECRET_KEY_FOR_TEST  = 'sk_test_vLw1amMu58RNWLOvFZMjMl7J00vvGnutd0' 

DEFAULT_CURRENCY_CODE                               = 'myr'
STRIPE_DEFAULT_PAYMENT_METHOD_TYPES                 = ['card','fpx']

FIREBASE_CERT_KEY_FILEPATH                          = None

DATASTORE_SERVICE_ACCOUNT_KEY_FILEPATH              = None

PROJECT_ID                                          = 'penefit-payment-dev'

CSRF_ENABLED                                        = True

CONTENT_WITH_JAVASCRIPT_LINK                        = True
 
AUTHORIZATION_BASE_URL                              = "/sec/oauth2/authorize"
TOKEN_URL                                           = "/sec/oauth2/token"
USERINFO_URL                                        = "/sec/oauth2/userinfo"

DEBUG_MODE                                          = True

FACEBOOK_ACCOUNT_ID                                 = os.environ['FACEBOOK_ID']
FACEBOOK_SECRET_KEY                                 = os.environ['FACEBOOK_SECRET_KEY']

APPLICATION_VERSION_NO                              = "1.0.0"

SIGNIN_URL                                          = 'http://localhost:8081/sec/signin'
#LOGIN_CONTENT_URL_FOR_PATH                          = 'security_bp.signin_content'



DAILY_REPORT_RECEIPIENTS                            = ['sglok@penefit.com']


if DEPLOYMENT_MODE==PRODUCTION_MODE:
    DEBUG_MODE       = False
    #DEBUG_MODE       = True

    #LOGGING_LEVEL    = logging.DEBUG
    #LOGGING_LEVEL    = logging.WARN
    LOGGING_LEVEL    = logging.INFO
    #LOGGING_LEVEL    = logging.ERROR
    
    PAYMENT_GATEWAY_APP_KEY                 = STRIPE_PAYMENT_GATEWAY_APP_KEY_FOR_LIVE
    PAYMENT_GATEWAY_SECRET_KEY              = STRIPE_PAYMENT_GATEWAY_SECRET_KEY_FOR_LIVE
    
    
    
elif DEPLOYMENT_MODE==DEMO_MODE:
    DEBUG_MODE       = True
    #DEBUG_MODE       = False
    
    LOGGING_LEVEL    = logging.DEBUG
    #LOGGING_LEVEL    = logging.INFO
    
    PAYMENT_GATEWAY_APP_KEY                 = STRIPE_PAYMENT_GATEWAY_APP_KEY_FOR_TEST
    PAYMENT_GATEWAY_SECRET_KEY              = STRIPE_PAYMENT_GATEWAY_SECRET_KEY_FOR_TEST
    
elif DEPLOYMENT_MODE==LOCAL_MODE:
    DEBUG_MODE       = True

    LOGGING_LEVEL    = logging.DEBUG
    #LOGGING_LEVEL    = logging.INFO
    
    SIGNIN_URL                              = 'http://localhost:8081/sec/signin'



DEFAULT_ETAG_VALUE                              = '68964759a96a7c876b7e'

DEFAULT_COUNTRY_CODE                            = 'my'

MODEL_CACHE_ENABLED                             = False

INTERNAL_MAX_FETCH_RECORD                       = 9999
MAX_FETCH_RECORD_FULL_TEXT_SEARCH               = 1000
MAX_FETCH_RECORD_FULL_TEXT_SEARCH_PER_PAGE      = 10
MAX_FETCH_RECORD                                = 99999999
MAX_FETCH_IMAGE_RECORD                          = 100
MAX_CHAR_RANDOM_UUID4                           = 20
PAGINATION_SIZE                                 = 2
VISIBLE_PAGE_COUNT                              = 10

GENDER_MALE_CODE                                = 'm'
GENDER_FEMALE_CODE                              = 'f'

API_VERSION                                     = '1.0.0'

APPLICATION_ACCOUNT_PROVIDER                    = 'app'

SUPPORT_LANGUAGES                               = ['en','zh']

#-----------------------------------------------------------------
# Web Beacon settings
#-----------------------------------------------------------------
WEB_BEACON_TRACK_EMAIL_OPEN   = 'eo'

    