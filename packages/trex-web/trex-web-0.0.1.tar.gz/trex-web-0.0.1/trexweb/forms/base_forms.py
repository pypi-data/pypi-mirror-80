'''
Created on 22 Apr 2020

@author: jacklok
'''
from wtforms import Form
from wtforms.fields.html5 import DateField
from datetime import datetime
import logging

class ValidationBaseForm(Form):
    
    def create_rest_return_error_message(self):
        error_message_list = []
        for err in self.errors.items():
            logging.debug('err=%s', err)
            error_message = err[1][0]
            error_message_list.append(error_message)
        
        error_message_dict = {'msg': error_message_list}
        
        return error_message_dict
    
    
class DateInputBaseField(DateField):
    def process_formdata(self, valuelist):
        if valuelist:
            date_str = ' '.join(valuelist)
            try:
                self.data = datetime.strptime(date_str, self.format).date()
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('%s is not a valid date value' % (self.label)))    