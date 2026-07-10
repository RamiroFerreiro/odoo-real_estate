from odoo import models, fields

class EstatePropertyTag(models.Model):

    _name = "estate.property.tag"
    _description = "Etiqueta de Propiedad"

    # -------------------------------------------------ATRIBUTOS----------------------------------------------------------
    
    name = fields.Char(string = "Nombre de Etiqueta", required = True)

    # ------------------------------------------------- RESTRICCIONES ----------------------------------------------------------
    
    _sql_constraints = [('unique_tag_name','UNIQUE(name)','El nombre de la ETIQUETA debe ser único')]

    