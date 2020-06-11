from datetime import timedelta, datetime
import base64
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo import api, fields, models


class RatingTable(models.Model):
    _name = 'cat.table'
    _description = 'Set up Rating tables'
    _rec_name = 'cat_id'

    cat_id=fields.Char('Category Name')
    job_ids=fields.One2many('job.table','category_id',string='Jobs')



# class TravelAgency(models.Model):
#     _name = 'cat.agency'
#     _description = 'Set up Your Travel Agency'
#
#     name = fields.Char('Agency Name', required=True)
#     address = fields.Char('Address')
#     email = fields.Char('Email')
#     phone = fields.Char('Phone Number')
#     mobile = fields.Char('Mobile Number')
#
#
# class AgencyBranch(models.Model):
#     _name = 'agency.branch'
#     _description = 'Set up Your Travel Agency Branch'
#
#     name = fields.Char('Branch Name', required=True)
#     travel_agency = fields.Many2one('travel.agency', 'Travel Agency',required=True)
#     address = fields.Char('Address')
#     email = fields.Char('Email')
#     phone = fields.Char('Phone Number')
#     mobile = fields.Char('Mobile Number')
#
#
# class CertificateBooklet(models.Model):
#     _name = 'certificate.booklet'
#     _description = 'Set up Your Certificate Booklet'
#
#     booklet_num = fields.Char('Booklet Number', required=True)
#     travel_agency = fields.Many2one('travel.agency', 'Travel Agency',required=True)
#     travel_agency_branch = fields.Many2one('agency.branch', 'Agency Branch',
#                                            domain="[('travel_agency','=',travel_agency)]",required=True)
#     serial_from = fields.Integer('Serial From')
#     serial_to = fields.Integer('Serial To')
#
#
# class Users(models.Model):
#     _inherit = 'res.users'
#
#     travel_agency = fields.Many2one('travel.agency', 'Travel Agency')
#     travel_agency_branch = fields.Many2one('agency.branch', 'Agency Branch',
#                                            domain="[('travel_agency','=',travel_agency)]")
#
#     address = fields.Char('Address')
#     phone = fields.Char('Phone Number')
#     mobile = fields.Char('Mobile Number')
#
#
# # class TravelAgencyCommission(models.Model):
# #     _name = 'travel.commission'
# #     _description = 'Set up Your Travel Commissions'
# #
# #     travel_agency = fields.Many2one('travel.agency', 'Travel Agency', required=True)
# #     valid_from = fields.Date('Valid From', default=datetime.today())
# #     valid_to = fields.Date('Valid To', default=datetime.today())
# #     commission = fields.Float('Commission Rate')
#
#
# class NotUsedSerials(models.Model):
#     _name = 'serial.available'
#     _description = 'Get The not used Serial Numbers'
#
#     travel_agency = fields.Many2one('travel.agency', 'Travel Agency', required=True)
#     travel_agency_branch = fields.Many2one('agency.branch', 'Agency Branch',
#                                            domain="[('travel_agency','=',travel_agency)]", required=True)
#     numbers = fields.Char('Serial Numbers Not Used', readonly=True)
#
#     @api.multi
#     def get_not_used_serial(self):
#         serial = self.env['certificate.booklet'].search(
#             [('travel_agency_branch', '=', self.travel_agency_branch.id)])
#
#         records = []
#         for rec in serial:
#             print(111111)
#             deff = rec.serial_to - rec.serial_from
#             print(deff)
#             x = 0
#             for y in range(deff + 1):
#                 ser = rec.serial_from + x
#                 policy = self.env['policy.travel'].search(
#                     [('state', '=', 'approved'), ('serial_no', '=', ser)])
#                 if not policy:
#                     records.append(ser)
#                 y += 1
#                 x += 1
#         print(records)
#         self.numbers = records
#         return {
#             "type": "ir.actions.do_nothing",
#         }
class Jobs(models.Model):
    _name = 'job.table'
    _rec_name = 'job_id'
    job_id=fields.Char('Job Name')
    ar_job_id = fields.Char('Arabic Job Name')
    category_id=fields.Many2one('cat.table',ondelete='cascade')
    condition_ids = fields.One2many('additional.conditions.table', 'condition_id', string='Jobs')

class Covers(models.Model):
    _name = 'cover.table'
    _rec_name = 'cover_id'
    cover_id=fields.Char('Cover Name')
    ar_cover_id = fields.Char('Arabic Cover Name')
    basic=fields.Boolean('Basic')
    taken=fields.Boolean(string='Taken',default=False)
    desc=fields.Text(string='Description')
    ar_desc = fields.Text(string='Arabic Description')

class AdditionalConditions(models.Model):
    _name = 'additional.conditions.table'
    _rec_name = 'condition_id'
    condition = fields.Char('Condition')
    ar_condition = fields.Char('Arabic Condition')
    condition_id = fields.Many2one('job.table', ondelete='cascade')