



# O365
  
Connect to to your Outlook email account and Sharepoint workspace.  

*Read this in other languages: [English](Manual_O365.md), [Português](Manual_O365.pr.md), [Español](Manual_O365.es.md)*
  
![banner](imgs/Banner_O365.jpg)
## How to install this module
  
To install the module in Rocketbot Studio, it can be done in two ways:
1. Manual: __Download__ the .zip file and unzip it in the modules folder. The folder name must be the same as the module and inside it must have the following files and folders: \__init__.py, package.json, docs, example and libs. If you have the application open, refresh your browser to be able to use the new module.
2. Automatic: When entering Rocketbot Studio on the right margin you will find the **Addons** section, select **Install Mods**, search for the desired module and press install.  

## How to use this module

Before using this module, you need to register your app in the Azure App Registrations portal.

1. Sign in to the Azure portal and search for the Microsoft Entra ID service.
2. On the left side menu, get into "App Registrations".
3. Select "New record".
4. Under “Compatible account types”, choose:
    - "Accounts in any organizational directory (any Azure AD directory: multi-tenant) and personal Microsoft accounts (such as Skype or Xbox)" for this case use Tenant ID = **common**.
    - "Only accounts from this organizational directory (only this account: single tenant) for this case use application-specific **Tenant ID**.
    - "Personal Microsoft accounts only" for this case use use Tenant ID = **consumers**.
5. Set the redirect uri (Web) as: https://login.microsoftonline.com/common/oauth2/nativeclient and click "Register".
6. Copy the application (client) ID. You will need this value.
7. Under "Certificates and secrets", generate a new client secret. Set 
the expiration (preferably 24 months). Copy the **VALUE** of the created client secret (**__NOT the Secret ID__**). It will hide after a few minutes.
8. Under "API permissions", click "Add a permission", select "Microsoft Graph", then "Delegated permissions", find and select "Mail.ReadWrite" and "User.Read", and finally " Add permissions".
9.  In Rocketbot Studio, insert the "Connect to O365" command, enter the requested data (client ID, secret value, and tenant), and run the command.
10. In the Rocketbot console a url will be generated, copy and paste it into your browser.
    - **Example:** <sub>https://login.microsoftonline.com/common/oauth2/v2.0/authorize?response_type=code&client_id=82f8efcd-6a0d-4532-a62e-3e2aecb4d19f&redirect_uri=https%3A%2F%2Flogin.microsoftonline.com%2Fcommon%2Foauth2%2Fnativeclient&scope=Mail.ReadWrite+User.Read.All&state=3LvNFBfX0qej9Q0rsixmSWjCGJyi0M&access_type=offline</sub>
11. Accept the permissions granting and it will return a screen without content. 
Copy the URL and Paste it into Rocketbot console below **"Paste the authenticated url here:"**.
    - **Example:** <sub>https://login.microsoftonline.com/common/oauth2/nativeclient?code=M.R3_SN1.5dcda10b-6567-ce05-3a5b-f67145c62684&state=3LvNFBfX0qej9Q0rsixmSWjCGJyi0M</sub>
12. Press "enter" and if the operation was successful you will see in the console: "Authentication Flow Completed. Oauth Access Token Stored. You can now use the API." and a file will have been created with your credentials, in the root folder of Rocketbot, called o365_token.txt or o365_token_{session}.txt.

## ERROR

If in the login tab that opens when you execute the connection command you see this error:

![error](imgs/o365error.PNG)

It is because the necessary administrator permissions have not been granted to the user, so the Administrator must perform the following steps:

1. Go to Azure portal >
2. Go to Azure Active Directory
3. Select your application
4. Go to API Permissions
5. Grant administrator consent


Alternatively, you can also allow users to consent to the app without administrator approval as follows:

1. Go to Azure portal
2.Enterprise Application
3. User settings
4. Go to Consent and permissions
5. Allow users to consent to apps

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
|Proxy HTTPS||https://192.168.00.00:4000|
|Proxy HTTP||http://192.168.00.00:4000|
|Asign to variable||Variable|

### List all emails
  
