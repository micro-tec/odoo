# -*- coding: utf-8 -*-
from odoo import tools
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import time
class saleType(models.Model):
    _inherit = 'res.partner'

    as_codigo_microtec = fields.Char('Codigo microtec')
    as_codigo_tienda = fields.Char('Tienda')
    as_tax_partner_id = fields.Many2one('account.tax', string="Taxes")
