
from odoo import models, fields

class AccountMove(models.Model):
    _inherit = "account.move"

    # -------------------------------------------------ATRIBUTOS----------------------------------------------------------

    #Many2one
    property_id = fields.Many2one(comodel_name = "estate.property", string = "Propiedad")