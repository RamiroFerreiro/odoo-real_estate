from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Oferta sobre propiedades"


    # -------------------------------------------------ATRIBUTOS----------------------------------------------------------

    price = fields.Float(string = "precio", required = True)
    status = fields.Selection(string = "Estado", selection= [("accepted", "Aceptada"),("refused", "Rechazada")])

    # -------------------------------------------------RELACIONES----------------------------------------------------------
    
    #Many2one
    partner_id = fields.Many2one(comodel_name = "res.partner", string = "Ofertante", required = True)
    property_id = fields.Many2one(comodel_name = "estate.property", string = "Propiedad", required = True)
    