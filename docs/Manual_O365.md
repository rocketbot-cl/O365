



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
2. In the left menu, select "App registrations".
3. Select "New registration".
4. Under “Compatible account types”, choose:
    - "Accounts in any organizational directory (any Azure AD directory: multi-tenant) and personal Microsoft accounts (such as Skype or Xbox)" for this case use Tenant ID = **common**.
    - "Only accounts from this organizational directory (only this account: single tenant) for this case use application-specific **Tenant ID**. (recommended for application authentication)
    - "Personal Microsoft accounts only" for this case use use Tenant ID = **consumers**.
5. Set the redirect uri (Web) as: https://localhost:5001/ and click "Register".
6. Copy the Application (client) ID. You will need this value.
7. Under "Certificates & secrets", generate a new client secret 
and set its expiration. Copy the **VALUE** of the created secret (**not the Secret ID**), since it will be hidden after a few minutes.

### Authentication types

| Type | User sign-in | Recommended use |
| --- | --- | --- |
| Delegated | Required for the first connection and when reauthorization is needed | Processes that run on behalf of a user |
| Application | Not required | Unattended processes using a corporate account |

### Delegated authentication

1. Under "API permissions", select "Microsoft Graph" > "Delegated permissions" and add:
    - `Mail.ReadWrite`
    - `Mail.Send`
    - `User.Read`
2. To use shared mailboxes, also add:
    - `Mail.ReadWrite.Shared`
    - `Mail.Send.Shared`
3. If you will use the SharePoint commands, also add:
    - `Group.Read.All`
    - `Sites.ReadWrite.All`
    - `Sites.Manage.All`
    - `Files.ReadWrite.All`
4. In Rocketbot Studio, insert the "Connect to O365" command and complete:
    - Authentication type: `Delegated`
    - `client_id`
    - `client_secret`
    - `tenant_id`
    - `session`, if required
5. Run the command. An authorization URL will be generated in the Rocketbot console. Copy it and open it in your browser.
6. Accept the requested permissions. The browser will redirect to a page with no content. Copy the complete URL and paste it into the Rocketbot console under **"Paste the authenticated url here:"**.
7. Press Enter. If the authentication is successful, the console will display: "Authentication Flow Completed. Oauth Access Token Stored. You can now use the API."

A credential file named `o365_token.txt` or `o365_token_{session}.txt` will be created in the Rocketbot root folder. If the saved refresh token is revoked or becomes invalid, run the connection command again and complete the authorization process with the new URL.

### Application authentication (app-only)

Application authentication is available only for organizational Microsoft accounts. It does not support personal Microsoft accounts.

1. Under
 "API permissions", select "Microsoft Graph" > "Application permissions" and add:
    - `Mail.ReadWrite`
    - `Mail.Send`
2. If you will use the SharePoint commands, also add:
    - `Group.Read.All`
    - `Sites.ReadWrite.All`
    - `Sites.Manage.All`
    - `Files.ReadWrite.All`
3. Select "Grant admin consent". Administrator consent is required for application permissions.
4. In Rocketbot Studio, insert the "Connect to O365" command and complete:
    - Authentication type: `Application`
    - `client_id`
    - `client_secret`
    - Specific `tenant_id` of the organization
    - `user_id`: User Principal Name (for example, `robot@company.com`) or Object ID of the mailbox the robot will use
    - `session`, if required
5. Run the command. This authentication type does not generate an authorization URL and does not require user sign-in.

The application obtains access tokens using its own credentials. It does not use a delegated refresh token. The "Enable shared mailbox" option applies 
only to delegated authentication.

The `user_id` selects the mailbox used by the module, but it does not restrict the permissions granted to the application. If access must be limited to specific mailboxes, the administrator must configure RBAC for Applications in Exchange Online.

### Additional permissions for Application authentication

With Application authentication, permissions are configured directly in Azure App Registrations. The **Connect to SharePoint** and **Enable shared mailbox** checkboxes in the connection command only add delegated permissions and are not required in this mode.

All permissions listed below must be added from:

1. Go to **Azure Portal > App registrations**.
2. Select the application.
3. Go to **API permissions**.
4. Select **Add a permission > Microsoft Graph**.
5. Select **Application permissions**.
6. Add the required permissions.
7. Select **Grant admin consent** to authorize the permissions.

#### SharePoint

To use SharePoint commands with 
Application authentication, add permissions according to the operations that the robot will perform:

