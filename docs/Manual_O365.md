



# O365
  
Connect to Outlook for O365.  
  
![banner](imgs/Banner_O365.png)
## How to install this module
  
__Download__ and __install__ the content in 'modules' folder in Rocketbot path  

## How to use this module

Before using this module, you need to register your app in the Azure App Registrations portal.

1. Sign in to the Azure portal (Applications Registration: https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade ).
2. Select "New record".
3. Under “Compatible account types” supported choose:
    a. "Accounts in any organizational directory (any Azure AD directory: multi-tenant) and personal Microsoft accounts (such as Skype or Xbox)" for this case use Tenant ID = common
    b. "Only accounts from this organizational directory (only this account: single tenant) for this case use application-specific Tenant ID.
4. Set the redirect uri (Web) as: https://login.microsoftonline.com/common/oauth2/nativeclient and click "Register".
5. Copy the application (client) ID. You will need this value.
6. Under "Certificates and secrets", generate a new client secret. Set the expiration (preferably 24 months). Copy the VALUE of the created client secret (NOT the Secret ID). It will hide after a few minutes.
7. Under "API permissions", click "Add a permission", select "Microsoft Graph", then "Delegated permissions", find and select "Mail.ReadWrite" and "User.Read", and finally " Add permissions".
8. In the Rocketbot console a url will be generated (Example: https://login.microsoftonline.com/common/oauth2/v2.0/authorize?response_type=code&client_id=82f8efcd-6a0d-4532-a62e-3e2aecb4d19f&redirect_uri=https%3A%2F%2Flogin.microsoftonline.com%2Fcommon%2Foauth2%2Fnativeclient&scope=Mail.ReadWrite+User.Read.All&state=3LvNFBfX0qej9Q0rsixmSWjCGJyi0M&access_type=offline ), copy and paste it into your browser.
9. Accept the permissions granting and it will return a screen without content. Copy the URL (Example: https://login.microsoftonline.com/common/oauth2/nativeclient?code=M.R3_SN1.5dcda10b-6567-ce05-3a5b-f67145c62684&state=3LvNFBfX0qej9Q0rsixmSWjCGJyi0M) and paste it into Rocketbot console below "Paste the authenticated url here:".
10. Press "enter" and if the operation was successful you will see in the console: "Authentication Flow Completed. Oauth Access Token Stored. You can now use the API." and a file will have been created with your credentials, in the root folder of Rocketbot, called o365_token.txt or o365_token_{session}.txt.

## Description of the commands

### Connect to O365
  
Connect to O365 application instance
|Parameters|Description|example|
| --- | --- | --- |
|client_id||client_id|
|client_secret||client_secret|
|tenant_id||tenant_id|
|session||session|
|Connect to Sharepoint||-|

### List all emails
  
List all email, you can specify a filter
|Parameters|Description|example|
| --- | --- | --- |
|Filter||subject eq 'compras'|
|Folder ID||Inbox|
|Number of emails to list||25|
|Asign to variable||Variable|
|session||session|

### List unread emails
  
List unread emails
|Parameters|Description|example|
| --- | --- | --- |
|Folder ID||Inbox|
|Number of emails to list||25|
|Asign to variable||Variable|
|session||session|

### Read email for ID
  
Read email for ID
|Parameters|Description|example|
| --- | --- | --- |
|Email ID||345|
|Path for download attachment||C:\User\Desktop|
|Download attachments||-|
|Mark as read||-|
|Asign to variable||Variable|
|session||session|

### Send Email
  
Send email
|Parameters|Description|example|
| --- | --- | --- |
|To||to@mail.com, to2@mail.com|
|Cc||to1@mail.com, to3@mail.com|
|Subject||Nuevo mail|
|Body||Esto es una prueba|
|Attached File||C:\User\Desktop\test.txt|
|Folder (Multiple files)||C:\User\Desktop\Files|
|session||session|

### Reply Email
  
Reply an email
|Parameters|Description|example|
| --- | --- | --- |
|Email ID||345|
|Body||Esto es una prueba|
|Attached File||C:\User\Desktop\test.txt|
|Folder (Multiple files)||C:\User\Desktop\Files|
|Mark as read||-|
|session||session|

### Forward Email
  
Forward an email
|Parameters|Description|example|
| --- | --- | --- |
|Email ID||345|
|To||to@mail.com, to2@mail.com|
|Cc||to1@mail.com, to3@mail.com|
|Body||Esto es una prueba|
|Attached File||C:\User\Desktop\test.txt|
|Folder (Multiple files)||C:\User\Desktop\Files|
|Mark as read||-|
|session||session|

### Download attachments
  
Download attached files
|Parameters|Description|example|
| --- | --- | --- |
|Email ID||345|
|Path for download attachment||C:\User\Desktop|
|Mark as read||-|
|Asign to variable||Variable|
|session||session|

### Mark as unread
  
Mark an email as unread
|Parameters|Description|example|
| --- | --- | --- |
|Email ID||345|
|Asign to variable||Variable|
|session||session|

### Email folders list
  
List of email folders
|Parameters|Description|example|
| --- | --- | --- |
|Asign to variable||Variable|
|session||session|

### Move email
  
Move an email from one folder to another
|Parameters|Description|example|
| --- | --- | --- |
|Email ID||345|
|Folder ID||345|
|Asign to variable||Variable|
|session||session|

### Create folder
  
Creates a new folder in the email
|Parameters|Description|example|
| --- | --- | --- |
|Parent folder ID||Inbox or 345...|
|Name of the new folder||new_folder|
|Asign to variable||Variable|
|session||session|

### Get groups
  
Get list of Groups
|Parameters|Description|example|
| --- | --- | --- |
|Asign to variable||Variable|
|session||session|

### Get group
  
Get Group by ID
|Parameters|Description|example|
| --- | --- | --- |
|Group ID||ID|
|Asign to variable||Variable|
|session||session|

### Get site
  
Get site of the Group
|Parameters|Description|example|
| --- | --- | --- |
|Group ID||ID|
|Asign to variable||Variable|
|session||session|

### Get site lists
  
Get lists of the Site
|Parameters|Description|example|
| --- | --- | --- |
|Group ID||ID|
|Asign to variable||Variable|
|session||session|

### Create List
  
Create a new list
|Parameters|Description|example|
| --- | --- | --- |
|Site ID||ID|
|List data||{'displayName': 'example_name'}|
|Asign to variable||Variable|
|session||session|

### Get list Items
  
Get the items of a list
|Parameters|Description|example|
| --- | --- | --- |
|Site ID||ID|
|List name||name|
|Asign to variable||Variable|
|session||session|

### Get Item
  
Get an item from a list
|Parameters|Description|example|
| --- | --- | --- |
|Site ID||ID|
|List name||name|
|Item ID||ID|
|Asign to variable||Variable|
|session||session|

### Create Item
  
Create an item in a list
|Parameters|Description|example|
| --- | --- | --- |
|Site ID||ID|
|List name||name|
|Item data||{'title': 'data'}|
|Asign to variable||Variable|
|session||session|

### Delete Item
  
Delete an item from a list
|Parameters|Description|example|
| --- | --- | --- |
|Site ID||ID|
|List name||name|
|Item ID||ID|
|Asign to variable||Variable|
|session||session|

### Update Item
  
Update an item data
|Parameters|Description|example|
| --- | --- | --- |
|Site ID||ID|
|List name||name|
|Item ID||ID|
|Item data||{'title': 'data'}|
|Asign to variable||Variable|
|session||session|