List all email, you can specify a filter
|Parameters|Description|example|
| --- | --- | --- |
|Filter||subject eq 'compras'|
|Order by||importance desc|
|Folder ID||Inbox|
|Number of emails to list||25|
|Asign to variable||Variable|
|session||session|

### List unread emails
  
List all unread emails from your mailbox
|Parameters|Description|example|
| --- | --- | --- |
|Filter||subject eq 'compras'|
|Order by||importance desc|
|Folder ID||Inbox|
|Number of emails to list||25|
|Asign to variable||Variable|
|session||session|

### Read email for ID
  
Read an email usign its ID
|Parameters|Description|example|
| --- | --- | --- |
|Email ID||345|
|Path for download attachment||C:\User\Desktop|
|Download attachments||-|
|Path to download HTML message||C:\User\Desktop|
|Download message as HTML||-|
|Mark as read||-|
|Email HTML body|If this box is marked, will bring the HTML version of email body.||
|Whole email in HTML|If this box is checked, it will return the whole email in HTML version.||
|Email RAW body|If this box is marked, will bring the RAW version of email body.||
|Asign to variable||Variable|
|session||session|

### Send Email
  
Send an email
|Parameters|Description|example|
| --- | --- | --- |
|To||to@mail.com, to1@mail.com|
|Cc||to2@mail.com, to3@mail.com|
|Bcc||to4@mail.com, to5@mail.com|
|Subject||Nuevo mail|
|Body||Esto es una prueba|
|Attached File||C:\User\Desktop\test.txt|
|Folder (Multiple files)||C:\User\Desktop\Files|
|session||session|

### Reply Email
  
Reply an email using its ID
|Parameters|Description|example|
| --- | --- | --- |
|Email ID||345|
|Cc||to2@mail.com, to3@mail.com|
|Bcc||to4@mail.com, to5@mail.com|
|Body||Esto es una prueba|
|Attached File||C:\User\Desktop\test.txt|
|Folder (Multiple files)||C:\User\Desktop\Files|
|Mark as read||-|
|Reply to the sender||-|
|session||session|

### Forward Email
  
Forward an email using its ID
|Parameters|Description|example|
| --- | --- | --- |
|Email ID||345|
|To||to@mail.com, to1@mail.com|
|Cc||to2@mail.com, to3@mail.com|
|Bcc||to4@mail.com, to5@mail.com|
|Body||This is a test.|
|Attached File||C:\User\Desktop\test.txt|
|Folder (Multiple files)||C:\User\Desktop\Files|
|Mark as read||-|
|Asign to variable||Variable|
|session||session|

### Download attachments
  
Download attached files from an email
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

### Download .eml
  
Download an email in .eml format
|Parameters|Description|example|
| --- | --- | --- |
|Email ID||345|
|Ruta de la carpeta||C:/Users/user/Documents/|
|Nombre del archivo||Mail|
|Asign to variable||Variable|
|session||session|

### Email folders list
  
List of email folders
|Parameters|Description|example|
| --- | --- | --- |
|Filter||displayName eq 'Processed'|
|Parent folder|||
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
  
Get the list of Groups that the account is part of
|Parameters|Description|example|
| --- | --- | --- |
|Filter|Filter groups that start with the text entered.||
|Asign to variable||Variable|
|session||session|

### Get group
  
Get Group by its ID
|Parameters|Description|example|
| --- | --- | --- |
|Group ID||ID|
|Asign to variable||Variable|
|session||session|

### Get site
  
Get the site of the Group
|Parameters|Description|example|
| --- | --- | --- |
|Group ID||ID|
|Hostname|Example from the link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH take tusitio.sharepoint.com|tusitio.sharepoint.com|
|Path to site|Example from the link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH take /sites/RecursosHumanos/SubsitioRRHH|/sites/RecursosHumanos/SubsitioRRHH|
|Asign to variable||Variable|
|session||session|

### Get site lists
  
Get the lists of the Site
|Parameters|Description|example|
| --- | --- | --- |
|Group ID||ID|
|Asign to variable||Variable|
|session||session|

