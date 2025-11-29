from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
import random
from odoo import Command


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
        default = "north", string = "Orientacion del jardin")
    
    garden_area = fields.Integer(string = "Superficie del jardin")

    state = fields.Selection(
        string = "estado", 
        selection = [("new","Nuevo"), ("offer_received", "Oferta Recibida"), ("offer_accepted","Oferta Aceptada"), ("sold","vendido"), ("canceled", "cancelado")],
        required = True,
        default = "new",
        copy = False)

    # -------------------------------------------------RELACIONES----------------------------------------------------------
    
    #Many2one
    property_type_id = fields.Many2one(comodel_name = "estate.property.type", string = "Tipo de Propiedad")
    buyer_id = fields.Many2one(comodel_name = "res.partner", string = "Comprador")
    salesman_id = fields.Many2one(comodel_name = "res.users", string = "Vendedor", copy = True, default = lambda self: self.env.user)
    offer_partner_ids = fields.Many2one(string = "Personas que ofertaron", related = "")

    #Many2many
    tag_ids = fields.Many2many(comodel_name = "estate.property.tag", string = "Etiquetas")

    #One2many
    offer_ids = fields.One2many(comodel_name = "estate.property.offer", inverse_name = "property_id", string = "Ofertas")
    
    # -------------------------------------------------CAMPOS COMPUTADOS----------------------------------------------------------

    total_area = fields.Float(string = "Superficie total", compute = "_compute_total_area", store = True)
    best_offer = fields.Float(string = "Mejor oferta", compute = "_compute_best_offer", store = True)
    offer_partner_ids = fields.Many2many( comodel_name="res.partner", string="Interesados", compute="_compute_offer_partner_ids")

    # ------------------------------------------------- COMPUTOS ----------------------------------------------------------    
   
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            
            offers = record.offer_ids.mapped("price")

            if offers:
                record.best_offer = max(offers)
            else:
                record.best_offer = 0

    @api.depends("offer_ids.partner_id")
    def _compute_offer_partner_ids(self):
        for record in self:
            record.offer_partner_ids = record.offer_ids.mapped("partner_id")


    # ------------------------------------------------- ONCHANGE ----------------------------------------------------------

    @api.onchange("garden")
    def _on_change_garden(self):
        if self.garden:
            self.garden_area = 10
        else:
            self.garden_area = 0

    @api.onchange("expected_price")
    def _on_change_expected_price(self):

        if self.expected_price and self.expected_price != 0 and self.expected_price < 10000:
            
            return {
                'warning': {'title': "Warning", 'message': "Cuidado! Precio demasiado bajo!", 'type': 'notification'},
            }

    # ------------------------------------------------- ACCIONES ---------------------------------------------------------- 
    def action_mark_as_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("Error: No se puede marcar como VENDIDA una propiedad CANCELADA")
            else:
                record.state = "sold"
        return True
    
    def action_mark_as_canceled(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Error: No se puede marcar como CANCELADA una propiedad VENDIDA")
            else:
                record.state = "canceled"
        return True
    
    def action_random_offer(self):
        for record in self:

            # Generar número aleatorio entre -0.30 y +0.30
            variation = random.uniform(-0.30, 0.30)

            # Calcular precio oferta
            offered_price = record.expected_price * (1 + variation)

            #Obtener todos los partners activos
            all_partners = self.env['res.partner'].search([('active','=',True)])

            # Buscar partner que no hay ofertado
            available_partners = all_partners - record.offer_partner_ids

            #Elegir uno aleatorio
            partner = random.choice(available_partners)

            # Crear oferta
            self.env["estate.property.offer"].create({

                "price": offered_price,
                "partner_id": partner.id,
                "property_id": record.id

            })
    
    def action_clear_tags(self):
        
        for record in self:
            record.tag_ids = [Command.clear()]


    def action_link_tags(self):

        tags = self.env["estate.property.tag"].search([])

        for record in self:
            record.tag_ids = [Command.set(tags.ids)]
    
    def action_brand_new(self):

        tag = self.env["estate.property.tag"].search([('name', '=', 'A estrenar')], limit=1)

        for record in self:
            if tag:
                record.tag_ids = [Command.link(tag.id)]
            else:
                record.tag_ids = [Command.create({'name' : 'A estrenar'})]

        return 
    
    # ------------------------------------------------- ORM ----------------------------------------------------------
    
    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        for rec in self:
            if rec.state not in ("new", "canceled"):
                raise UserError("Solo se pueden borrar propiedades nuevas o canceladas.")