# O365
  
Connect to Outlook through O365.  

## How to install this module
  
__Download__ and __install__ the content in 'modules' folder in Rocketbot path  


## How to use this module

Before using this module, you need to register your app in the Azure App Registrations portal.

1. Sign in to the Azure portal and search for the Azure Active Directory service.
2. On the left side menu, get into "App Registrations".
3. Select "New record".
4. Under “Compatible account types” supported choose:
    - "Accounts in any organizational directory (any Azure AD directory: multi-tenant) and personal Microsoft accounts (such as Skype or Xbox)" for this case use Tenant ID = **common**.
    - "Only accounts from this organizational directory (only this account: single tenant) for this case use application-specific **Tenant ID**.
5. Set the redirect uri (Web) as: https://login.microsoftonline.com/common/oauth2/nativeclient and click "Register".
6. Copy the application (client) ID. You will need this value.
7. Under "Certificates and secrets", generate a new client secret. Set the expiration (preferably 24 months). Copy the **VALUE** of the created client secret (**__NOT the Secret ID__**). It will hide after a few minutes.
8. Under "API permissions", click "Add a permission", select "Microsoft Graph", then "Delegated permissions", find and select "Mail.ReadWrite" and "User.Read", and finally " Add permissions".
9.  In Rocketbot Studio, insert the "Connect to O365" command, enter the requested data (client ID, secret value, and tenant), and run the command.
10. In the Rocketbot console a url will be generated, copy and paste it into your browser.
    - **Example:** <sub>https://login.microsoftonline.com/common/oauth2/v2.0/authorize?response_type=code&client_id=82f8efcd-6a0d-4532-a62e-3e2aecb4d19f&redirect_uri=https%3A%2F%2Flogin.microsoftonline.com%2Fcommon%2Foauth2%2Fnativeclient&scope=Mail.ReadWrite+User.Read.All&state=3LvNFBfX0qej9Q0rsixmSWjCGJyi0M&access_type=offline</sub>
11. Accept the permissions granting and it will return a screen without content. Copy the URL and Paste it into Rocketbot console below **"Paste the authenticated url here:"**.
    - **Example:** <sub>https://login.microsoftonline.com/common/oauth2/nativeclient?code=M.R3_SN1.5dcda10b-6567-ce05-3a5b-f67145c62684&state=3LvNFBfX0qej9Q0rsixmSWjCGJyi0M</sub>
12. Press "enter" and if the operation was successful you will see in the console: "Authentication Flow Completed. Oauth Access Token Stored. You can now use the API." and a file will have been created with your credentials, in the root folder of Rocketbot, called o365_token.txt or o365_token_{session}.txt.


## Overview


1. Connect to O365  
Connect to O365 application instance

2. List all emails  
List all email, you can specify a filter

3. List unread emails  
List all unread emails from your mailbox

4. Read email for ID  
Read an email usign its ID

5. Send Email  
Send an email

6. Reply Email  
Reply an email using its ID

7. Forward Email  
Forward an email using its ID

8. Download attachments  
Download attached files from an email

9. Mark as unread  
Mark an email as unread

10. Email folders list  
List of email folders

11. Move email  
Move an email from one folder to another

12. Create folder  
Creates a new folder in the email

13. Get groups  
Get the list of Groups that the account is part of

14. Get group  
Get Group by its ID

15. Get site  
Get the site of the Group

16. Get site lists  
Get the lists of the Site

17. Create List  
Create a new list

18. Get list Items  
Get the items of a List using its name

19. Get Item  
Get an Item, using its ID, from a List

20. Create Item  
Create an Item in a List

21. Delete Item  
Delete an Item, using its ID, from a List

22. Update Item  
Update an Item data using its ID  




----
### OS

- windows
- mac
- linux
- docker

### Dependencies
- [**bs4**](https://pypi.org/project/bs4/)
- [**O365**](https://pypi.org/project/O365/)
### License
  
![MIT](https://camo.githubusercontent.com/107590fac8cbd65071396bb4d04040f76cde5bde/687474703a2f2f696d672e736869656c64732e696f2f3a6c6963656e73652d6d69742d626c75652e7376673f7374796c653d666c61742d737175617265)  
[MIT](http://opensource.org/licenses/mit-license.ph)