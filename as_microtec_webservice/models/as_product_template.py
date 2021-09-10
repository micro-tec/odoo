# -*- coding: utf-8 -*-
from odoo import tools
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import time
class saleType(models.Model):
    _inherit = 'product.template'

    as_id_producto_microtec = fields.Char('ID producto microtec')
    as_create_date = fields.Date('Fecha creacion')