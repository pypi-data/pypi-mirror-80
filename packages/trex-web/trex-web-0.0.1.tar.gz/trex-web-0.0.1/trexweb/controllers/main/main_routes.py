'''
Created on 15 Apr 2020

@author: jacklok
'''

from flask import Blueprint, render_template
import logging


main_bp = Blueprint('main_bp', __name__,
                     template_folder='templates',
                     static_folder='static',
                     url_prefix='/')

@main_bp.route('/test-home')
def test_home(): 
    #return render_template('main/home.html', navigation_type = 'home',)
    return render_template('test/test_home.html')


@main_bp.route('/')
@main_bp.route('/home')
def home_page(): 
    #return render_template('main/home.html', navigation_type = 'home',)
    return render_template('main/index.html', navigation_type='home')


@main_bp.route('/api-docs')
def api_doc(): 
    return render_template('main/api_docs.html', 
                           navigation_type = 'api-docs',)
    
@main_bp.route('/pricing')
def pricing_page(): 
    return render_template('main/landing/pricing_section_page.html', 
                           navigation_type = 'pricing',)
    
@main_bp.route('/service')
def service_page(): 
    return render_template('main/landing/service_section_page.html', 
                           navigation_type = 'service',)


@main_bp.route('/feature')
def feature_page(): 
    return render_template('main/landing/feature_section_page.html', 
                           navigation_type = 'feature',)                    


@main_bp.route('/contact-us')
def contact_us_page(): 
    return render_template("system/contact_us_page.html")


