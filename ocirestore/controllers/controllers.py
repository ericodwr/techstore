from odoo import http, models, fields
from odoo.http import request
import json


class TechstoreAPI(http.Controller):
    @http.route('/techstoreapi/products', auth='public', method=['GET'])
    def getProducts(self, **kw):
        productslist = request.env['ocirestore.productslist'].search([])
        productsjson = []
        for products in productslist:
            productjson = []
            for product in products.products_ids:
                supplierjson = []
                for supplier in product.supplier_id:
                    supplierjson.append({
                        'brand': supplier.name
                    })
                productjson.append({
                    'name': product.name,
                    'stock': product.stock,
                    'price': product.sell_price,
                    'supplier': supplierjson

                })

            productsjson.append({
                'category': products.name,
                'category_id': products.categories_id,
                'total_products': products.total_products,
                'products': productjson
            })
        return json.dumps(productsjson)
