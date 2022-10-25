



# O365
  
Conectar con Outlook mediante O365.  
  
![banner](imgs/Banner_O365.png)
## Como instalar este módulo
  
__Descarga__ e __instala__ el contenido en la carpeta 'modules' en la ruta de Rocketbot.  

## Como usar este modulo

Antes de usar este modulo, es necesario registrar tu aplicación en el portal de Azure App Registrations. 

1. Inicie sesión en Azure Portal (Registración de aplicaciones: https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade ).
2. Seleccione "Nuevo registro".
3. En “Tipos de cuenta compatibles” soportados elija:
    a. "Cuentas en cualquier directorio organizativo (cualquier directorio de Azure AD: multiinquilino) y cuentas de Microsoft personales (como Skype o Xbox)" para este caso utilizar  ID Inquilino = common
    b. "Solo cuentas de este directorio organizativo (solo esta cuenta: inquilino único) para este caso utilizar ID Inquilino especifica de la aplicación.
4. Establezca la uri de redirección (Web) como: https://login.microsoftonline.com/common/oauth2/nativeclient y haga click en "Registrar".
5. Copie el ID de la aplicación (cliente). Necesitará este valor.
6. Dentro de "Certificados y secretos", genere un nuevo secreto de cliente. Establezca la caducidad (preferiblemente 24 meses). Copie el VALOR del secreto de cliente creado (NO el ID de Secreto). El mismo se ocultará al cabo de unos minutos.
7. Dentro de "Permisos de API", haga click en "Agregar un permiso", seleccione "Microsoft Graph", luego "Permisos delegados", busque y seleccione "Mail.ReadWrite" y "User.Read", y por ultimo "Agregar permisos".
8. En la consola de Rocketbot se generara una url (Ejemplo: https://login.microsoftonline.com/common/oauth2/v2.0/authorize?response_type=code&client_id=82f8efcd-6a0d-4532-a62e-3e2aecb4d19f&redirect_uri=https%3A%2F%2Flogin.microsoftonline.com%2Fcommon%2Foauth2%2Fnativeclient&scope=Mail.ReadWrite+User.Read.All&state=3LvNFBfX0qej9Q0rsixmSWjCGJyi0M&access_type=offline ), copiarla y pegarla en su navegador.
9. Aceptar el otorgamiento de permisos y devolvera una pantalla sin contenido. Copiar la URL (Ejemplo: https://login.microsoftonline.com/common/oauth2/nativeclient?code=M.R3_SN1.5dcda10b-6567-ce05-3a5b-f67145c62684&state=3LvNFBfX0qej9Q0rsixmSWjCGJyi0M) y pegarla en la consola de Rocketbot debajo de "Paste the authenticated url here:".
10. Presionar "enter" y si la operación fue exitosa vera en la consola: "Authentication Flow Completed. Oauth Access Token Stored. You can now use the API." y se habra creado un archivo con sus credenciales, en la carpeta raiz de Rocketbot, llamado o365_token.txt o o365_token_{session}.txt.

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

### Listar todos los emails
  
Listar todos los emails, se puede especificar un filtro
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Filtro||subject eq 'compras'|
|ID Carpeta||Inbox|
|Cantidad de emails a listar||25|
|Asignar a variable||Variable|
|session||session|

### Listar emails no leidos
  
Listar todos los emails no leidos de tu casilla de correo
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
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
|Marcar como leído||-|
|Cuerpo de email en HTML|Si se marca esta casilla, devolvera el cuerpo del email en versión HTML.||
|Asignar a variable||Variable|
|session||session|

### Enviar Email
  
Envia un email
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Para||to@mail.com, to2@mail.com|
|Cc||to1@mail.com, to3@mail.com|
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
|Cc||to1@mail.com, to3@mail.com|
|Mensaje||Esto es una prueba|
|Archivo Adjunto||C:\User\Desktop\test.txt|
|Carpeta (Varios archivos)||C:\User\Desktop\Files|
|Marcar como leído||-|
|session||session|

### Reenviar Email
  
Reenviar un email utilizando su ID
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del email||345|
|Para||to@mail.com, to2@mail.com|
|Cc||to1@mail.com, to3@mail.com|
|Mensaje||This is a test.|
|Archivo Adjunto||C:\User\Desktop\test.txt|
|Carpeta (Varios archivos)||C:\User\Desktop\Files|
|Marcar como leído||-|
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

### Listar carpetas del correo
  
Lista todas las carpetas del correo
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
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
|Asignar a variable||Variable|
|session||session|

### Obtener listas
  
Obtener las listas del Sitio
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del Grupo||ID|
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
|Nombre de Lista||name|
|Asignar a variable||Variable|
|session||session|

### Obtener Item
  
Obtener un Item, utilizando su ID, de una Lista
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|ID del Sitio||ID|
|Nombre de Lista||name|
|ID del Item||ID|
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