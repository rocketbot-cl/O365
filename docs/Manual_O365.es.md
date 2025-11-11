



# O365
  
Conectate a tu cuenta de correo Outlook y a tu espacio de trabajo Sharepoint.  

*Read this in other languages: [English](Manual_O365.md), [Português](Manual_O365.pr.md), [Español](Manual_O365.es.md)*
  
![banner](imgs/Banner_O365.jpg)
## Como instalar este módulo
  
Para instalar el módulo en Rocketbot Studio, se puede hacer de dos formas:
1. Manual: __Descargar__ el archivo .zip y descomprimirlo en la carpeta modules. El nombre de la carpeta debe ser el mismo al del módulo y dentro debe tener los siguientes archivos y carpetas: \__init__.py, package.json, docs, example y libs. Si tiene abierta la aplicación, refresca el navegador para poder utilizar el nuevo modulo.
2. Automática: Al ingresar a Rocketbot Studio sobre el margen derecho encontrara la sección de **Addons**, seleccionar **Install Mods**, buscar el modulo deseado y presionar install.  



## Como usar este modulo

Antes de usar este módulo, es necesario registrar tu aplicación en el portal de Azure App Registrations. 

1. Inicie sesión en Azure Portal y busque el servicio Microsoft Entra ID.
2. En el menu en el lateral izquierdo, ingrese a "Registros de Aplicaciones".
3. Seleccione "Nuevo registro".
4. En “Tipos de cuenta compatibles”, elija:
    - "Cuentas en cualquier directorio organizativo (cualquier directorio de Azure AD: multiinquilino) y cuentas de Microsoft personales (como Skype o Xbox)" para este caso utilizar  ID Inquilino = **common**.
    - "Solo cuentas de este directorio organizativo (solo esta cuenta: inquilino único) para este caso utilizar **ID Inquilino** especifico de la aplicación.
    - "Solo cuentas personales de Microsoft " for this case use use Tenant ID = **consumers**.
5. Establezca la uri de redirección (Web) como: https://login.microsoftonline.com/common/oauth2/nativeclient y haga click en "Registrar".
6. Copie el ID de la aplicación 
(cliente). Necesitará este valor.
7. Dentro de "Certificados y secretos", genere un nuevo secreto de cliente. Establezca la caducidad (preferiblemente 24 meses). Copie el **VALOR** del secreto de cliente creado (**__NO el ID de Secreto__**). El mismo se ocultará al cabo de unos minutos.
8. Dentro de "Permisos de API", haga click en "Agregar un permiso", seleccione "Microsoft Graph", luego "Permisos delegados", busque y seleccione "Mail.ReadWrite" y "User.Read", y por ultimo "Agregar permisos".
9. En Rocketbot Studio, insertar el comando "Conectar a O365", ingresar los datos solicitados (ID de cliente, valor del secreto y tenant) y ejecutar el comando.
10. En la consola de Rocketbot se generara una url, copiarla y pegarla en su navegador.
    - **Ejemplo:** 
<sub>https://login.microsoftonline.com/common/oauth2/v2.0/authorize?response_type=code&client_id=82f8efcd-6a0d-4532-a62e-3e2aecb4d19f&redirect_uri=https%3A%2F%2Flogin.microsoftonline.com%2Fcommon%2Foauth2%2Fnativeclient&scope=Mail.ReadWrite+User.Read.All&state=3LvNFBfX0qej9Q0rsixmSWjCGJyi0M&access_type=offline</sub>
11. Aceptar el otorgamiento de permisos y devolverá una pantalla sin contenido. Copiar la URL y pegarla el la consola de Rocketbot debajo de **"Paste the authenticated url here:"**.
    - **Ejemplo:** <sub>https://login.microsoftonline.com/common/oauth2/nativeclient?code=M.R3_SN1.5dcda10b-6567-ce05-3a5b-f67145c62684&state=3LvNFBfX0qej9Q0rsixmSWjCGJyi0M</sub> 
12. Presionar "enter" y si la operación fue exitosa vera en la consola: "Authentication Flow Completed. Oauth Access Token Stored. You can now use the API." y se habra creado un archivo con sus credenciales, en la carpeta raíz de Rocketbot, llamado o365_token.txt o o365_token_{session}.txt.

## Como filtrar correos


Para realizar filtro de correos deberá utilizar los siguientes Operadores y Funciones. 

1. __Equality operators__       
    - Igual (__eq__)
    - Diferente (__ne__)
    - Negación (__not__)
    - En (__in__)
    - Tiene (__has__)
2. __Relational operators__
    - Menor que (__lt__)
    - Mayor que (__gt__)
    - Menor o igual que (__le__)
    - Mayor o igual que (__ge__)
3. __Conditional operators__
    - Y (__and__)
    - O (__or__)
