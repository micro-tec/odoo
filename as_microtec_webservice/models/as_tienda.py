# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools

class As_Accionamiento(models.Model):#as_accionamiento
    _name = 'as.tienda'
    _description = "modelo"

    name = fields.Char('Titulo')
    as_nombre_corto = fields.Char('Nombre Corto')
    as_codigo_tienda = fields.Char('Codigo tienda')
    as_direccion = fields.Char('Direccion')
    as_company = fields.Many2one("res.company", string="Compañia")
    active = fields.Boolean(string="Active", default=True,)
    

    