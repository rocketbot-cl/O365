



# O365
  
Connect to Outlook for O365.  
  
![banner](/docs/imgs/Banner_O365.png)
## Como instalar este módulo
  
__Baixe__ e __instale__ o conteúdo na pasta 'modules' no caminho do Rocketbot  




## Como usar este módulo

Antes de usar este módulo, você precisa registrar seu aplicativo no portal de Registros de 
Aplicativo do Azure.

1. Entre no portal do Azure (Registro de Aplicativos: 
https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade ).
2. Selecione "Novo registro".
3. Em
 "Tipos de conta compatíveis" suportados, escolha:
    uma. "Contas em qualquer diretório organizacional (qualquer 
diretório do Azure AD: multilocatário) e contas pessoais da Microsoft (como Skype ou Xbox)" para este caso, use ID de 
locatário = comum
    b. "Somente contas deste diretório organizacional (somente esta conta: locatário único) para este 
caso usam ID de locatário específico do aplicativo.
4. Defina o uri de redirecionamento (Web) como: 
https://login.microsoftonline.com/common/oauth2/nativeclient e clique em "Registrar".
5. Copie o ID do aplicativo 
(cliente). Você vai precisar desse valor.
6. Em "Certificados e segredos", gere um novo segredo do cliente. Defina a 
validade (de preferência 24 meses). Copie o VALUE do segredo do cliente criado (NÃO o ID do segredo). Ele vai esconder 
depois de alguns minutos.
7. Em "Permissões de API", clique em "Adicionar uma permissão", selecione "Microsoft Graph", 
depois em "Permissões delegadas", localize e selecione "Mail.ReadWrite" e "User.Read" e, finalmente, "Adicionar 
permissões".
8. No console do Rocketbot será gerado um URL (Exemplo: 
https://login.microsoftonline.com/common/oauth2/v2.0/authorize?response_type=code&client_id=82f8efcd-6a0d-4532-a62e-3e2aecb4d19f&redirect_uri=https%3A%2F%2Flogin.microsoftonline.com%2Fcommon%2Foauth2%2Fnativeclient&scope=Mail.ReadWrite+User.Read.All&state=3LvNFBfX0qej9Q0rsixmSWjCGJyi0M&access_type=offline),
 copie e cole no seu navegador.
9. Aceite a concessão de permissões e retornará uma tela sem conteúdo. Copie o URL 
(Exemplo: 
https://login.microsoftonline.com/common/oauth2/nativeclient?code=M.R3_SN1.5dcda10b-6567-ce05-3a5b-f67145c62684&state=3LvNFBfX0qej9Q0rsixmSWjCGJyi0M)
 e cole-o no console do Rocketbot abaixo de "Paste the authenticated url here:".
10. Pressione "enter" e se a operação 
foi bem sucedida você verá no console: "Authentication Flow Completed. Oauth Access Token Stored. You can now use the 
API." e será criado um arquivo com suas credenciais, na pasta raiz do Rocketbot, chamado o365_token.txt
## Descrição do comando

### Conectar a O365
  
Conectar-se à instância do aplicativo O365
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|client_id||client_id|
|client_secret||client_secret|
|tenant_id||tenant_id|

### Enviar Email
  
Envia un email
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Para||to@mail.com, to2@mail.com|
|Assunto||Nuevo mail|
|Mensagem||Esto es una prueba|
|Attached File||C:\User\Desktop\test.txt|
|Pasta (vários arquivos)||C:\User\Desktop\Files|

### Lista de pastas de e-mail
  
Lista de pastas de e-mail
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Atribuir à variável||Variable|

### Listar todos os e-mails
  
Listar todos os e-mails, você pode especificar um filtro
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Filter||subject eq 'compras'|
|ID Pasta||Inbox|
|Atribuir à variável||Variable|

### Ler e-mail para identificação
  
Ler e-mail para identificação
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Identificação do email||345|
|Caminho para download do anexo||C:\User\Desktop|
|Atribuir à variável||Variable|
|Marcar como lido||-|