### Get lists by Site ID
  
Get the lists of the Site
|Parameters|Description|example|
| --- | --- | --- |
|Site ID||ID|
|Asign to variable||Variable|
|Session||session|

### Get list columns
  
Get the editable columns of a specific List of the Site
|Parameters|Description|example|
| --- | --- | --- |
|Site ID||ID|
|List ID||ID|
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
  
Get the items of a List using its name
|Parameters|Description|example|
| --- | --- | --- |
|Site ID||ID|
|Hostname|Example from the link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH take tusitio.sharepoint.com|tusitio.sharepoint.com|
|Path to site|Example from the link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH take /sites/RecursosHumanos/SubsitioRRHH|/sites/RecursosHumanos/SubsitioRRHH|
|List name||name|
|Limit||10|
|Query filter||field/id1 eq 'value'|
|Order by||column|
|Fields to expand||['id1','id2',...]|
|Asign to variable||Variable|
|session||session|

### Get Item
  
Get an Item, using its ID, from a List
|Parameters|Description|example|
| --- | --- | --- |
|Site ID||ID|
|Hostname|Example from the link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH take tusitio.sharepoint.com|tusitio.sharepoint.com|
|Path to site|Example from the link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH take /sites/RecursosHumanos/SubsitioRRHH|/sites/RecursosHumanos/SubsitioRRHH|
|List name||name|
|Item ID||ID|
|Fields to expand||['id1','id2',...]|
|Asign to variable||Variable|
|session||session|

### Create Item
  
Create an Item in a List
|Parameters|Description|example|
| --- | --- | --- |
|Site ID||ID|
|List name||name|
|Item data||{'title': 'data'}|
|Asign to variable||Variable|
|session||session|

### Delete Item
  
Delete an Item, using its ID, from a List
|Parameters|Description|example|
| --- | --- | --- |
|Site ID||ID|
|List name||name|
|Item ID||ID|
|Asign to variable||Variable|
|session||session|

### Update Item
  
Update an Item data using its ID
|Parameters|Description|example|
| --- | --- | --- |
|Site ID||ID|
|List name||name|
|Item ID||ID|
|Item data||{'title': 'data'}|
|Asign to variable||Variable|
|session||session|

### Get document libraries
  
Get a list of the Document Libraries within the Site
|Parameters|Description|example|
| --- | --- | --- |
|Site ID||ID|
|Hostname|Example from the link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH take tusitio.sharepoint.com|tusitio.sharepoint.com|
|Path to site|Example from the link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH take /sites/RecursosHumanos/SubsitioRRHH|/sites/RecursosHumanos/SubsitioRRHH|
|Asign to variable||Variable|
|session||session|

### Get documents
  
Get a list of the documents within a library
|Parameters|Description|example|
| --- | --- | --- |
|Site ID||ID|
|Hostname|Example from the link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH take tusitio.sharepoint.com|tusitio.sharepoint.com|
|Path to site|Example from the link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH take /sites/RecursosHumanos/SubsitioRRHH|/sites/RecursosHumanos/SubsitioRRHH|
|Library ID|You can get the library ID using the 'Get document libraries' module|ID|
|Start from|Path within the library from where to start getting the documents. Example /Shared Documents/Folder1|Path/to/folder|
|Contains|Get only the documents that contain this text in their name. Leave empty to get all documents.|Text|
|Asign to variable||Variable|
|session||session|

### Upload document
  
Upload a document to a Site library
|Parameters|Description|example|
| --- | --- | --- |
|Site ID||ID|
|Library ID||ID|
|Folder ID||ID|
|Path|||
|Asign to variable||Variable|
|session||session|

### Download or modify document
  
Upload a document to a Site library
|Parameters|Description|example|
| --- | --- | --- |
|Site ID||ID|
|Library ID||ID|
|Item ID||ID|
|Data to modify||{'name': 'new_name.jpg', 'description':'new_description'}|
|Update document data|||
|Target folder ID||ID|
|Move document|||
|Path|||
|Download document|||
|Delete document|||
|Asign to variable||Variable|
|session||session|
