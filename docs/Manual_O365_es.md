# O365
  
Este modulo permite conectar Rocketbot con Outlook y/o Sharepoint mediante la API O365. Se podrán programar tareas relacionadas a la lectura, descarga de adjuntos, envío, respuesta o archivado de correos electrónicos de casilla Outlook, asi como realizar operaciones relacionadas a listas de Sharepoint.  

![banner](imgs/Banner_O365.png)
## Como instalar este módulo

La instalación puede ser:
1. Manual: __Descargar__ el archivo .zip y descomprimirlo en la carpeta modules. El nombre de la carpeta debe ser el mismo al del módulo y dentro debe tener los siguientes archivos y carpetas: \__init__.py, package.json, docs, example y libs. Si tiene abierta la aplicación, refresca el navegador para poder utilizar el nuevo modulo.
2. Automática: Al ingresar a Rocketbot Studio sobre el margen derecho encontrara la sección de **Addons**, seleccionar **Install Mods**, buscar el modulo deseado y presionar install.

## Como usar este modulo

Antes de usar este módulo, es necesario registrar tu aplicación en el portal de Azure App Registrations. 

1. Ingrese a https://azure.microsoft.com/ e inicie sesión o cree una cuenta (de no poseer una). 
2. Busque el servicio Azure Active Directory.
3. En el menu en el lateral izquierdo, ingrese a "Registros de Aplicaciones".
4. Seleccione "Nuevo registro".
5. En “Tipos de cuenta compatibles” soportados elija:
    - "Cuentas en cualquier directorio organizativo (cualquier directorio de Azure AD: multi-inquilino) y cuentas de Microsoft personales (como Skype o Xbox)" para este caso utilizar  ID Inquilino (Tenant ID __en ingles__) = **common**.
    - "Solo cuentas de este directorio organizativo (solo esta cuenta: inquilino único) para este caso utilizar **ID Inquilino** (**Tenant ID** __en ingles__) especifico de la aplicación.
6. Establezca la uri de re-dirección (Web) como: https://login.microsoftonline.com/common/oauth2/nativeclient y haga click en "Registrar".
7. Copie el ID de la aplicación (cliente). Necesitará este valor.
8. Dentro de "Certificados y secretos", genere un nuevo secreto de cliente. Establezca la caducidad (preferiblemente 24 meses). Copie el **VALOR** del secreto de cliente creado (**__NO el ID de Secreto__**). El mismo se ocultará al cabo de unos minutos.
9. Dentro de "Permisos de API", haga click en "Agregar un permiso", seleccione "Microsoft Graph", luego "Permisos delegados", busque y seleccione "Mail.ReadWrite" y "User.Read", y por ultimo "Agregar permisos".
10. En Rocketbot Studio, insertar el comando "Conectar a O365", ingresar los datos solicitados (ID de cliente, valor del secreto y tenant) y ejecutar el comando.
11. En la consola de Rocketbot se generara una url, copiarla y pegarla en su navegador.
    - **Ejemplo:** <sub>https://login.microsoftonline.com/common/oauth2/v2.0/authorize?response_type=code&client_id=82f8efcd-6a0d-4532-a62e-3e2aecb4d19f&redirect_uri=https%3A%2F%2Flogin.microsoftonline.com%2Fcommon%2Foauth2%2Fnativeclient&scope=Mail.ReadWrite+User.Read.All&state=3LvNFBfX0qej9Q0rsixmSWjCGJyi0M&access_type=offline</sub>
12. Aceptar el otorgamiento de permisos y devolverá una pantalla sin contenido. Copiar la URL y pegarla el la consola de Rocketbot debajo de **"Paste the authenticated url here:"**.
    - **Ejemplo:** <sub>https://login.microsoftonline.com/common/oauth2/nativeclient?code=M.R3_SN1.5dcda10b-6567-ce05-3a5b-f67145c62684&state=3LvNFBfX0qej9Q0rsixmSWjCGJyi0M</sub> 
13. Presionar "enter" y si la operación fue exitosa vera en la consola: "Authentication Flow Completed. Oauth Access Token Stored. You can now use the API." y se habrá creado un archivo con sus credenciales, en la carpeta raíz de Rocketbot, llamado o365_token.txt o o365_token_{session}.txt.

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

Las mismas surgen del json de la respuesta a la consulta realizada a la API. Para revisar las propiedades de correos específicos puede ingresar a https://developer.microsoft.com/en-us/graph/graph-explorer ingresando con su cuenta de AZURE y realizar la consulta https://graph.microsoft.com/v1.0/me/messages/<ID_correo>.

