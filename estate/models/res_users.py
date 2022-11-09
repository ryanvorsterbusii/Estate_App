# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2Many("estate.property", "user_id", string="Properties",
                                   domain=[("state", "in", ["new", "offer_received"])])
