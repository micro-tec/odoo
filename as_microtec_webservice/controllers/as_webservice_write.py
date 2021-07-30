# -*- coding: utf-8 -*-
from odoo.tools.translate import _
from odoo import http
from odoo import http
from odoo.http import request
from datetime import datetime
from bs4 import BeautifulSoup
import json
import sys
import uuid
from odoo import http
from odoo.http import request, Response
from odoo.tests import tagged, Form

import json
import yaml
import requests, json
import logging
_logger = logging.getLogger(__name__)
from datetime import timedelta, datetime, date
import calendar
from dateutil.relativedelta import relativedelta
import os.path

class as_webservice_microtec(http.Controller):

    @http.route(['/tiamerica/microtec/create_sale',], auth="public", type="json", method=['POST'], csrf=False)
    def crear_factura_proveedor(self, **post):
        """ 
            tokedev: 4761b5d3f6474d1da7a6db5be87a097b34a67a42
            prod: 112cbd5cbeff3cae4c162847d18c997d4d9a7481
            http://10.0.10.66:14001/tiamerica/microtec/create_sale
        """
        post = request.jsonrequest

        myapikey = request.httprequest.headers.get("Authorization")
        error_auth = {			
                        "RespCode":-1,
                        "RespMessage":"Authorization no esta presente en el header"
                    }
        error_so_create = {			
                        "RespCode":-1,
                        "RespMessage":"No se pudo crear la venta"
                    }
        if not myapikey:
            return error_auth
        user_id = request.env["res.users.apikeys"]._check_credentials(scope="rpc", key=myapikey)
        request.uid = user_id
        res = {}
        callback = post.get('callback')

        if user_id:
            as_nueva_venta = request.env['sale.order'].sudo().create(post)
            res['sale_order_id'] = as_nueva_venta.id
            res['sale_order_name'] = as_nueva_venta.name
            res['status'] = 'Venta Creada'
            # res_json = json.dumps(res)

            #confirmar venta
            as_nueva_venta.action_confirm()

            #confirmar movimiento de inventario
            for picking in as_nueva_venta.picking_ids:
                wiz = picking.button_validate()
                wiz = Form(request.env['stock.immediate.transfer'].with_context(wiz['context'])).save()
                wiz.process()
                #picking.action_confirm() probar si es que no esta en confirmado
                # picking.action_assign()
                # picking.button_validate()
                # self.env['stock.immediate.transfer'].create({'pick_ids': [(4, picking.id)]}).process()

            return '{0}({1})'.format(callback, res)

        else:
            return '{0}({1})'.format(callback, error_so_create)
        