4. __Functions__        
    - Comienza con (__startsWith__)
    - Termina con (__endsWith__)
    - Contiene (__contains__)

Las principales propiedades que pueden utilizarse para realizar filtros son:

    "createdDateTime": "2022-10-24T13:14:24Z",
    "categories": [],
    "receivedDateTime": "2022-10-24T13:14:24Z",
    "sentDateTime": "2022-10-24T13:14:09Z",
    "hasAttachments": true/false,
    "importance": "",
    "isReadReceiptRequested": true/false,
    "isRead": true/false,
    "isDraft": true/false,
    "inferenceClassification": "",
    
"body": {
        "contentType": "",
        "content": ""
    },
    "sender": {
        "emailAddress": {
            "name": "",
            "address": ""
        }
    },
    "from": {
        "emailAddress": {
            "name": "",
            "address": ""
        }
    },
    "toRecipients": [
        {
            "emailAddress": {
                "name": "",
                "address": ""
            }
        }
    ],
    "ccRecipients": [
        {
            "emailAddress": {
                "name": "",
                "address": ""
            }
        }
    ],
    "bccRecipients": [
        {
            "emailAddress": {
                "name": "",
                "address": ""
            }
        }
    ],
    "replyTo": [
        {
            "emailAddress": {
                "name": "",
                "address": ""
            }
        }
    ],
    "flag": {
        "flagStatus": ""
    }

Las mismas surgen del json de la respuesta a la consulta realizada a la 
API. Para revisar las propiedades de correos específicos puede ingresar a https://developer.microsoft.com/en-us/graph/graph-explorer ingresando con su cuenta de AZURE y realizar la consulta https://graph.microsoft.com/v1.0/me/messages/<ID_correo>.

