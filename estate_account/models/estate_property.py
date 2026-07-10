from odoo import models
from odoo import Command 

class EstateProperty(models.Model):
    _inherit = "estate.property"

    # -------------------------------------------------REDEFINICION----------------------------------------------------------

    def action_mark_as_sold(self):

        for record in self:
            self.env["account.move"].create({
                "property_id": record.id,
                "partner_id":record.buyer_id.id,
                "move_type":"out_invoice",
                "line_ids":[
                    
                    Command.create({
                        "name": record.name,
                        "quantity": 1,
                        "price_unit": record.selling_price 
                    }),

                    Command.create({
                        "name": "Gastos administrativos",
                        "quantity": 1,
                        "price_unit": 100
                    })

                ],

            })
            
        return super().action_mark_as_sold() 

    