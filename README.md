# Microsoft Sql Server

* dumpsqldb.py: Esta basado en msqlclient.py de Impacket. Permite bajar todo el contenido de la base de datos.

# >= SharePoint 2013
(https://docs.microsoft.com/en-us/SharePoint/install/user-profile-service-overview?redirectedfrom=MSDN)

## Enumeración de SharePoint

### People Manager
Estas son las REST Api, para el manejo de perfiles en SharePoint 2013 o Superior.
Obtener información de un perfil
#### Obtener información de un perfil

> **[DOMINIO]**/_api/SP.UserProfiles.PeopleManager/GetPropertiesFor(accountName=@v)?@v='i:0#.f|membership|__cuenta.dominio__'
> 
> **[DOMINIO]**/_api/web/siteUsers: Obtiene el listado de usuarios del portal
> 
> /_api/Web/GetUserById(**IdUsuario**)



### Listas
> Obtener todos los items de una lista: **[DOMINIO]**/_api/web/lists/getByTitle('*LISTA*')/items
>
> /_api/web/lists/getByTitle('*Lista*')/items?$filter=(Title%20eq%20%27@**Filtro**%27)&$select=*Campos*&$expand=&$orderby=ID%20asc&$top=9999**
