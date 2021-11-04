# -*- coding: utf-8 -*-
from odoo import tools
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import time
class saleType(models.Model):
    _inherit = 'purchase.order'

    as_referencia_micotec = fields.Char('Referencia microtec')