from datetime import timedelta, datetime
import base64
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo import api, fields, models
class Travelapi(models.Model):
    _name='personal.front'

    # @api.multi
    def create_test(self):
        self.create_policy({'package':'family','c_name':'ali','add':'50tyri','pass':'8888888888','dob':'2012-01-01','zone':'zone 1','p_from':'2020-01-01','p_to':'2020-01-06','family':[{'name':'mo','dob':'2010-01-01','type':'kid'}],'mail':'eslam3bady@gmail.com'})
    @api.model
    def create_policy(self,data):
        policy_id=self.env['policy.personal'].create({'customer':data.get('c_name'),'national_id':data.get('id'),'job':data.get('job'),'address':data.get('address'),'country_id':data.get('national'),'city':data.get('city'),'covers':[(6,0,data.get('cover'))],'sum_insured':data.get('sum_insured'),'phone':data.get('phone'),'eligible':data.get('elig_bool'),'policy_lang':data.get('language'),'state':'approved'})
        if data.get('othere'):
            for rec in data.get('othere'):
                self.env['eligible.table'].create(
                    {'name': rec['name'], 'mem_perc': rec['rate'], 'relationship': rec['relationship'],
                     'policy_id': policy_id.id})
        # self.env['policy.personal'].search([('id','=',policy_id.id)]).get_financial_data()
        self.env['policy.personal'].search([('id', '=', policy_id.id)]).send_mail_template(data.get('mail'))
        return [policy_id.id,policy_id.policy_num]





