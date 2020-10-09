from odoo import models, tools, fields, api

class PricePersonal(models.Model):
    _name = 'personal.price'
    _description = 'Set up Price tables'
    # currency_id=fields.Many2one('res.currency')
    date_from = fields.Date('From')
    date_to = fields.Date('To')
    dimensional_stamp = fields.Float('Dimensional Stamp')
    issuing_fees = fields.Float('Issuing Fees')

    price_lines=fields.One2many('personal.price.line','p_price_id',string='Prices')

class PersonalPriceTable(models.Model):
    _name = 'personal.price.line'
    cat=fields.Many2one('cat.table')
    cover=fields.Many2one('cover.table')
    rate=fields.Float('Rate')
    p_price_id=fields.Many2one('personal.price',ondelete='cascade')