



# O365
  
Connect to Outlook for O365.  

## Como instalar este módulo
  
__Descarga__ e __instala__ el contenido en la carpeta 'modules' en la ruta de Rocketbot.  




## Como usar este modulo

Antes de usar este modulo, es necesario registrar tu aplicación en el portal de Azure App 
Registrations. 

1. Inicie sesión en Azure Portal (Registración de aplicaciones: 
https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade ).
2. Seleccione "Nuevo registro".
3. 
En “Tipos de cuenta compatibles” soportados elija:
    a. "Cuentas en cualquier directorio organizativo (cualquier 
directorio de Azure AD: multiinquilino) y cuentas de Microsoft personales (como Skype o Xbox)" para este caso utilizar  
ID Inquilino = common
    b. "Solo cuentas de este directorio organizativo (solo esta cuenta: inquilino único) para este
 caso utilizar ID Inquilino especifica de la aplicación.
4. Establezca la uri de redirección (Web) como: 
https://login.microsoftonline.com/common/oauth2/nativeclient y haga click en "Registrar".
5. Copie el ID de la 
aplicación (cliente). Necesitará este valor.
6. Dentro de "Certificados y secretos", genere un nuevo secreto de cliente.
 Establezca la caducidad (preferiblemente 24 meses). Copie el VALOR del secreto de cliente creado (NO el ID de Secreto).
 El mismo se ocultará al cabo de unos minutos.
7. Dentro de "Permisos de API", haga click en "Agregar un permiso", 
seleccione "Microsoft Graph", luego "Permisos delegados", busque y seleccione "Mail.ReadWrite" y "User.Read", y por 
ultimo "Agregar permisos".
8. En la consola de Rocketbot se generara una url (Ejemplo: 
https://login.microsoftonline.com/common/oauth2/v2.0/authorize?response_type=code&client_id=82f8efcd-6a0d-4532-a62e-3e2aecb4d19f&redirect_uri=https%3A%2F%2Flogin.microsoftonline.com%2Fcommon%2Foauth2%2Fnativeclient&scope=Mail.ReadWrite+User.Read.All&state=3LvNFBfX0qej9Q0rsixmSWjCGJyi0M&access_type=offline
 ), copiarla y pegarla en su navegador.
9. Aceptar el otorgamiento de permisos y devolvera una pantalla sin contenido. 
Copiar la URL (Ejemplo: 
https://login.microsoftonline.com/common/oauth2/nativeclient?code=M.R3_SN1.5dcda10b-6567-ce05-3a5b-f67145c62684&state=3LvNFBfX0qej9Q0rsixmSWjCGJyi0M)
 y pegarla en la consola de Rocketbot debajo de "Paste the authenticated url here:".
10. Presionar "enter" y si la 
operación fue exitosa vera en la consola: "Authentication Flow Completed. Oauth Access Token Stored. You can now use the
 API." y se habra creado un archivo con sus credenciales, en la carpeta raiz de Rocketbot, llamado o365_token.txt


## Overview


1. Conectar a O365  
Conectar a una insancia de la aplicación de O365

2. Enviar Email  
Envia un email

3. Carpetas Correo  
Lista todas las carpetas del correo

4. Lista todos los email  
Lista todos los email, se puede especificar un filtro

5. Leer email por ID  
Leer email por ID  




----
### OS

- windows
- mac
- linux
- docker

### Dependencies
- [**bs4**](https://pypi.org/project/bs4/)
### License
  
![MIT](https://camo.githubusercontent.com/107590fac8cbd65071396bb4d04040f76cde5bde/687474703a2f2f696d672e736869656c64732e696f2f3a6c6963656e73652d6d69742d626c75652e7376673f7374796c653d666c61742d737175617265)  
[MIT](http://opensource.org/licenses/mit-license.ph)