- `Sites.Read.All`: allows reading documents and SharePoint list items.
- `Sites.ReadWrite.All`: allows creating, reading, updating, and deleting documents and list items.
- `Sites.Manage.All`: required to create or delete lists and document libraries.
- `Files.Read.All`: allows reading documents.
- `Files.ReadWrite.All`: allows uploading, modifying, moving, and deleting documents.
- `Group.Read.All`: required when the command retrieves the site using a Microsoft 365 Group ID.

You do not need to add all permissions if the robot will not use all these operations.

In the **Connect to O365** command, leave the **Connect to SharePoint** checkbox unchecked.

Alternatively, you can use the `Sites.Selected` permission to restrict application access to specific sites. In that case, in addition to adding the permission and granting admin consent, an administrator must explicitly grant access 
to each site.

Official documentation:

- [Microsoft Graph permissions reference](https://learn.microsoft.com/en-us/graph/permissions-reference)
- [Selected permissions in OneDrive and SharePoint](https://learn.microsoft.com/en-us/graph/permissions-selected-overview)

#### Shared mailboxes

To use shared mailboxes with Application authentication, add the following permissions:

- `Mail.Read`: allows reading emails only.
- `Mail.ReadWrite`: allows creating, reading, updating, moving, and deleting emails.
- `Mail.Send`: allows sending emails.

To use all email commands in the module, add:

- `Mail.ReadWrite`
- `Mail.Send`

The `Mail.Read.Shared`, `Mail.ReadWrite.Shared`, and `Mail.Send.Shared` permissions apply only to Delegated authentication and should not be selected for Application authentication.

Then, in the **Connect to O365** command, complete `user_id` with the UPN or Object ID of the default user. If the robot will work only with a shared mailbox, you can enter that mailbox's 
email address. Leave the **Enable shared mailbox** checkbox unchecked.

In each email command that includes the **Shared mailbox** field, enter the email address of the mailbox on which the operation will be performed.

Application mail permissions may grant access to all mailboxes in the organization. If access must be limited to specific mailboxes, the administrator must configure an access policy or Application RBAC in Exchange Online.

Official documentation:

- [Microsoft Graph permissions reference](https://learn.microsoft.com/en-us/graph/permissions-reference)
- [Role Based Access Control for Applications in Exchange Online](https://learn.microsoft.com/en-us/exchange/permissions-exo/application-rbac)

### How to filter emails

To filter emails, use the following operators and functions.

1. **Equality operators**

   - Equal (**eq**)
   - Not equal (**ne**)
   - Negation (**not**)
   - In (**in**)
   - Has (**has**)

2. **Relational operators**

   - Less than (**lt**)
   - 
Greater than (**gt**)
   - Less than or equal to (**le**)
   - Greater than or equal to (**ge**)

3. **Conditional operators**

   - And (**and**)
   - Or (**or**)

4. **Functions**

   - Starts with (**startsWith**)
   - Ends with (**endsWith**)
   - Contains (**contains**)

The main properties that can be used to create filters are:

```json
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
```

These properties come from the JSON response returned by the API query. To review the properties of specific emails, go to [Microsoft Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer), sign in with your Azure account, and run the following query:

```text
https://graph.microsoft.com/v1.0/me/messages/<email_ID>
```

It is important to use only single quotation marks (`'`) when specifying the value to filter, except for Boolean values (**true** / **false**). The following are practical examples of how to create filters:

- Unread emails = **isRead eq false**
- Read emails = 
**isRead eq true**
- The subject is equal to... = **subject eq 'example'**
- The subject contains... = **contains(Subject, 'example')**
- The subject starts with the word... = **startswith(Subject, 'example')**
- The received date is between... = **ReceivedDateTime ge \<date> and ReceivedDateTime le \<date>**
- The email body contains... = **contains(Body/Content, 'example')**
- The email sender is equal to... = **From/EmailAddress/Address eq 'example@example.com'**
- The email sender starts with... = **Startswith(From/EmailAddress/Address, 'example')**
- The email has attachments = **HasAttachments eq true**

### How to identify emails (ID)

Emails are identified by a unique and dynamic ID. This means that if some of an email's properties change, its ID will also be affected. The clearest example occurs when an email is moved to another folder. For example, the ID of an email in Inbox will not be the same after it has been moved to the "Processed" folder. To use the email again, run 
the **List Emails** command on the "Processed" folder and obtain its new ID.

When using `filter` and `order by` in the same query to retrieve messages, make sure to specify the properties as follows:

- Properties that appear in `order by` must also appear in `filter`.
- Properties that appear in `order by` must be in the same order as in `filter`.
- Properties included in `order by` must appear in `filter` before any properties that are not included in `order by`.


### Authentication errors

If an authorization error appears during delegated authentication:

![error](imgs/o365error.PNG)

1. Go to Microsoft Entra ID > "App registrations".
2. Select the application.
3. Go to "API permissions".
4. Verify that the required permissions have been added.
5. Grant administrator consent when required.

For application authentication, also verify that a specific organizational Tenant ID and a valid `user_id` are being used.

## Description of the commands

### Connect to O365
  
Connect to O365 application instance
|Parameters|Description|example|
| --- | --- | --- |
|Authentication type|Delegated keeps the previous behavior and uses a user's session. Application uses client credentials, requires user_id, and does not use a refresh token.|--- Select ---|
|client_id||client_id|
|client_secret||client_secret|
|tenant_id||tenant_id|
|Target user (user_id)|Application authentication only. UPN (email) or Object ID of the user on which the robot will operate.|robot@test.com or object ID|
|session||session|
|Connect to Sharepoint|Delegated authentication only. In Application mode, permissions are configured in Azure.|-|
|Enable shared mailbox|Delegated authentication only. In Application mode, permissions are configured in Azure.|-|
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
|Shared Mailbox (Optional)|Shared mailbox email to access|sharedmailbox@outlook|
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
|Shared Mailbox|Shared mailbox email to access|sharedmailbox@outlook|
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
|Shared Mailbox|Shared mailbox email to access|sharedmailbox@outlook|
|Asign to variable||Variable|
|session||session|

### Send Email
  
Send an email
|Parameters|Description|example|
| --- | --- | --- |
|To||to@mail.com, to1@mail.com|
|Cc||to2@mail.com, to3@mail.com|
|Bcc||to4@mail.com, to5@mail.com|
|Shared Mailbox (Optional)|Shared mailbox email from which you want to send the email|sharedmailbox@outlook|
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
|Shared Mailbox (Optional)|Shared mailbox email from which you want to reply the email|sharedmailbox@outlook|
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
|Shared Mailbox (Optional)|Shared mailbox email from which you want to forward the email|sharedmailbox@outlook|
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
|Shared mailbox|Optional. You must provide the email of the shared mailbox.|shared@mailbox.com|
|Asign to variable||Variable|
|session||session|

### Mark as unread
  
Mark an email as unread
|Parameters|Description|example|
| --- | --- | --- |
|Email ID||345|
|Shared mailbox|Optional. You must provide the email of the shared mailbox.|shared@mailbox.com|
|Asign to variable||Variable|
|session||session|

### Download .eml
  
Download an email in .eml format
|Parameters|Description|example|
| --- | --- | --- |
|Email ID||345|
|Ruta de la carpeta||C:/Users/user/Documents/|
|Nombre del archivo||Mail|
|Shared mailbox|Optional. You must provide the email of the shared mailbox.|shared@mailbox.com|
|Asign to variable||Variable|
|session||session|

### Email folders list
  
List of email folders
|Parameters|Description|example|
| --- | --- | --- |
|Filter||displayName eq 'Processed'|
|Parent folder|||
|Shared mailbox|Optional. You must provide the email of the shared mailbox.|shared@mailbox.com|
|Asign to variable||Variable|
|session||session|

### Move email
  
Move an email from one folder to another
|Parameters|Description|example|
| --- | --- | --- |
|Email ID||345|
|Folder ID||345|
|Shared mailbox|Optional. You must provide the email of the shared mailbox.|shared@mailbox.com|
|Asign to variable||Variable|
|session||session|

### Create folder
  
Creates a new folder in the email
|Parameters|Description|example|
| --- | --- | --- |
|Parent folder ID||Inbox or 345...|
|Name of the new folder||new_folder|
|Shared mailbox|Optional. You must provide the email of the shared mailbox.|shared@mailbox.com|
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

### Create folder Sharepoint
  
Create a new SharePoint folder
|Parameters|Description|example|
| --- | --- | --- |
|Parent folder ID||Id de la biblioteca...|
|Parent Folder Item ID||ID de la carpeta contenedora o 'root'|
|Group/Site ID||ID del Grupo de M365|
|Name of the new folder||new_folder|
|Asign to variable||Variable|
|session||session|