Es importante tener presente que solo deben utilizarse comillas simples (') cuando se indique el valor a filtrar, salvo para el caso de valores booleanos (__true__ / __false__). A continuación se muestran ejemplos prácticos de cómo realizar filtros:

- Correos no leidos = __isRead eq false__
- Correos leidos = __isRead eq true__
- El Asunto es igual a... = __subject eq ‘example’__
- El Asunto contiene... = __contains(Subject, ‘example’)__
- El Asunto comienza con la palabra... = __startswith(Subject, ‘example’)__
- La fecha de recepción esta entre... = __ReceivedDateTime ge <date> and ReceivedDateTime le <date>__
- El cuerpo del correo contiene... = __contains(Body/Content, ‘example’)__
- El remitente del correo es igual a... = 
__From/EmailAddress/Address eq ‘example@example.com’__
- El remitente del correo comienza con... = __Startswith(From/EmailAddress/Address, ‘example’)__
- El correo tiene adjuntos = __HasAttachments eq true__
## Como identificar correos (ID)

Los correos se encuentran identificados con un ID único y dinámico. Esta última cualidad hace que si un correo cambia algunas de sus propiedades el ID se verá afectado, el caso más claro se produce al cambiar un correo de carpeta. Por ejemplo: el ID de un correo en Inbox no será el mismo una vez lo hayamos movido a la carpeta "Procesados", para volver a hacer uso del correo se deberá ejecutar el comando Listar Emails sobre la carpeta "Procesados" y obtener el nuevo ID.

Cuando utilice 'filtro' y 'ordenar por' en la misma consulta para obtener mensajes, asegúrese de especificar las propiedades de las siguientes maneras:

Las propiedades que aparecen en 'ordenar por' también deben aparecer en 'filtro'.
Las propiedades que aparecen en 'ordenar por' 
están en el mismo orden que en 'filtro'.
Las propiedades que están presentes en 'ordenar por' aparecen en 'filtro' antes de cualquier propiedad que no lo esté.

## ERROR

Si en la pestaña de login que se abre al ejecutar el comando de conexión visualizas este error:

![error](imgs/o365error.PNG)

Es porque no se han concedido los permisos de administrador necesarios al usuario, por lo que el Administrador deberá realizar los siguientes pasos:

1. Ir a Azure Portal > 
2. Ir a Azure Active Directory 
3. Selecciona tu aplicación 
4. Ir a API Permissions
5. Conceder consentimiento del administrador

Alternativamente, también puede permitir que los usuarios den su consentimiento a la aplicación sin la aprobación del administrador de la siguiente manera:

1. Ir a Azure Portal 
2. Enterprise Application 
3. Ajustes de usuario 
4. Ir a Consentimiento y permisos
5. Permitir a los usuarios consentir para aplicaciones


## Descripción de los comandos

### Conectar a O365
  
Conectar a una insancia de la aplicación de O365
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|client_id||client_id|
|client_secret||client_secret|
|tenant_id||tenant_id|
|session||session|
|Conectarse a Sharepoint||-|
|Proxy HTTPS||https://192.168.00.00:4000|
|Proxy HTTP||http://192.168.00.00:4000|
|Asignar a variable||Variable|

### Listar todos los emails
  
Listar todos los emails, se puede especificar un filtro
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Filtro||subject eq 'compras'|
|Ordenar por||importance desc|
|ID Carpeta||Inbox|
|Cantidad de emails a listar||25|
|Asignar a variable||Variable|
|session||session|

### Listar emails no leidos
  
Listar todos los emails no leidos de tu casilla de correo
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Filtro||subject eq 'compras'|
|Ordenar por||importance desc|
|ID Carpeta||Inbox|
|Cantidad de emails a listar||25|
|Asignar a variable||Variable|
|session||session|

### Leer email por ID
  
Leer un email utilizando su ID
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del email||345|
|Ruta para descargar adjuntos||C:\User\Desktop|
|Descargar adjuntos||-|
|Ruta para descargar mensaje html||C:\User\Desktop|
|Descargar mensaje como HTML||-|
|Marcar como leído||-|
|Cuerpo de email en HTML|Si se marca esta casilla, devolvera el cuerpo del email en versión HTML.||
|Email completo en HTML|Si se marca esta casilla, devolvera el email completo en versión HTML.||
|Cuerpo de email RAW|Si se marca esta casilla, devolvera el cuerpo del email en versión RAW.||
|Asignar a variable||Variable|
|session||session|

### Enviar Email
  
Envia un email
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Para||to@mail.com, to1@mail.com|
|Cc||to2@mail.com, to3@mail.com|
|Bcc||to4@mail.com, to5@mail.com|
|Asunto||Nuevo mail|
|Mensaje||Esto es una prueba|
|Archivo Adjunto||C:\User\Desktop\test.txt|
|Carpeta (Varios archivos)||C:\User\Desktop\Files|
|session||session|

### Responder Email
  
Responder un email utilizando su ID
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del email||345|
|Cc||to2@mail.com, to3@mail.com|
|Bcc||to4@mail.com, to5@mail.com|
|Mensaje||Esto es una prueba|
|Archivo Adjunto||C:\User\Desktop\test.txt|
|Carpeta (Varios archivos)||C:\User\Desktop\Files|
|Marcar como leído||-|
|Responder al remitente||-|
|session||session|

### Reenviar Email
  
Reenviar un email utilizando su ID
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del email||345|
|Para||to@mail.com, to1@mail.com|
|Cc||to2@mail.com, to3@mail.com|
|Bcc||to4@mail.com, to5@mail.com|
|Mensaje||This is a test.|
|Archivo Adjunto||C:\User\Desktop\test.txt|
|Carpeta (Varios archivos)||C:\User\Desktop\Files|
|Marcar como leído||-|
|Asignar a variable||Variable|
|session||session|

### Descargar adjuntos
  
Descarga los archivos adjuntos de un correo
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del email||345|
|Ruta para descargar adjuntos||C:\User\Desktop|
|Marcar como leído||-|
|Asignar a variable||Variable|
|session||session|

### Marcar como no leido
  
Marcar un email como no leido
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del email||345|
|Asignar a variable||Variable|
|session||session|

### Descargar .eml
  
Descargar un correo en formato .eml
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del email||345|
|Folder path||C:/Users/user/Documents/|
|Filename||Mail|
|Asignar a variable||Variable|
|session||session|

### Listar carpetas del correo
  
Lista todas las carpetas del correo
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Filtro||displayName eq 'Processed'|
|Carpeta padre|||
|Asignar a variable||Variable|
|session||session|

### Mover email
  
Mover un email de una carpeta a otra
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del email||345|
|ID de carpeta||345|
|Asignar a variable||Variable|
|session||session|

### Crear carpeta
  
Crea una nueva carpeta en el correo electrónico.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID carpeta padre||Inbox or 345...|
|Nombre de la nueva carpeta||new_folder|
|Asignar a variable||Variable|
|session||session|

### Obtener grupos
  
Obtener lista de Grupos a los que pertenece la cuenta
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Filtro|Filtra los grupos que empiezan con el texto ingresado.||
|Asignar a variable||Variable|
|session||session|

### Obtener grupo
  
Obtener Grupo por su ID
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del Grupo||ID|
|Asignar a variable||Variable|
|session||session|

### Obtener sitio
  
Obtener el sitio del Grupo
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del Grupo||ID|
|Hostname|Ejemplo del link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH sacar tusitio.sharepoint.com|tusitio.sharepoint.com|
|Ruta al sitio|Ejemplo del link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH sacar /sites/RecursosHumanos/SubsitioRRHH|/sites/RecursosHumanos/SubsitioRRHH|
|Asignar a variable||Variable|
|session||session|

### Obtener listas
  
Obtener las listas del Sitio
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del Grupo||ID|
|Asignar a variable||Variable|
|session||session|

### Obtener listas por ID del Sitio
  
Obtener las listas del Sitio
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del Sitio||ID|
|Asignar a variable||Variable|
|Session||session|

### Obtener columnas de lista
  
Obtener las columnas editables de una Lista específica del Sitio
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del Sitio||ID|
|ID de Lista||ID|
|Asignar a variable||Variable|
|session||session|

### Crear Lista
  
Crear una nueva lista
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del Sitio||ID|
|Datos de lista||{'displayName': 'example_name'}|
|Asignar a variable||Variable|
|session||session|

### Obtener items de lista
  
Obtener los items de una Lista utilizando su nombre
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del Sitio||ID|
|Hostname|Ejemplo del link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH sacar tusitio.sharepoint.com|tusitio.sharepoint.com|
|Ruta al sitio|Ejemplo del link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH sacar /sites/RecursosHumanos/SubsitioRRHH|/sites/RecursosHumanos/SubsitioRRHH|
|Nombre de Lista||name|
|Limite||10|
|Filtro de consulta||field/id1 eq 'value'|
|Ordenar por||column|
|Campos a expandir||['id1','id2',...]|
|Asignar a variable||Variable|
|session||session|

### Obtener Item
  
Obtener un Item, utilizando su ID, de una Lista
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del Sitio||ID|
|Hostname|Ejemplo del link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH sacar tusitio.sharepoint.com|tusitio.sharepoint.com|
|Ruta al sitio|Ejemplo del link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH sacar /sites/RecursosHumanos/SubsitioRRHH|/sites/RecursosHumanos/SubsitioRRHH|
|Nombre de Lista||name|
|ID del Item||ID|
|Campos a expandir||['id1','id2',...]|
|Asignar a variable||Variable|
|session||session|

### Crear Item
  
Crear un Item dentro de una Lista
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del Sitio||ID|
|Nombre de Lista||name|
|Datos del Item||{'title': 'data'}|
|Asignar a variable||Variable|
|session||session|

### Borrar Item
  
Borrar un Item, usando su ID, de una Lista
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del Sitio||ID|
|Nombre de Lista||name|
|ID del Item||ID|
|Asignar a variable||Variable|
|session||session|

### Actalizar Item
  
Actualizar datos de un Item usando si ID
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del Sitio||ID|
|Nombre de Lista||name|
|ID del Item||ID|
|Datos del Item||{'title': 'data'}|
|Asignar a variable||Variable|
|session||session|

### Obtener bibliotecas de documentos
  
Obtener una lista de las bibliotecas de documentos dentro del sitio
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del Sitio||ID|
|Hostname|Ejemplo del link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH sacar tusitio.sharepoint.com|tusitio.sharepoint.com|
|Ruta al sitio|Ejemplo del link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH sacar /sites/RecursosHumanos/SubsitioRRHH|/sites/RecursosHumanos/SubsitioRRHH|
|Asignar a variable||Variable|
|session||session|

### Obtener documentos
  
Obtenga una lista de los documentos dentro de una biblioteca
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del Sitio||ID|
|Hostname|Ejemplo del link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH sacar tusitio.sharepoint.com|tusitio.sharepoint.com|
|Ruta al sitio|Ejemplo del link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH sacar /sites/RecursosHumanos/SubsitioRRHH|/sites/RecursosHumanos/SubsitioRRHH|
|ID de la Biblioteca|Puede obtener el ID de la biblioteca utilizando el módulo 'Obtener bibliotecas de documentos'|ID|
|Empezar desde|Ruta dentro de la biblioteca desde donde empezar a obtener los documentos. Ejemplo /Documentos compartidos/Carpeta1|Path/to/folder|
|Contiene|Obtener solo los documentos que contienen este texto en su nombre. Dejar vacío para obtener todos los documentos.|Text|
|Asignar a variable||Variable|
|session||session|

### Subir documento
  
Subir un documento a una biblioteca del sitio
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del Sitio||ID|
|ID de la Biblioteca||ID|
|ID de la Carpeta||ID|
|Ruta|||
|Asignar a variable||Variable|
|session||session|

### Descargar o modificar documento
  
Subir un documento a una biblioteca del sitio
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del Sitio||ID|
|ID de la Biblioteca||ID|
|ID del Item||ID|
|Datos a modificar||{'name': 'new_name.jpg', 'description':'new_description'}|
|Actualizar datos de documento|||
|ID de la carpeta destino||ID|
|Mover documento|||
|Ruta|||
|Descargar documento|||
|Borrar documento|||
|Asignar a variable||Variable|
|session||session|
