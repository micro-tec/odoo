# -*- coding: utf-8 -*-
from odoo import tools
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import time
class saleType(models.Model):
    _inherit = 'account.move.line'

    as_discount_2 = fields.Float('Descuento 2')
    as_discount_3 = fields.Float('Descuento 3')