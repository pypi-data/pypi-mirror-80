'''
Created on 20 Apr 2020

@author: jacklok
'''
import csv, os, json 
from flask import Blueprint, render_template, request, current_app
from trexlib.utils.log_util import get_tracelog
from trexlib.utils.common.cache_util import cache, AGE_TIME_ONE_HOUR 
from trexweb.utils.common.http_response_util import create_cached_response, MINE_TYPE_JSON, MINE_TYPE_JAVASCRIPT
from trexlib.utils.common.common_util import sort_dict_list
from trexmodel.utils.model.model_util import create_db_client
from trexweb.libs.http import StatusCode, create_rest_message
from trexmodel.models.datastore.system_models import ContactUs, Feedback
from trexweb.forms.system_forms import ContactUsForm, FeedbackForm
from trexweb.conf import SIGNIN_URL
from trexmail.mailjet import send_email
from trexmail.conf import DEFAULT_SENDER, DEFAULT_RECIPIENT_EMAIL
import logging
from flask.helpers import url_for



system_bp = Blueprint('system_bp', __name__,
                     template_folder    = 'templates',
                     static_folder      = 'static',
                     url_prefix         = '/system'
                     )


COUNTRY_CODE_FILEPATH = os.path.abspath(os.path.dirname(__file__)) + '/data/countries.csv'  


@system_bp.after_request
def set_system_response_headers(response):
    request_url = request.url
    logging.debug('request_url=%s', request_url)
    
    if request_url.endswith('.js'):
        response.headers['Content-Type'] = MINE_TYPE_JAVASCRIPT
    
    response.charset= 'utf-8'    
    logging.debug('---set_system_response_headers---')
    
    return response

@system_bp.route('/contact-us', methods=['GET'])
def contact_us():
    return render_template("system/contact_us.html", 
                           side_menu_item="contact_us",
                           page_title = "Drop Us a Message",
                           )
    
@system_bp.route('/contact-us-page', methods=['GET'])
def contact_us_page():
    return render_template("system/contact_us_page.html"
                           )    

@system_bp.route('/thank-you-for-contact-us-page', methods=['GET'])
def thank_you_for_contact_us_page():
    return render_template("system/thank_you_for_contact_us_page.html")

@system_bp.route('/thank-you-for-contact-us', methods=['GET'])
def thank_you_for_contact_us():
    return render_template("system/thank_you_for_contact_us.html")


def get_country_list():
    countries_list = []
    
    with open(COUNTRY_CODE_FILEPATH) as csv_file:
        logging.debug('Found country data file')
        data        = csv.reader(csv_file, delimiter=',')
        first_line  = True
        
        
        
        for row in data:
            if not first_line:
                countries_list.append({
                    "cnty_code": row[0],
                    "cnty_name": row[1],
                    "gmt": row[3],
                    "trunk_code": row[4],
                    "cnty_id": row[5],
                    })
            else:
                first_line = False
    
    return sort_dict_list(countries_list, sort_attr_name='cnty_code')


@system_bp.route('/list-country-code', methods=['GET'])
@cache.cached(timeout=50)
def list_country_code_json():
    logging.debug('---list_country_code_json--- ')
    countries_list = get_country_list()
    
    #logging.debug('sorted_countries_list=%s', sorted_countries_list)
    countries_list_in_json  = json.dumps(countries_list, sort_keys = True, separators = (',', ': '))
    
    resp = create_cached_response(countries_list_in_json, 
                                  mime_type=MINE_TYPE_JSON, 
                                  max_age_in_seconds=AGE_TIME_ONE_HOUR
                                  )
    
    return resp

