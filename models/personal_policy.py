from datetime import timedelta, datetime
import base64
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo import api, fields, models,exceptions
import math
from datetime import date

class TravelPolicy(models.Model):
    _name = 'policy.personal'
    _rec_name = 'policy_num'
    _description = 'Create Your Travel Policies'
    # @api.multi
    @api.model
    def send_mail_template(self,mail):

        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        template_id = self.env.ref('personal_acciedent.email_template_pa')
        template_id.write({'email_to': mail})

        template_id.send_mail(self.ids[0], force_send=True)
        # self.env['mail.template'].browse(template_id.id).send_mail(self.id)

    policy_num = fields.Char(string='Policy Number', required=True, copy=False, index=True,
                             default=lambda self: self.env['ir.sequence'].next_by_code('policy'), readonly=True)
    state = fields.Selection([('pending', 'Pending'),
                              ('approved', 'Approved'),
                              ('canceled', 'Canceled'), ],
                             'Status', required=True, default='pending', copy=False)
    type = fields.Selection([('issue', 'Issue'), ('cancel', 'Cancel')], readonly=True, default='issue')
    issue_date = fields.Date(string='Issue Date', readonly=True, default=datetime.today())
    customer = fields.Char('Insured Name')
    job = fields.Many2one('job.table',string='Customer Job')
    cat_policy = fields.Many2one('cat.table',related='job.category_id')
    policy_lang = fields.Selection([('en', 'English'), ('ar', 'Arabic')],
                                   'Policy Language', required=True, default='ar')
    address = fields.Char('Address')
    # passport_num = fields.Char('PassPort Number')
    expiry_date = fields.Date('Expiration Date', readonly=True, compute='add_year')
    national_id = fields.Char('National ID')
    covers=fields.Many2many('cover.table')
    DOB = fields.Date('Date Of Birth', default=datetime.today())
    age = fields.Integer('Age', readonly=True, compute='compute_age')
    gender = fields.Selection([('m', 'M'), ('f', 'F')])
    phone = fields.Char('phone')

    years = fields.Integer('Period in Years',compute='compute_years', readonly=True)

    currency_id = fields.Many2one("res.currency", "Currency", copy=True,
                                  default=lambda self: self.env.user.company_id.currency_id, readonly=True)
    net_premium = fields.Float('Net Premium', readonly=True, compute='compute_net_premium',store=True)
    sum_insured=fields.Float('Sum Insured')
    user_id = fields.Many2one('res.users', 'User Name', index=True, track_visibility='onchange',
                              default=lambda self: self.env.user, readonly=True)
    cancel_reason = fields.Char('Cancel Reason')
    eligible_ids=fields.One2many('eligible.table','policy_id',string='Eliagibles')

    is_canceled = fields.Boolean(default=False)
    eligible = fields.Boolean(default=True,string='Legal heirs')
    total = fields.Float('Total', readonly=True, compute='get_total',store=True)

    country_id = fields.Selection([('egyptian', 'Egyptian'),
                      ('non_egyptian', 'Non Egyptian'),],
                     'Nationality', required=True, default='egyptian')
    city = fields.Char('Place Of Residence', help='Enter City')

    # @api.one
    @api.onchange('covers')
    def _check_covers(self):
        if self.covers:
            for rec in self.covers:
                if rec.basic:
                    return {'domain': {'covers': [('basic', '=',False )]}}
                else:
                    for rec in self.covers:
                        if rec.basic:
                            return {'domain': {'covers': [('basic', '=', False)]}}

                    return {'domain': {'covers': [(1, '=', 1)]}}
        else:
            return {'domain': {'covers': [(1,'=',1)]}}

            # for record in self.covers:
                    #     if record.basic:
                    #         raise exceptions.ValidationError('Kid Age Must  Be  Less Than 18')

            # if self.age > 18 and self.type == 'kid':

    @api.model
    def get_qouate(self,data):
        if data.get('cover'):
            job=data.get('j')
            price=self.env['personal.price'].search([('date_from','<=',self.issue_date),('date_to','>=',self.issue_date)])

            # for rec in price:
            #     dimensional_stamp = rec.dimensional_stamp
            #     issuing_fees = rec.issuing_fees
            sum = 0
            for rec in price.price_lines.search([('cat','=',self.env['job.table'].search([('id','=',job)]).category_id.id)]):
                for record in data.get('cover'):
                    # for record in record:
                     if record==rec.cover.id:

                        sum+=(rec.rate/1000)

            dimensional_stamp = self.get_dimensional_stamp()
            issuing_fees = self.get_issuing_fees()
            net_prem = sum*data.get('sum_insured')
            proportional_stamp = (net_prem*5)/100
            supervisory_fees = net_prem * (0.6/100)
            policy_holder_protection_fund = net_prem * (0.2/100)
            revising_and_approval_fees = net_prem * (0.1/100)
            fra,res=math.modf(net_prem+proportional_stamp+supervisory_fees+policy_holder_protection_fund+revising_and_approval_fees+dimensional_stamp+issuing_fees)
            return res
    @api.model
    def get_dimensional_stamp(self):
        price = self.env['personal.price'].search(
                [('date_from', '<=', self.issue_date), ('date_to', '>=', self.issue_date)])
        return price.dimensional_stamp

    @api.model
    def get_issuing_fees(self):
        price = self.env['personal.price'].search(
            [('date_from', '<=', self.issue_date), ('date_to', '>=', self.issue_date)])
        return price.issuing_fees

    @api.model
    def get_additional_conditions(self):
        job = self.env['job.table'].search([('id', '=', self.job.id)])
        return job.condition_ids


    # @api.one
    @api.depends('issue_date')
    def add_year(self):
        if self.issue_date:
            # d = datetime.strptime(self.issue_date, '%Y-%m-%d').date()
            self.expiry_date =  self.issue_date.replace(year=self.issue_date.year + 1)


    @api.depends('sum_insured','issue_date', 'job', 'covers')
    def compute_net_premium(self):
        if self.covers and self.sum_insured and self.job and self.covers:
            job = self.job.id
            price = self.env['personal.price'].search(
                [('date_from', '<=', self.issue_date), ('date_to', '>=', self.issue_date)])
            sum = 0
            for rec in price.price_lines.search(
                    [('cat', '=', self.env['job.table'].search([('id', '=', job)]).category_id.id)]):
                for record in self.covers:
                    # for record in record:
                    if record.id == rec.cover.id:
                        sum += (rec.rate / 1000)

            self.net_premium = sum * self.sum_insured



    # @api.one
    @api.depends('issue_date', 'expiry_date')
    def compute_years(self):
        if self.issue_date and self.expiry_date:
            # date1 = datetime.strptime(self.expiry_date, '%Y-%m-%d').date()
            # date2 = datetime.strptime(self.issue_date, '%Y-%m-%d').date()
            difference = relativedelta(self.expiry_date, self.issue_date)
            self.years = difference.years



    @api.depends('sum_insured', 'issue_date', 'job', 'covers')
    def get_total(self):
        if self.covers and self.issue_date and self.sum_insured and self.job:
            result=self.get_qouate({'j':self.job.id,'d':self.DOB,'sum_insured':self.sum_insured,'cover':self.covers.ids})
            self.total=result

    # @api.one
    @api.depends('DOB')
    def compute_age(self):
        if self.DOB:
            # date1 = datetime.strptime(self.issue_date, '%Y-%m-%d').date()
            # date2 = datetime.strptime(self.DOB, '%Y-%m-%d').date()
            difference = relativedelta(self.issue_date, self.DOB)
            age = difference.years
            months = difference.months
            days = difference.days
            if months or days != 0:
                age += 1
            self.age = age





    def confirm_policy(self):
        if self.address and self.customer and self.DOB:
            # serial = self.env['certificate.booklet'].search(
            #     [('travel_agency_branch', '=', self.travel_agency_branch.id)])
            # print(serial)
            # serial2 = self.env['policy.travel'].search(
            #     [('serial_no', '=', self.serial_no), ('id', '!=', self.id)])
            # print(serial2)
            # records = []
            # if serial2:
            #     raise UserError((
            #         "Document Serial Number already exists!"))
            # else:
            #     for rec in serial:
            #         deff = rec.serial_to - rec.serial_from
            #         print(deff)
            #         x = 0
            #         for y in range(deff + 1):
            #             print(11111111111)
            #             ser = rec.serial_from + x
            #             records.append(ser)
            #             y += 1
            #             x += 1
            #     print(records)
            #     if self.serial_no in records:
            #         print(6666666666666)
            self.state = 'approved'
                #     break
                # else:
                #     raise UserError((
                #         "Your Serial Number doesn't match your Branch Serial Numbers "))
        else:
            raise UserError((
                "You Must Enter All The Policy Data"))

