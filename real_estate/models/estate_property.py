from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "propiedad"

    name = fields.Char(string = "titulo", required = True)
    description = fields.Text(string = "descripcion", required = True)
    postcode = fields.Char(string = "Codigo postal")
    date_availability = fields.Date(string = "Fecha Disponibilidad")
    expected_price = fields.Float(string = "Precio esperado")
    selling_price = fields.Float(string = "Precio de venta")
    bedrooms = fields.Integer(string = "Habitaciones", default = 2)
    living_area = fields.Integer(string = "Superficie cubierta")
    facades = fields.Integer(string = "Fachadas")
    garage = fields.Boolean(string = "Garage")
    garden = fields.Boolean(string = "Jardin")
    garden_orientation = fields.Selection(
        selection = [("north","Norte"), ("south", "Sur"), ("east","Este"), ("west","oeste")],
        defaulth = "north", string = "Orientacion del jardin")
    garden_area = fields.Integer(string = "Superficie del jardin")

