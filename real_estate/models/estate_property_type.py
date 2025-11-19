from odoo import models, fields

class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Tipo de Propiedad"

    name = fields.Char(string = "Nombre del Tipo", required = True)


