'''
Created on 15 May 2020

@author: jacklok
'''

from wtforms import StringField, validators
from wtforms.fields.html5 import DateField
from forms.base_forms import ValidationBaseForm, DateInputBaseField

from datetime import date
import logging 

class MerchantDetailsForm(ValidationBaseForm):
    key                 = StringField('Key')
    company_name        = StringField('Company Name', [
                                        validators.DataRequired(message="Company is required"),
                                        validators.Length(min=3, max=150, message='Full name length must be within 3 and 150 characters')
                                        ]
                                        )
    contact_name        = StringField('Contact Name', [
                                        validators.DataRequired(message="Contact name is required"),
                                        validators.Length(min=3, max=150, message='Contact name length must be within 3 and 150 characters')
                                        ]
                                        )
    mobile_phone        = StringField('Contact Mobile Phone', [
                                        ]
                                        )
    office_phone        = StringField('Contact Office Phone', [
                                        ]
                                        )
    
    email               = StringField('Email Address', [
                                        validators.DataRequired(message="Email is required"),
                                        validators.Length(min=7, max=150, message="Emaill address length must be within 7 and 150 characters"),
                                        validators.Email("Please enter valid email address.")
                                        ]
                                        )
    
    
    
class AddMerchantForm(MerchantDetailsForm):
    plan_start_date     = DateField('Plan Start Date',default=date.today, format='%d/%m/%Y')
    plan_end_date       = DateField('Plan End Date',default=date.today, format='%d/%m/%Y')   
    
    
        
        
        
         