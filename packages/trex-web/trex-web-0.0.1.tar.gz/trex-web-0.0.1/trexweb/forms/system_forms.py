'''
Created on 29 Apr 2020

@author: jacklok
'''
from wtforms import StringField, validators
from trexweb.forms.base_forms import ValidationBaseForm

class ContactUsForm(ValidationBaseForm):
    name                = StringField('Contact name', [
                                        validators.DataRequired(message="Contact name is required"),
                                        validators.Length(min=3, max=200, message='Contact name length must be within 3 and 200 characters')
                                        ]
                                        )
    email               = StringField('Email Address', [
                                        validators.DataRequired(message="Email is required"),
                                        validators.Length(min=7, max=150, message="Emaill address length must be within 7 and 150 characters"),
                                        validators.Email("Please enter valid email address.")
                                        ]
                                        )
    subject             = StringField('Subject', [
                                        validators.Length(max=300, message="Subject length must not more than 300 characters")
                                        ]
                                        )
    
    message             = StringField('Message', [
                                        validators.Length(max=3000, message="Message length must not more than 3000 characters")
                                        ]
                                        )
    
class FeedbackForm(ValidationBaseForm):
    name                = StringField('Person name', [
                                        validators.DataRequired(message="Person name is required"),
                                        validators.Length(min=3, max=150, message='Person name length must be within 3 and 150 characters')
                                        ]
                                        )
    email               = StringField('Email Address', [
                                        validators.DataRequired(message="Email is required"),
                                        validators.Length(min=7, max=150, message="Emaill address length must be within 7 and 150 characters"),
                                        validators.Email("Please enter valid email address.")
                                        ]
                                        )
    rating               = StringField('Rating', [
                                        validators.DataRequired(message="Rating is required"),
                                        
                                        ]
                                        )
    message             = StringField('Message', [
                                        validators.Length(max=100, message="City length must not more than 1000 characters")
                                        ]
                                        )    