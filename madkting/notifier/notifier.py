from odoo.api import Environment
from ..log.logger import logger
import requests
import json


def send_stock_webhook(env, product_id, hook_id=None):
    """
    TODO: register webhook failures in order to implement "retries"
    :param env:
    :type env: Environment
    :param product_id:
    :type product_id: int
    :param hook_id:
    :type hook_id: int
    :return:
    """
    product = env['product.product'].search([('id', '=', product_id)], limit=1)

    if hook_id:
        webhook_suscriptions = env['madkting.webhook'].search([('id', '=', hook_id)])
    else:
        webhook_suscriptions = env['madkting.webhook'].search([
            ('hook_type', '=', 'stock'),
            ('active', '=', True)
        ])

    config = env['madkting.config'].sudo().get_config()

    if config and config.stock_quant_available_quantity_enabled:
        ubicaciones_stock = {}
        if config.stock_source:            
            for branch_id in config.stock_source.split(','):
                location = env['stock.location'].search([('id', '=', int(branch_id))], limit=1)
                qty_in_branch = env['stock.quant']._get_available_quantity(product, location)
                ubicaciones_stock.update({branch_id : qty_in_branch})
        else:
            for branch_id, stock in product.get_stock_by_location().items():
                location = env['stock.location'].search([('id', '=', int(branch_id))], limit=1)
                qty_in_branch = env['stock.quant']._get_available_quantity(product, location)
                ubicaciones_stock.update({branch_id : qty_in_branch})
    else:
        ubicaciones_stock = product.get_stock_by_location()
        
    webhook_body = {
        'product_id': product.id,
        'default_code': product.default_code,
        'id_product_madkting': product.id_product_madkting,
        'event': 'stock_update',
        'qty_available': product.qty_available,
        'quantities' : ubicaciones_stock
        # 'quantities': product.get_stock_by_location()
    }
    data = json.dumps(webhook_body)
    headers = {'Content-Type': 'application/json'}
    for webhook in webhook_suscriptions:
        """
        TODO: if the webhook fails store it into a database for retry implementation
        """
        success = send_webhook(webhook.url, data, headers)


def send_webhook(url, data, headers):
    """
    :param url:
    :param data:
    :param headers:
    :return:
    """
    logger.debug("#### SEND WEBHOOK ####")
    logger.debug(data)
    logger.debug(url)
    logger.debug(headers)
    try:
        response = requests.post(url, data=data, headers=headers)
    except Exception as ex:
        logger.exception(ex)
        return False
    else:
        if not response.ok:
            logger.error(response.text)
            return False
        return True
