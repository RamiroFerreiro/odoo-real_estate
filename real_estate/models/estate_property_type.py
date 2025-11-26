from odoo import models, fields

class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Tipo de Propiedad"

    # ------------------------------------------------- RESTRICCIONES ----------------------------------------------------------
    
    _sql_constraints = [('unique_type_name','UNIQUE(name)','El nombre del TIPO de propiedad debe ser único')]

    # -------------------------------------------------ATRIBUTOS----------------------------------------------------------

    name = fields.Char(string = "Nombre del Tipo", required = True)