Es importante tener presente que solo deben utilizarse comillas simples (') cuando se indique el valor a filtrar, salvo para el caso de valores booleanos (__true__ / __false__). A continuación se muestran ejemplos prácticos de cómo realizar filtros:

- Correos no leídos = __isRead eq false__
- Correos leídos = __isRead eq true__
- El Asunto es igual a... = __subject eq ‘example’__
- El Asunto contiene... = __contains(Subject, ‘example’)__
- El Asunto comienza con la palabra... = __startswith(Subject, ‘example’)__
- La fecha de recepción esta entre... = __ReceivedDateTime ge <date> and ReceivedDateTime le <date>__
- El cuerpo del correo contiene... = __contains(Body/Content, ‘example’)__
- El remitente del correo es igual a... = __From/EmailAddress/Address eq ‘example@example.com’__
- El remitente del correo comienza con... = __Startswith(From/EmailAddress/Address, ‘example’)__
- El correo tiene adjuntos = __HasAttachments eq true__
## Como identificar correos (ID)

Los correos se encuentran identificados con un ID único y dinámico. Esta última cualidad hace que si un correo cambia algunas de sus propiedades el ID se verá afectado, el caso más claro se produce al cambiar un correo de carpeta. Por ejemplo: el ID de un correo en Inbox no será el mismo una vez lo hayamos movido a la carpeta "Procesados", para volver a hacer uso del correo se deberá ejecutar el comando Listar Emails sobre la carpeta "Procesados" y obtener el nuevo ID.

## Descripción de los comandos

### Conectar a O365
  
Este comando permite conectar a una una cuenta de Microsoft mediante una aplicación creada en Azure. Asignando un ID de sesión permite conectarse a multiples cuentas en el mismo robot.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|client_id|ID de Aplicación obtenido de Portal Azure.|65a03f5a-7a5d-4b07-8g2a-5d4302dd6bae|
|client_secret|Valor del Secreto de Aplicación obtenido de Portal Azure.|fyh5Q~eBIxrYK8R8Anc3d0s5lbJJnjg83FmNDa9E|
|tenant_id|Valor del Tenant o Inquilino de Aplicación obtenido de Portal Azure.|common ó f1b6cc40-37d0-4b36-80de-a59d2b9ceeab|
|session|ID a otorgar a la conexión.|default|
|Conectarse a Sharepoint|Checkbox: Tildar para otorgar permisos a la conexión para operar en Sharepoint.|-|

### Listar todos los emails
  
Este comando permite listar todos los correos de una cuenta de correo electrónico, se puede especificar parámetros de filtrado y la cantidad maxima del listado.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Filtro|Parámetros de filtrado para la realizar la búsqueda en la casilla de correo. Dejar vació para traer todos los correos.|subject eq 'compras'|
|ID Carpeta|ID de la carpeta donde buscar el/los correos, obtenido con el comando listar carpetas del correo. Por defecto busca en Bandeja de Entrada.|Inbox|
|Cantidad de emails a listar|Numero máximo de correos a listar. Si la cantidad obtenida supera el valor, devolverá los mas recientes que cumplan las condiciones de filtrado.|25|
|Asignar a variable|Nombre de la variable de Rocketbot donde almacenar el resultado de la ejecución.|Variable|
|session|ID a otorgado a la conexión.|default|

### Listar emails no leídos
  
Este comando permite listar todos los correos no leídos de una cuenta de correo electrónico, se puede especificar parámetros de filtrado y la cantidad maxima del listado.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Filtro|Parámetros de filtrado para la realizar la búsqueda en la casilla de correo. Dejar vació para traer todos los correos no Leidos.|subject eq 'compras'|
|ID Carpeta|ID de la carpeta donde buscar el/los correos, obtenido con el comando listar carpetas del correo. Por defecto busca en Bandeja de Entrada.|Inbox|
|Cantidad de emails a listar|Numero máximo de correos a listar. Si la cantidad obtenida supera el valor, devolverá los mas recientes que cumplan las condiciones de filtrado.|25|
|Asignar a variable|Nombre de la variable de Rocketbot donde almacenar el resultado de la ejecución.|Variable|
|session|ID a otorgado a la conexión.|default|

### Leer email por ID
  
Este comando permite leer y descargar los adjuntos de un correo utilizando su ID (obtenido con alguno de los comandos de Listar). Se puede obtener el cuerpo en formato texto plano o HTML.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del email|ID del correo a leer, obtenido de los comandos de Listar Correos.|345|
|Ruta para descargar adjuntos|Ruta de la carpeta donde descargar los archivos adjuntos al correo.|C:\User\Desktop|
|Descargar adjuntos|Checkbox: Si se marca esta casilla, se descargaran los archivos adjunto en la ruta indicada.|-|
|Marcar como leído|Checkbox: Si se marca esta casilla, el correo figurara como "leído" en la casilla de correo.|-|
|Cuerpo de email en HTML|Checkbox: Si se marca esta casilla, devolverá el cuerpo del email en versión HTML.|-|
|Asignar a variable|Nombre de la variable de Rocketbot donde almacenar el resultado de la ejecución.|Variable|
|session|ID a otorgado a la conexión.|default|

### Enviar Email
  
Este comando permite enviar un correo desde una casilla de correo electrónico a uno o multiples destinatarios. El cuerpo del correo puede ser en formato texto plano o HTML y puede adjuntarse una único archivo o una carpeta con multiples archivos.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Para|Dirección/es de correo electrónico (separadas por coma) destinatarias del correo a enviar|to@mail.com, to1@mail.com|
|Cc|Dirección/es de correo electrónico (separadas por coma) en copia del correo a enviar|to2@mail.com, to3@mail.com|
|Bcc|Dirección/es de correo electrónico (separadas por coma) en copia oculta del correo a enviar|to4@mail.com, to5@mail.com|
|Asunto|Asunto del correo a enviar|Nuevo mail|
|Mensaje|Cuerpo del correo a enviar, puede ser en formato texto plano o HTML|Esto es una prueba|
|Archivo Adjunto|Ruta del archivo a adjuntar al correo a enviar|C:\User\Desktop\test.txt|
|Carpeta (Varios archivos)|Ruta de la carpeta contenedora de los archivos a adjuntar al correo a enviar|C:\User\Desktop\Files|
|session|ID a otorgado a la conexión.|default|

### Responder Email
  
Este comando permite responder un correo utilizando su ID (obtenido con alguno de los comandos de Listar) a uno o multiples destinatarios. El cuerpo del correo puede ser en formato texto plano o HTML y puede adjuntarse una único archivo o una carpeta con multiples archivos.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del email|ID del correo a responder, obtenido de los comandos de Listar Correos.|345|
|Cc|Dirección/es de correo electrónico (separadas por coma) en copia del correo a enviar|to2@mail.com, to3@mail.com|
|Bcc|Dirección/es de correo electrónico (separadas por coma) en copia oculta del correo a enviar|to4@mail.com, to5@mail.com|
|Mensaje|Cuerpo del correo respuesta, puede ser en formato texto plano o HTML|Esto es una prueba|
|Archivo Adjunto|Ruta del archivo a adjuntar al correo a enviar|C:\User\Desktop\test.txt|
|Carpeta (Varios archivos)|Ruta de la carpeta contenedora de los archivos a adjuntar al correo a enviar|C:\User\Desktop\Files|
|Marcar como leído|Checkbox: Si se marca esta casilla, el correo figurara como "leído" en la casilla de correo|-|
|session|ID a otorgado a la conexión.|default|

### Reenviar Email
  
Este comando permite reenviar un correo utilizando su ID (obtenido con alguno de los comandos de Listar) a uno o multiples destinatarios. El cuerpo del correo puede ser en formato texto plano o HTML y puede adjuntarse una único archivo o una carpeta con multiples archivos.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del email|ID del correo a reenviar, obtenido de los comandos de Listar Correos.|345|
|Para|Dirección/es de correo electrónico (separadas por coma) destinatarias del correo a enviar.|to@mail.com, to1@mail.com|
|Cc|Dirección/es de correo electrónico (separadas por coma) en copia del correo a enviar.|to2@mail.com, to3@mail.com|
|Bcc|Dirección/es de correo electrónico (separadas por coma) en copia oculta del correo a enviar.|to4@mail.com, to5@mail.com|
|Mensaje|Cuerpo del correo a adicionar al correo a reenviar, puede ser en formato texto plano o HTML.|This is a test.|
|Archivo Adjunto|Ruta del archivo a adjuntar al correo a enviar.|C:\User\Desktop\test.txt|
|Carpeta (Varios archivos)|Ruta de la carpeta contenedora de los archivos a adjuntar al correo a enviar.|C:\User\Desktop\Files|
|Marcar como leído|Checkbox: Si se marca esta casilla, el correo figurara como "leído" en la casilla de correo.|-|
|session|ID a otorgado a la conexión.|default|

### Descargar adjuntos
  
Este comando permite descarga los archivos adjuntos de un correo utilizando su ID (obtenido con alguno de los comandos de Listar). También permite marcar como leído el mencionado correo.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del email|ID de correo del cual descargar los adjuntos, obtenido de los comandos de Listar Correos.|345|
|Ruta para descargar adjuntos|Ruta de la carpeta donde descargar los archivos adjuntos al correo.|C:\User\Desktop|
|Marcar como leído|Checkbox: Si se marca esta casilla, el correo figurara como "leído" en la casilla de correo.|-|
|Asignar a variable|Nombre de la variable de Rocketbot donde almacenar el resultado de la ejecución.|Variable|
|session|ID a otorgado a la conexión.|default|

### Marcar como no leído
  
Este comando permite marcar un correo como no leído utilizando su ID (obtenido con alguno de los comandos de Listar).
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del email|ID de correo al cual marcar como No Leído, obtenido de los comandos de Listar Correos.|345|
|Asignar a variable|Nombre de la variable de Rocketbot donde almacenar el resultado de la ejecución.|Variable|
|session|ID a otorgado a la conexión.|default|

### Listar carpetas del correo
  
Este comando permite listar todas las carpetas de una casilla de correo electrónico.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Asignar a variable|Nombre de la variable de Rocketbot donde almacenar el resultado de la ejecución.|Variable|
|session|ID a otorgado a la conexión.|default|

### Mover email
  
Este comando permite mover un email de una carpeta a otra utilizando sus respectivos IDs (obtenidos con alguno de los comandos de Listar).
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del email|ID de correo a mover, obtenido de los comandos de Listar Correos.|345|
|ID de carpeta destino|ID de la carpeta destino para el correo, obtenido con el comando listar carpetas del correo.|345|
|Asignar a variable|Nombre de la variable de Rocketbot donde almacenar el resultado de la ejecución.|Variable|
|session|ID a otorgado a la conexión.|default|

### Crear carpeta
  
Este comando permite crea una nueva carpeta en una casilla de correo electrónico utilizando el ID de la carpeta padre (obtenido con el comando de Listar Carpetas).
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID carpeta padre|ID de la carpeta donde crear la nueva carpeta, obtenido con el comando listar carpetas del correo. Por defecto la creara en Bandeja de Entrada.|Inbox or 345...|
|Nombre de la nueva carpeta|Nombre a otorgar a la carpeta a crear.|new_folder|
|Asignar a variable|Nombre de la variable de Rocketbot donde almacenar el resultado de la ejecución.|Variable|
|session|ID a otorgado a la conexión.|default|

### Obtener grupos
  
Este comando permite obtener la lista de Grupos a los que pertenece la cuenta.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Asignar a variable|Nombre de la variable de Rocketbot donde almacenar el resultado de la ejecución.|Variable|
|session|ID a otorgado a la conexión.|default|

### Obtener grupo
  
Este comando permite obtener obtener los datos de un Grupo utilizando su ID (obtenido con el comando de Obtener Grupos).
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del Grupo|ID del Grupo del cual obtener los datos, obtenido con el comando Obtener Grupos.|ID|
|Asignar a variable|Nombre de la variable de Rocketbot donde almacenar el resultado de la ejecución.|Variable|
|session|ID a otorgado a la conexión.|default|

### Obtener sitio
  
Este comando permite obtener el Sitio del Grupo utilizando su ID (obtenido con el comando de Obtener Grupos).
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del Grupo|ID del Grupo del cual obtener el Sitio, obtenido con el comando Obtener Grupos.|ID|
|Asignar a variable|Nombre de la variable de Rocketbot donde almacenar el resultado de la ejecución.|Variable|
|session|ID a otorgado a la conexión.|default|

### Obtener listas
  
Este comando permite obtener las listas que existen en un Sitio utilizando su ID de Grupo (obtenido con el comando de Obtener Grupos).
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del Grupo|ID del Grupo del cual obtener las listas que existen en su Sitio, obtenido con el comando Obtener Grupos.|ID|
|Asignar a variable|Nombre de la variable de Rocketbot donde almacenar el resultado de la ejecución.|Variable|
|session|ID a otorgado a la conexión.|default|

### Crear Lista
  
Este comando permite crear una nueva Lista dentro de un Sitio utilizando su ID (obtenido con el comando de Obtener Sitio).
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del Sitio|ID del Sitio en el cual crear una Lista, obtenido con el comando Obtener Sitio.|ID|
|Datos de lista|Diccionario con las propiedades de la nueva lista.|{'displayName': 'example_name'}|
|Asignar a variable|Nombre de la variable de Rocketbot donde almacenar el resultado de la ejecución.|Variable|
|session|ID a otorgado a la conexión.|default|

### Obtener items de lista
  
Este comando permite obtener los items de una Lista utilizando su nombre (obtenido con el comando de Obtener Listas) y el ID del Sitio al cual pertenece (obtenido con el comando de Obtener Sitio).
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del Sitio|ID del Sitio al cual pertenece la Lista, obtenido con el comando Obtener Sitio.|ID|
|Nombre de Lista|Nombre de la Lista de la cual obtener el listado de items.|name|
|Asignar a variable|Nombre de la variable de Rocketbot donde almacenar el resultado de la ejecución.|Variable|
|session|ID a otorgado a la conexión.|default|

### Obtener Item
  
Este comando permite obtener un Item de una Lista utilizando su ID (obtenido con el comando de Obtener Items de Lista), el nombre de la Lista (obtenido con el comando de Obtener Listas) y el ID del Sito (obtenido con el comando de Obtener Sitio) al cual pertenece.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del Sitio|ID del Sitio al cual pertenece la Lista, obtenido con el comando Obtener Sitio.|ID|
|Nombre de Lista|Nombre de la Lista a la cual pertenece el Item.|name|
|ID del Item|ID del Item del cual obtener datos, obtenido con el comando Obtener Items de Lista|ID|
|Asignar a variable|Nombre de la variable de Rocketbot donde almacenar el resultado de la ejecución.|Variable|
|session|ID a otorgado a la conexión.|default|

### Crear Item
  
Este comando permite crear un Item dentro de una Lista utilizando el nombre de la Lista (obtenido con el comando de Obtener Listas) y el ID del Sito (obtenido con el comando de Obtener Sitio) al cual pertenecerá.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del Sitio|ID del Sitio al cual pertenece la Lista, obtenido con el comando Obtener Sitio.|ID|
|Nombre de Lista|Nombre de la Lista a la cual pertenece el Item.|name|
|Datos del Item|Diccionario con los valores para cada uno de los campos del nuevo Item {'campo': 'valor'}.|{'title': 'data'}|
|Asignar a variable|Nombre de la variable de Rocketbot donde almacenar el resultado de la ejecución.|Variable|
|session|ID a otorgado a la conexión.|default|

### Borrar Item
  
Este comando permite borrar un Item de una Lista utilizando su ID (obtenido con el comando de Obtener Items de Lista), el nombre de la Lista (obtenido con el comando de Obtener Listas) y el ID del Sito (obtenido con el comando de Obtener Sitio) al cual pertenece.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del Sitio|ID del Sitio al cual pertenece la Lista, obtenido con el comando Obtener Sitio.|ID|
|Nombre de Lista|Nombre de la Lista a la cual pertenece el Item.|name|
|ID del Item|ID del Item a borrar, obtenido con el comando Obtener Items de Lista|ID|
|Asignar a variable|Nombre de la variable de Rocketbot donde almacenar el resultado de la ejecución.|Variable|
|session|ID a otorgado a la conexión.|default|

### Actualizar Item
  
Este comando permite actualizar los datos de un Item de una Lista utilizando su ID (obtenido con el comando de Obtener Items de Lista), el nombre de la Lista (obtenido con el comando de Obtener Listas) y el ID del Sito (obtenido con el comando de Obtener Sitio) al cual pertenece.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del Sitio|ID del Sitio al cual pertenece la Lista, obtenido con el comando Obtener Sitio.|ID|
|Nombre de Lista|Nombre de la Lista a la cual pertenece el Item.|name|
|ID del Item|ID del Item a actualizar, obtenido con el comando Obtener Items de Lista|ID|
|Datos del Item|Diccionario con los valores a actualizar del Item {'campo': 'valor'}.|{'title': 'data'}|
|Asignar a variable|Nombre de la variable de Rocketbot donde almacenar el resultado de la ejecución.|Variable|
|session|ID a otorgado a la conexión.|default|