#
#
#
# class NewModule(models.Model):
#     _name = 'cancel.policy'
#
#     cancel_reason = fields.Char('Your Cancel Reason')
#
#     @api.multi
#     def cancel_policy(self):
#         context = dict(self._context or {})
#         active_ids = context.get('active_ids', []) or []
#         if self.cancel_reason:
#             for rec in self.env['policy.travel'].search([('id', 'in', active_ids)]):
#                 if  rec.state == 'approved':
#                     rec.create(
#                         {'state': 'canceled', 'policy_num': rec.policy_num, 'issue_date': rec.issue_date,
#                          'type': 'cancel',
#                          'insured': rec.insured, 'address': rec.address, 'serial_no': rec.serial_no,
#                          'passport_num': rec.passport_num, 'DOB': rec.DOB, 'age': rec.age, 'gender': rec.gender,
#                          'coverage_from': rec.coverage_from,
#                          'geographical_coverage': rec.geographical_coverage, 'coverage_to': rec.coverage_to,
#                          'days': rec.days, 'currency_id': rec.currency_id.id, 'net_premium': (rec.net_premium*-1) ,
#                          'proportional_stamp': (rec.proportional_stamp* -1), 'issue_fees': (rec.issue_fees*-1),
#                          'dimensional_stamp': (rec.dimensional_stamp*-1), 'gross_premium': (rec.gross_premium*-1),
#                          'supervisory_stamp': (rec.supervisory_stamp*-1), 'travel_agency': rec.travel_agency.id,
#                          'travel_agency_branch': rec.travel_agency_branch.id, 'user_id': rec.user_id.id,
#                          'travel_agency_comm': (rec.travel_agency_comm*-1), 'net_to_insurer': (rec.net_to_insurer * -1),
#                          'cancel_reason': self.cancel_reason,
#                          'is_editable': False, 'is_canceled': True})
#                     rec.write({'is_canceled': True})
#                 else:
#                     raise UserError((
#                         'This Policy is Approved or Canceled!'))
#
#         else:
#             raise UserError((
#                 'You have to insert your Cancel Reason !'))
#
#         return {'type': 'ir.actions.act_window_close'}


class FamilyAge(models.Model):
    _name = 'eligible.table'


    name=fields.Char('name')
    mem_perc=fields.Char('Percentage')
    relationship = fields.Char('Relationship')
    policy_id=fields.Many2one('policy.personal',ondelete='cascade')