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
    webhook_body = {
        'product_id': product.id,
        'default_code': product.default_code,
        'id_product_madkting': product.id_product_madkting,
        'event': 'stock_update',
        'qty_available': product.qty_available,
        'quantities': product.get_stock_by_location()
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
    logger.info("#### SEND WEBHOOK ####")
    logger.info(data)
    logger.info(url)
    logger.info(headers)
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
