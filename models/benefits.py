from odoo import models, tools, fields, api

class TravelBenefits(models.Model):
    _name = 'travel.benefits'
    cover = fields.Char(string="Cover")
    limit = fields.Char('Limit (USD)')