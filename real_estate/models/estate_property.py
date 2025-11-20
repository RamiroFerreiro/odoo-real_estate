from odoo import models, fields
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "propiedad"

    # -------------------------------------------------ATRIBUTOS----------------------------------------------------------

    name = fields.Char(string = "titulo", required = True)
    description = fields.Text(string = "descripcion", required = True)
    postcode = fields.Char(string = "Codigo postal")
    date_availability = fields.Date(string = "Fecha Disponibilidad", copy = False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(string = "Precio esperado")
    selling_price = fields.Float(string = "Precio de venta", copy = False)
    bedrooms = fields.Integer(string = "Habitaciones", default = 2)
    living_area = fields.Integer(string = "Superficie cubierta")
    facades = fields.Integer(string = "Fachadas")
    garage = fields.Boolean(string = "Garage")
    garden = fields.Boolean(string = "Jardin")

    garden_orientation = fields.Selection(
        selection = [("north","Norte"), ("south", "Sur"), ("east","Este"), ("west","oeste")],
        defaulth = "north", string = "Orientacion del jardin")
    garden_area = fields.Integer(string = "Superficie del jardin")

    state = fields.Selection(string = "estado", 
        selection = [("new","Nuevo"), ("offer_received", "Oferta Recibida"), ("offer_accepted","Oferta Aceptada"), ("sold","vendido"), ("canceled", "cancelado")],
        required = True,
        default = "new",
        copy = False)

    # -------------------------------------------------RELACIONES----------------------------------------------------------
    
    #Many2one
    property_type_id = fields.Many2one(comodel_name = "estate.property.type", string = "Tipo de Propiedad")
    buyer_id = fields.Many2one(comodel_name = "res.partner", string = "Comprador")
    salesman_id = fields.Many2one(comodel_name = "res.users", string = "Vendedor", copy = True, default = lambda self: self.env.user)

    #Many2many
    tag_ids = fields.Many2many(comodel_name = "estate.property.tag", string = "Etiquetas")

    #One2many
    offer_ids = fields.One2many(comodel_name = "estate.property.offer", inverse_name = "property_id", string = "Ofertas")
    
    