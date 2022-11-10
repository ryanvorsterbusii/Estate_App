# -*- coding: utf-8 -*-

from odoo import models


class EstateProperty(models.Model):
    _inherit = "estate.property"


def action_sold(self):
    soldaction = super().action_sold()
    journal = self.env["account.journal"].search([("type", "=", "sale")])

    for prop in self:
        self.env["account.move"].create(
            {
                "partner_id": prop.buyer_id.id,
                "move_type": "out_invoice",
                "journal_id": journal.id,
                "invoice_line_ids": [
                    (

                    )
                ]

            }
        )
    return soldaction
