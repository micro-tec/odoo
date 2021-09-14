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
    def as_crear_venta(self, **post):
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

    @http.route(['/tiamerica/microtec/tienda/<int:tienda_id>','/tiamerica/microtec/tienda'], auth="public", type="json", method=['POST'], csrf=False)
    def as_process_tienda(self, tienda_id=False, **post ):
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
                        "RespMessage":"No se pudo crear la tienda"
                    }
        if not myapikey:
            return error_auth
        user_id = request.env["res.users.apikeys"]._check_credentials(scope="rpc", key=myapikey)
        request.uid = user_id
        res = {}
        callback = post.get('callback')

        if user_id:

            tienda = request.env['as.tienda']
            res = {}

            if tienda_id == False:
                tienda_nueva = tienda.sudo().create(post)
                tienda_id = tienda_nueva.id
                res['id_tienda'] = tienda_id
                res['status'] = 'Creado'
                return '{0}({1})'.format(callback, res)
            else:
                search_tienda = tienda.sudo().search([('id', '=', tienda_id)])
                search_tienda.update(post)
                res['id_tienda'] = search_tienda.id
                res['status'] = 'Actualizado'
                return '{0}({1})'.format(callback, res)

    @http.route(['/tiamerica/microtec/tienda/delete/<int:tienda_id>',], auth="public", type="json", method=['POST'], csrf=False)
    def as_delete_tienda(self, tienda_id=False, **post ):
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
                        "RespMessage":"No se pudo borrar la tienda"
                    }
        if not myapikey:
            return error_auth
        user_id = request.env["res.users.apikeys"]._check_credentials(scope="rpc", key=myapikey)
        request.uid = user_id
        res = {}
        callback = post.get('callback')

        if user_id:
            tienda = request.env['as.tienda']
            res = {}

            if tienda_id == False:
                return '{0}({1})'.format(callback, error_so_create)
            else:
                search_tienda = tienda.sudo().search([('id', '=', tienda_id)])
                search_tienda.update({"active":False})
                res['id_tienda'] = search_tienda.id
                res['status'] = 'Desactivado'
                return '{0}({1})'.format(callback, res)

    @http.route(['/tiamerica/microtec/almacen/<int:almacen_id>','/tiamerica/microtec/almacen'], auth="public", type="json", method=['POST'], csrf=False)
    def as_create_almacen(self, almacen_id=False, **post ):
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
                        "RespMessage":"No se pudo crear el almacen"
                    }
        if not myapikey:
            return error_auth
        user_id = request.env["res.users.apikeys"]._check_credentials(scope="rpc", key=myapikey)
        request.uid = user_id
        res = {}
        callback = post.get('callback')

        if user_id:
            almacen = request.env['stock.warehouse']
            res = {}

            if almacen_id == False:
                almacen_nuevo = almacen.sudo().create(post)
                almacen_id = almacen_nuevo.id
                res['id_almacen'] = almacen_id
                res['status'] = 'Creado'
                return '{0}({1})'.format(callback, res)
            else:
                search_almacen = almacen.sudo().search([('id', '=', almacen_id)])
                search_almacen.update(post)
                res['id_almacen'] = search_almacen.id
                res['status'] = 'Actualizado'
                return '{0}({1})'.format(callback, res)

    @http.route(['/tiamerica/microtec/create_product_category',], auth="public", type="json", method=['POST'], csrf=False)
    def as_crear_categoria_producto(self, **post):
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
            as_product_category = request.env['product.category'].sudo().create(post)
            res['product_category_id'] = as_product_category.id
            res['status'] = 'Categoria de productos creada'
            res_json = json.dumps(res)

            return '{0}({1})'.format(callback, res)

        else:
            return '{0}({1})'.format(callback, error_so_create)

    @http.route(['/tiamerica/microtec/producto/<int:producto_id>','/tiamerica/microtec/producto'], auth="public", type="json", method=['POST'], csrf=False)
    def as_process_producto(self, producto_id=False, **post ):
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
                        "RespMessage":"No se pudo crear el producto"
                    }
        if not myapikey:
            return error_auth
        user_id = request.env["res.users.apikeys"]._check_credentials(scope="rpc", key=myapikey)
        request.uid = user_id
        res = {}
        callback = post.get('callback')

        if user_id:

            producto = request.env['product.template']
            res = {}

            if producto_id == False:
                producto_nueva = producto.sudo().create(post)
                producto_id = producto_nueva.id
                res['id_producto'] = producto_id
                res['status'] = 'Creado'
                return '{0}({1})'.format(callback, res)
            else:
                search_producto = producto.sudo().search([('id', '=', producto_id)])
                search_producto.update(post)
                res['id_producto'] = search_producto.id
                res['status'] = 'Actualizado'
                return '{0}({1})'.format(callback, res)

        else:
            return '{0}({1})'.format(callback, error_so_create)

    @http.route(['/tiamerica/microtec/cliente/<int:cliente_id>','/tiamerica/microtec/cliente'], auth="public", type="json", method=['POST'], csrf=False)
    def as_process_cliente(self, cliente_id=False, **post ):
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
                        "RespMessage":"No se pudo crear el cliente"
                    }
        if not myapikey:
            return error_auth
        user_id = request.env["res.users.apikeys"]._check_credentials(scope="rpc", key=myapikey)
        request.uid = user_id
        res = {}
        callback = post.get('callback')

        if user_id:

            cliente = request.env['res.partner']
            res = {}

            if cliente_id == False:
                cliente_nueva = cliente.sudo().create(post)
                cliente_id = cliente_nueva.id
                res['id_cliente'] = cliente_id
                res['status'] = 'Creado'
                return '{0}({1})'.format(callback, res)
            else:
                search_cliente = cliente.sudo().search([('id', '=', cliente_id)])
                search_cliente.update(post)
                res['id_cliente'] = search_cliente.id
                res['status'] = 'Actualizado'
                return '{0}({1})'.format(callback, res)

        else:
            return '{0}({1})'.format(callback, error_so_create)

    @http.route(['/tiamerica/microtec/create_diario',], auth="public", type="json", method=['POST'], csrf=False)
    def as_crear_diario(self, **post):
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
                        "RespMessage":"No se pudo crear el diario"
                    }
        if not myapikey:
            return error_auth
        user_id = request.env["res.users.apikeys"]._check_credentials(scope="rpc", key=myapikey)
        request.uid = user_id
        res = {}
        callback = post.get('callback')

        if user_id:
            as_diario = request.env['account.journal'].sudo().create(post)
            res['journal_id'] = as_diario.id
            res['status'] = 'Diario creado'
            res_json = json.dumps(res)

            return '{0}({1})'.format(callback, res)

        else:
            return '{0}({1})'.format(callback, error_so_create)

    @http.route(['/tiamerica/microtec/create_factura',], auth="public", type="json", method=['POST'], csrf=False)
    def as_crear_factura(self, **post):
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
                        "RespMessage":"No se pudo crear la factura"
                    }
        if not myapikey:
            return error_auth
        user_id = request.env["res.users.apikeys"]._check_credentials(scope="rpc", key=myapikey)
        request.uid = user_id
        res = {}
        callback = post.get('callback')

        if user_id:

            # invoice = request.env['account.move'].with_context(default_move_type='out_invoice').create(post)
            as_factura = request.env['account.move'].with_context(default_move_type='out_invoice').create(post)
            res['move_id'] = as_factura.id
            res['status'] = 'Factura creada'
            res_json = json.dumps(res)

            return '{0}({1})'.format(callback, res)

        else:
            return '{0}({1})'.format(callback, error_so_create)