@system_bp.route('/config.js', methods=['GET'])
@cache.cached(timeout=60)
def config():
    logging.debug('############################### config ############################### ')
    
    logging.debug('g = %s ', current_app.config['version_no'])
    
    config_dict = {
                    #"DASHBOARD_URL"         : url_for('main_bp.dashboard_page'),
                    "SIGNIN_URL"            : SIGNIN_URL,
                    "LOADING_IMAGE_PATH"    : url_for('static', filename='custom/img/shared/app-loading.gif'),
                    "LOADING_TEXT"          :'Please wait, your request are processing now', 
                    }
    
    
    return render_template("system/config.js", **config_dict)
    '''
    resp = create_cached_response(config_dict, 
                                  mime_type=MINE_TYPE_JAVASCRIPT, 
                                  max_age_in_seconds=AGE_TIME_ONE_HOUR
                                  )
    
    return resp
    '''

@system_bp.route('/js-i18n.js', methods=['GET'])
def javascript_i18n_message():
    logging.debug('---javascript_i18n_message--- ')
    return render_template("i18n/js_message.js")

@system_bp.route('/contact-us', methods=['post'])
def contact_us_post():
    logging.debug('--- submit contact_us data ---')
    contact_us_data = request.form
    
    logging.debug('contact_us_data=%s', contact_us_data)
    
    contact_us_form = ContactUsForm(contact_us_data)
    
    
    try:
        if contact_us_form.validate():
            
            
            db_client = create_db_client(info=current_app.config['database_config'], caller_info="contact_us_post")
            with db_client.context():
                try:
                    ContactUs.create(
                                    contact_name        = contact_us_form.name.data,
                                    contact_email       = contact_us_form.email.data,
                                    contact_subject     = contact_us_form.subject.data,
                                    contact_message     = contact_us_form.message.data
                                    )
                    
                    contact_us_subject = 'Contact-Us Subject: %s' % contact_us_form.subject.data
                    
                    send_email(sender=DEFAULT_SENDER, 
                               to_address=[DEFAULT_RECIPIENT_EMAIL], 
                               subject=contact_us_subject, 
                               body=contact_us_form.message.data)
                    
                    return create_rest_message('Thank you, we will contact you shortly', status_code=StatusCode.OK)
                
                except:
                    logging.error('Failed to create contact due to %s', get_tracelog())
                    return create_rest_message(status_code=StatusCode.BAD_REQUEST)
            return create_rest_message(status_code=StatusCode.BAD_REQUEST)
        else:
            error_message = contact_us_form.create_rest_return_error_message()
            
            return create_rest_message(error_message, status_code=StatusCode.BAD_REQUEST)
    except:
        logging.error('Fail to contact us due to %s', get_tracelog())
        
        return create_rest_message(status_code=StatusCode.BAD_REQUEST)

@system_bp.route('/feedback', methods=['GET'])
def feedback_form():
    logging.debug('---feedback_form--- ')
    return render_template("system/feedback_form_content.html")

@system_bp.route('/full-modal-example', methods=['GET'])
def full_modal_example():
    return render_template("test/full_modal_example_content.html")
    
@system_bp.route('/feedback', methods=['post'])
def feedback_form_post():
    logging.debug('--- submit feedback_post data ---')
    feedback_data = request.form
    
    logging.debug('feedback_data=%s', feedback_data)
    
    feedback_form = FeedbackForm(feedback_data)
    
    try:
        if feedback_form.validate():
            
            
            db_client = create_db_client(info=current_app.config['database_config'], caller_info="feedback_post")
            with db_client.context():
                try:
                    Feedback.create(
                                    name            = feedback_form.name.data,
                                    email           = feedback_form.email.data,
                                    rating          = feedback_form.rating.data,
                                    message         = feedback_form.message.data
                                    )
                    
                    return create_rest_message('Thank you for you feedback', status_code=StatusCode.OK)
                
                except:
                    logging.error('Failed to create contact due to %s', get_tracelog())
                    return create_rest_message(status_code=StatusCode.BAD_REQUEST)
            return create_rest_message(status_code=StatusCode.BAD_REQUEST)
        else:
            error_message = feedback_form.create_rest_return_error_message()
            
            return create_rest_message(error_message, status_code=StatusCode.BAD_REQUEST)
    except:
        logging.error('Fail to submit feedback due to %s', get_tracelog())
        
        return create_rest_message(status_code=StatusCode.BAD_REQUEST)    



