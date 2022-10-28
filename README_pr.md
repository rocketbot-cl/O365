



# O365
  
Conecte-se ao Outlook usando o O365.

*Read this in other languages: [English](README.md), [Portugues](README_pr.md), [Español](README_es.md).*

## Como instalar este módulo
  
__Baixe__ e __instale__ o conteúdo na pasta 'modules' no caminho do Rocketbot.

## Como usar este módulo

Antes de usar este módulo, você precisa registrar seu aplicativo no portal de Registros de Aplicativo do Azure.

1. Entre no portal do Azure e procure o serviço Azure Active Directory.
2. Lá, no menu do lado esquerdo, digite "Registro do Aplicativo".
3. Selecione "Novo registro".
4. Em "Tipos de conta compatíveis" suportados, escolha:
    a. "Contas em qualquer diretório organizacional (qualquer diretório do Azure AD: multilocatário) e contas pessoais da Microsoft (como Skype ou Xbox)" para este caso, use ID de locatário = common
    b. "Somente contas deste diretório organizacional (somente esta conta: locatário único) para este caso usam ID de locatário específico do aplicativo.
5. Defina o uri de redirecionamento (Web) como: https://login.microsoftonline.com/common/oauth2/nativeclient e clique em "Registrar".
6. Copie o ID do aplicativo (cliente). Você vai precisar desse valor.
7. Em "Certificados e segredos", gere um novo segredo do cliente. Defina a validade (de preferência 24 meses). Copie o VALUE do segredo do cliente criado (NÃO o ID do segredo). Ele vai esconder depois de alguns minutos.
8. Em "Permissões de API", clique em "Adicionar uma permissão", selecione "Microsoft Graph", depois em "Permissões delegadas", localize e selecione "Mail.ReadWrite" e "User.Read" e, finalmente, "Adicionar permissões".
9. No Rocketbot Studio, insira o comando "Connect to O365", insira os dados solicitados (ID do cliente, valor secreto e locatário) e execute o comando.
10. No console do Rocketbot será gerado um URL (Exemplo: https://login.microsoftonline.com/common/oauth2/v2.0/authorize?response_type=code&client_id=82f8efcd-6a0d-4532-a62e-3e2aecb4d19f&redirect_uri=https%3A%2F%2Flogin.microsoftonline.com%2Fcommon%2Foauth2%2Fnativeclient&scope=Mail.ReadWrite+User.Read.All&state=3LvNFBfX0qej9Q0rsixmSWjCGJyi0M&access_type=offline), copie e cole no seu navegador.
11. Aceite a concessão de permissões e retornará uma tela sem conteúdo. Copie o URL (Exemplo: https://login.microsoftonline.com/common/oauth2/nativeclient?code=M.R3_SN1.5dcda10b-6567-ce05-3a5b-f67145c62684&state=3LvNFBfX0qej9Q0rsixmSWjCGJyi0M) e cole-o no console do Rocketbot abaixo de "Paste the authenticated url here:".
12. Pressione "enter" e se a operação foi bem sucedida você verá no console: "Authentication Flow Completed. Oauth Access Token Stored. You can now use the API." e será criado um arquivo com suas credenciais, na pasta raiz do Rocketbot, chamado o365_token.txt o o365_token_{session}.txt.


## Overview


1. Conectar a O365  
Conectar-se à instância do aplicativo O365

2. Listar todos os e-mails  
Listar todos os e-mails, você pode especificar um filtro

3. Listar e-mails não lidos  
Liste todos os e-mails não lidos da sua caixa de correio

4. Ler e-mail para identificação  
Ler um e-mail usando seu ID

5. Enviar Email  
Envia un email

6. Responder Email  
Responder um email usando seu ID

7. Reenviar um e-mail  
Reenviar um e-mail usando seu ID

8. Baixar anexos  
Baixar anexos de e-mail

9. Marcarcomo não lido  
Marcar um e-mail como não lido

10. Lista de pastas de e-mail  
Lista de pastas de e-mail

11. Mover e-mail  
Mover um email de uma pasta para outra

12. Criar pasta  
Cria uma nova pasta no e-mail

13. Obter Grupos  
Obter lista de Grupos aos quais a conta pertence

14. Obter Grupos  
Obter Grupo por ID

15. Obter site  
Obter o site do Grupo

16. Obter listas  
Obter as listas do Site

17. Criar List  
Criar uma nova lista

18. Obter itens da lista  
Obter os itens de uma Lista usando seu nome

19. Obter Item  
Obtenha um Item, usando seu ID, de uma lista

20. Criar Item  
Criar um Item dentro de uma Lista

21. Criar Item  
Eliminar um Item, usando seu ID, de uma Lista

22. Actualizar Item  
Actualizar dados do Item usando seu ID  




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