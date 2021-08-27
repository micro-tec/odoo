# -*- coding: utf-8 -*-
from odoo import tools
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import time
class saleType(models.Model):
    _inherit = 'stock.warehouse'

    as_tienda = fields.Many2one("as.tienda", string="Id Tienda")