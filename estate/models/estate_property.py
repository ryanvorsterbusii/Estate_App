from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "The expected price must be strictly positive"),
        ("check_selling_price", "CHECK(selling_price >= 0)", "The offer price must be positive"),
    ]

    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From", default=lambda
        self: self._default_date_availability(), copy=False)
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", copy=False, readonly=True)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("N", "North"),
            ("S", "South"),
            ("E", "East"),
            ("W", "West"),
        ],
        string="Garden Orientation",
    )

    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
    )
    active = fields.Boolean("Active", default=True)

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    user_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", readonly=True, copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    def _default_date_availability(self):
        return fields.Date.context_today(self) + relativedelta(months=3)

    # Computed Fields for total area and best price

    total_area = fields.Integer(compute="compute_total_area")

    @api.depends("living_area", "garden_area")
    def compute_total_area(self):
        for prop in self:
            prop.total_area = prop.living_area + prop.garden_area

    best_price = fields.Integer(compute="compute_best_price")

    api.depends("offer_ids.price")

    def compute_best_price(self):
        for prop in self:
            prop.best_price = max(prop.offer_ids.mapped("price")) if prop.offer_ids else 0.0

    api.onchange("garden")

    def onchange_garden(self):
        if self.garden:
            self.garden = 10
            self.garden_orientation = "N"
        else:
            self.garden = 0
            self.garden_orientation = False

    def action_sold(self):
        if "canceled" in self.mapped("state"):
            raise UserError("Canceled properties cannot be sold.")
        return self.write({"state": "sold"})

    def action_cancel(self):
        if "sold" in self.mapped("state"):
            raise UserError("Sold properties cannot be canceled.")
        return self.write({"state": "canceled"})