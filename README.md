# odoo-real_estate
Repositorio creado para el desarrollo de los ejercicios de la materia Programacion ERP con Odoo en el contexto de la Licenciatura en Sistemas.

## Consideraciones
### Activar Permisos del Módulo
Para poder visualizar el desarrollor del módulo: ingresar como superusuario o bien agregar el usuario admin/admin al grupo "Manager de Propiedades". Para la segunda opción: 

**1) Activar modo desarrollador.** Settings --> activate mode developer

**2) Actualizar el modulo real_estateG1.** Buscar modulo --> upgrade

**3) Agregar Mitchell Admin al grupo "Manager de Propiedades".** Settings --> Users and Companies --> Groups --> Inmobiliara / Manager de Propiedades --> Add a line --> Mitchell Admin

## Unidad 1

### Punto 4
Al crear un modelo, en nuestro caso "estate_property", se agregan por defecto algunos campo adicionales. Los cuales son: **id** (integer), **create_uid** (integer), **write_uid** (integer), **create_date** (timestamp without time zone) y **write_date** (timestamp without time zone).
    
Los campos **create_uid** y **write_uid** son FK con la tabla usuarios. El primero indica que usuario creo el registro. El segundo indica que usuario modificó por última vez el registro. 

### Punto 6
El orden de los archivos colocado en el manifest es importante. Primero hay que agregar el archivo que contiene las acciones y después el archivo que contiene al menú que las consume. Por el contrario, el programa falla ya que Odoo lo lee de manera secuencial.

### Punto 7
Aunque hayamos creado el menú solo se puede acceder como superusuario. Esto se debe a que no están definidos los permisos. El superusuario tiene permiso a todo y por eso se puede visualizar. 

### Punto 8
Si en el view_mode de la acción colocamos "list" solo vamos a poder visualizar el listado de registros y crear nuevos, no se va a poder modificar ni entrar al detalle completo de cada uno.

Si solo colocamos "form" vamos a poder crear nuevos registros y entrar al detalle del primero que aparezca.

### Punto 9
En Odoo existen tres tipos de usuarios: internal, public, portal. El **usuario interno** es el que tiene acceso a backoffice. El **usuario público** solo tiene acceso a la página web sin necesidad de login. El **usuario portal** está pensado para los clientes y proveedores, tienen acceso a la página web, pueden ver seguimiento de órdenes y facturas pero tiene limitado el backoffice.

### Punto 10
EL grupo **base.group_user** representa a un usuario interno (Internal User) en Odoo. Para hacer que ese grupo tenga todos los permisos hay que definirlo en el csv. 

Es un grupo definido en el código nativo de Odoo por esto mismo se utiliza "base." y el usuario admin originalmente pertenece a este grupo.

### Punto 12
Los grupos y sus permisos es mejor definirlos por código, ya que persisten mejor y no se pierden cosas. Puede servir hacerlo en desarrollo para probar algo rápido.

### Punto 15
Solo los usuarios que pertenecen a algún grupo con permisos explícitos en **ir.model.access.csv** son los pueden interactuar con el modelo **estate.property**. Los usuarios que no pertenezcan a ningún grupo con acceso quedan bloqueados.

Estos grupos pueden ser custom, es decir, definidos por nuestro módulo o bien, pueden ser nativos de Odoo como usuario interno, público o portal.

### Punto 18
Al duplicar el registro solo ocurrio lo esperado, lo duplico tal cual sin alguna diferencia alguna

### Punto 19
Se realiza el duplicado pero con la diferencia de que los campos donde agregamos "copy=False" no se duplicaron.

### Punto 35
Se utiliza el campo many2many porque la relacion entre propiedades y etiquetas permite que mas de 1 propiedad tenga asignada la misma etiqueta, como tambien permite que mas de una etiqueta tenga asignada la misma propiedad, esa relacion se guarda dentro de la tabla intermedia generada por el ORM, donde los atributos son las 2 FK a las tablas relacionadas, permitiendo tener un registro de estas relaciones sin perder datos.

### Punto 39
1) "inverse_name" hay que especificarlo porque el campo One2many no guarda nada. Solo se muestra los registros (estate_property_offer) que apuntan a la propiedad a través de su Many2one (property_id).

2) El One2many es virtual porque no crea una columna en estate.property. Los datos reales están en el lado Many2one (estate_property_offer.property_id) y el One2many lo refleja.

### Punto 40
No es necesario incorporar una acción porque se llama la vista de lista ofertas desde el formulario de propiedad.

## Unidad 2
### Punto 3

 El campo no se ve reflejado en la tabla de pgweb porque es un campo computado y se calcula cada vez que se llama desde la vista. No se persiste porque hasta el momento no se indicó "store = true" que por defecto está en false. 

### Punto 5
Si al campo computado le agregamos "store = true" este se calculará solamente una única vez y luego cada vez que se llame desde la vista se consultará desde la base de datos.

Además del "store = true" para persistir el campo con su valor, hay que utilizar el decorador "@api.depends()" para establecer la dependencia con otros campos y que se calcule cada vez que se llama desde la vista.

### Punto 7
Al campo "best_offer" creo que es bueno almacenarlo para no tener que estar buscando el valor máximo cada vez que se ejecuta. En caso de que crezca mucho la cantidad de ofertas, el costo del cómputo será muy grande, por eso conviene almacenarlo. La desventaja se encuentra en que cada vez que se agrega una nueva oferta, el campo "best_offer"  debe calcularse y persistirse.

Por otra parte, si en un futuro queremos visualizar el campo en una lista no se tiene que calcular por cada llamado y se consulta directamente de la base de datos.

### Punto 19
No se puede utilizar "related" porque offer_id es un atributo One2Many y offer_partner_ids  es un atributo Many2many. Un related apunta a un único campo de un único registro.

### Punto 22
Usar @api.ondelete() es más conveniente que poner la validación en la lógica de negocio porque este decorador actúa a nivel del ORM, garantizando que ningún proceso —ni directo ni indirecto— pueda eliminar registros no permitidos, manteniendo las capas bien separadas y el código más seguro, coherente y mantenible.

### Punto 24

No es necesario crear una regla de acceso en ir.model.access.csv para este caso porque estamos usando herencia clásica (_inherit) sobre el modelo res.users. Esto significa que estamos agregando un campo a un modelo existente, y por lo tanto, se mantienen las reglas de acceso ya definidas para res.users. Todos los usuarios con permisos sobre ese modelo seguirán accediendo normalmente al nuevo campo agregado.