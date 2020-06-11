from odoo import models, tools, fields, api

class TravelExcess(models.Model):

    _name = 'travel.excess'
    rule = fields.Char(string="Rule")
    amount = fields.Char('Amount')