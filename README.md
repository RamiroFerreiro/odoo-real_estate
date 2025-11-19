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


