# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning, ValidationError, UserError
from datetime import date, datetime, timedelta
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    state = fields.Selection(selection_add=[
        ('packed', 'Packed'),
        ('arriving', 'Arriving'),
        ('delivered', 'Delivered'),
        ('cancel',)])
    date_packed = fields.Datetime(string='Packed Date', readonly=True, copy=False)
    date_arrive = fields.Datetime(string='Arrive Date', readonly=True, copy=False)
    date_deliver = fields.Datetime(string='Deliver Date', readonly=True, copy=False)
    receiver_id = fields.Many2one('res.users', 'Received By', readonly=True, copy=False, track_visibility='onchange')
    digital_signature = fields.Binary(string="Signature")
        
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for so in self:
            so.write({'receiver_id': self.env.uid})
        return res
            
    def action_sales_packed(self):
        self.write({
            'state': 'packed',
            'date_packed': fields.Datetime.now()
        })
            
    def action_sales_arriving(self):
        self.write({
            'state': 'arriving',
            'date_arrive': fields.Datetime.now()
        })
            
    def action_sales_delivered(self):
        self.write({
            'state': 'delivered',
            'date_deliver': fields.Datetime.now()
        })                            
    
