from odoo import models, fields, api
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Oferta sobre propiedades"


    # -------------------------------------------------ATRIBUTOS----------------------------------------------------------

    price = fields.Float(string = "precio", required = True)
    status = fields.Selection(string = "Estado", selection= [("accepted", "Aceptada"),("refused", "Rechazada")])
    validity = fields.Integer(string = "Validez", default = 7)


    # -------------------------------------------------RELACIONES----------------------------------------------------------
    
    #Many2one
    partner_id = fields.Many2one(comodel_name = "res.partner", string = "Ofertante", required = True)
    property_id = fields.Many2one(comodel_name = "estate.property", string = "Propiedad", required = True)
    
    # -------------------------------------------------CAMPOS COMPUTADOS----------------------------------------------------------

    date_deadline = fields.Date(string = "Fecha limite", compute = "_compute_date_deadline", inverse = "_inverse_date_deadline", store = True)
    property_type = fields.Char(string = "Tipo de propiedad", related = "property_id.property_type_id.name", stored = True)


    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:

            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)

            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)


    def _inverse_date_deadline(self):
        for record in self:

            result = None

            if record.create_date and record.date_deadline:
                result = record.date_deadline - record.create_date.date()
                
            elif record.date_deadline:
                result = record.date_deadline - fields.Date.today()  
            
            record.validity = result.days

    # ------------------------------------------------- ACCIONES ----------------------------------------------------------  

    def action_accept_offer(self):

        for record in self:
        
            #Sobre oferta
            self.status = "accepted"

            #Sobre propiedad
            self.property_id.buyer_id = self.partner_id
            self.property_id.selling_price = self.price
            self.property_id.state = "offer_accepted"

            #Rechazar demás ofertas
            other_offers = self.property_id.offer_ids - record
            other_offers.write({"status": "refused"})

        
        return True

    # ------------------------------------------------- RESTRICCIONES ----------------------------------------------------------
    
    _sql_constraints = [('unique_offer', 'UNIQUE(partner_id, property_id)', 'Una persona solo puede realizar una unica oferta por cada propiedad.')]

    

            
