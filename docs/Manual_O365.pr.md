



# O365
  
Conecte-se à sua conta de e-mail do Outlook e ao espaço de trabalho do Sharepoint.  

*Read this in other languages: [English](Manual_O365.md), [Português](Manual_O365.pr.md), [Español](Manual_O365.es.md)*
  
![banner](imgs/Banner_O365.jpg)
## Como instalar este módulo
  
Para instalar o módulo no Rocketbot Studio, pode ser feito de duas formas:
1. Manual: __Baixe__ o arquivo .zip e descompacte-o na pasta módulos. O nome da pasta deve ser o mesmo do módulo e dentro dela devem ter os seguintes arquivos e pastas: \__init__.py, package.json, docs, example e libs. Se você tiver o aplicativo aberto, atualize seu navegador para poder usar o novo módulo.
2. Automático: Ao entrar no Rocketbot Studio na margem direita você encontrará a seção **Addons**, selecione **Install Mods**, procure o módulo desejado e aperte instalar.  


## Como usar este módulo

Antes de usar este módulo, você precisa registrar seu aplicativo no portal de Registros de Aplicativo do Azure.

1. Entre no portal do Azure e procure o serviço Microsoft Entra ID.
2. No menu lateral esquerdo, acesse "Registros de aplicativos".
3. Selecione "Novo registro".
4. Em "Tipos de conta compatíveis", escolha:
    - "Contas em qualquer diretório organizacional (qualquer diretório do Azure AD: multilocatário) e contas pessoais da Microsoft (como Skype ou Xbox)" para este caso, use ID de locatário = **common**.
    - "Somente contas deste diretório organizacional (somente esta conta: locatário único) para este caso usam **ID de locatário específico** do aplicativo. (Recomendado para autenticação de aplicação)
    - "Somente contas pessoais da Microsoft" para este caso, use ID do locatário = **consumers**.
5. Defina o uri de redirecionamento (Web) como: https://localhost:5001/ e clique em "Registrar".
6. Copie o ID do aplicativo (cliente). Você precisará
 desse valor.
7. Em "Certificados e segredos", gere um novo segredo do cliente e defina sua validade. Copie o **VALOR** do segredo criado (**não o ID do segredo**), pois ele ficará oculto após alguns minutos.

### Tipos de autenticação

| Tipo | Login do usuário | Uso recomendado |
| --- | --- | --- |
| Delegada | Necessário para a primeira conexão e quando uma nova autorização for necessária | Processos executados em nome de um usuário |
| Aplicativo | Não necessário | Processos não assistidos que utilizam uma conta corporativa |

### Autenticação delegada

1. Em "Permissões de API", selecione "Microsoft Graph" > "Permissões delegadas" e adicione:
    - `Mail.ReadWrite`
    - `Mail.Send`
    - `User.Read`
2. Para usar caixas de correio compartilhadas, adicione também:
    - `Mail.ReadWrite.Shared`
    - `Mail.Send.Shared`
3. Se você utilizar os comandos do SharePoint, adicione também:
    - `Group.Read.All`
    - `Sites.ReadWrite.All`
    - `Sites.Manage.All`
    - `Files.ReadWrite.All`
4. No Rocketbot Studio, insira o comando "Conectar ao O365" e preencha:
    - Tipo de autenticação: `Delegada`
    - `client_id`
    - `client_secret`
    - `tenant_id`
    - `session`, se necessário
5. Execute o comando. Uma URL de autorização será gerada no console do Rocketbot. Copie-a e abra-a no navegador.
6. Aceite as permissões solicitadas. O navegador redirecionará para uma página sem conteúdo. Copie a URL completa e cole-a no console do Rocketbot abaixo de **"Paste the authenticated url here:"**.
7. Pressione Enter. Se a autenticação for bem-sucedida, o console mostrará: "Authentication Flow Completed. Oauth Access Token Stored. You can now use the API."

Um arquivo de credenciais chamado `o365_token.txt` ou `o365_token_{session}.txt` será criado na pasta raiz do Rocketbot. Se o refresh token armazenado for revogado ou deixar de ser válido, execute novamente o comando de conexão e conclua a autorização com a nova URL.

### Autenticação de aplicativo (app-only)

A autenticação de aplicativo está disponível somente para contas organizacionais da Microsoft. Ela não oferece suporte a contas pessoais da Microsoft.

1. Em "Permissões de API", selecione "Microsoft Graph" > "Permissões de aplicativo" e adicione:
    - `Mail.ReadWrite`
    - `Mail.Send`
2. Se você utilizar os comandos do SharePoint, adicione também:
    - `Group.Read.All`
    - `Sites.ReadWrite.All`
    - `Sites.Manage.All`
    - `Files.ReadWrite.All`
3. Selecione "Conceder consentimento do administrador". As permissões de aplicativo exigem o consentimento do administrador.
4. No Rocketbot Studio, insira o comando "Conectar ao O365" e preencha:
    - Tipo de autenticação: `Aplicativo`
    - `client_id`
    - `client_secret`
    - `tenant_id` específico da organização
    - `user_id`: nome principal do usuário, por exemplo `robot@empresa.com`, ou Object ID da caixa de correio que o robô utilizará
    - `session`, se necessário
5. Execute o comando. Esse tipo de autenticação não 
gera uma URL de autorização e não exige login do usuário.

O aplicativo obtém access tokens usando suas próprias credenciais. Ele não utiliza um refresh token delegado. A opção "Ativar caixa de correio compartilhada" se aplica somente à autenticação delegada.

O `user_id` seleciona a caixa de correio utilizada pelo módulo, mas não limita as permissões concedidas ao aplicativo. Se o acesso precisar ser restrito a caixas de correio específicas, o administrador deverá configurar o RBAC para Aplicativos no Exchange Online.

### Permissões adicionais para autenticação de Aplicação

Na autenticação de Aplicação, as permissões são configuradas diretamente no Azure App Registrations. As caixas de seleção **Conectar ao SharePoint** e **Ativar caixa de correio compartilhada** do comando de conexão adicionam apenas permissões delegadas e não são necessárias neste modo.

Todas as permissões indicadas abaixo devem ser adicionadas em:

1. Acesse **Azure Portal > App registrations**.
2. Selecione o 
aplicativo.
3. Acesse **API permissions**.
4. Selecione **Add a permission > Microsoft Graph**.
5. Selecione **Application permissions**.
6. Adicione as permissões necessárias.
7. Selecione **Grant admin consent** para autorizar as permissões.

#### SharePoint

Para utilizar os comandos do SharePoint com autenticação de Aplicação, adicione as permissões de acordo com as operações que o robô realizará:

- `Sites.Read.All`: permite ler documentos e itens de listas do SharePoint.
- `Sites.ReadWrite.All`: permite criar, ler, modificar e excluir documentos e itens de listas.
- `Sites.Manage.All`: necessária para criar ou excluir listas e bibliotecas de documentos.
- `Files.Read.All`: permite ler documentos.
- `Files.ReadWrite.All`: permite carregar, modificar, mover e excluir documentos.
- `Group.Read.All`: necessária quando o comando obtém o site por meio do ID de um Grupo do Microsoft 365.

Não é necessário adicionar todas as permissões se o robô não utilizar todas essas operações.

No 
comando **Conectar ao O365**, deixe desmarcada a caixa **Conectar ao SharePoint**.

Como alternativa, você pode utilizar a permissão `Sites.Selected` para limitar o acesso do aplicativo a sites específicos. Nesse caso, além de adicionar a permissão e conceder o consentimento do administrador, um administrador deve conceder acesso explicitamente a cada site.

Documentação oficial:

- [Microsoft Graph permissions reference](https://learn.microsoft.com/en-us/graph/permissions-reference)
- [Selected permissions in OneDrive and SharePoint](https://learn.microsoft.com/en-us/graph/permissions-selected-overview)

#### Caixas de correio compartilhadas

Para utilizar caixas de correio compartilhadas com autenticação de Aplicação, adicione as seguintes permissões:

- `Mail.Read`: permite somente ler e-mails.
- `Mail.ReadWrite`: permite criar, ler, modificar, mover e excluir e-mails.
- `Mail.Send`: permite enviar e-mails.

Para utilizar todos os comandos de e-mail do módulo, adicione:

- `Mail.ReadWrite`
- `Mail.Send`

As permissões `Mail.Read.Shared`, `Mail.ReadWrite.Shared` e `Mail.Send.Shared` correspondem somente à autenticação Delegada e não devem ser selecionadas para autenticação de Aplicação.

Em seguida, no comando **Conectar ao O365**, preencha `user_id` com o UPN ou Object ID do usuário padrão. Se o robô trabalhar somente com uma caixa de correio compartilhada, você pode informar o endereço de e-mail dessa caixa. Deixe desmarcada a caixa **Ativar caixa de correio compartilhada**.

Em cada comando de e-mail que inclua o campo **Caixa de correio compartilhada**, informe o endereço de e-mail da caixa na qual a operação será realizada.

As permissões de Aplicação de e-mail podem conceder acesso a todas as caixas de correio da organização. Se for necessário limitar o acesso a caixas específicas, o administrador deverá configurar uma política de acesso ou o Application RBAC no Exchange Online.

Documentação oficial:

- [Microsoft Graph permissions 
reference](https://learn.microsoft.com/en-us/graph/permissions-reference)
- [Role Based Access Control for Applications in Exchange Online](https://learn.microsoft.com/en-us/exchange/permissions-exo/application-rbac)

### Como filtrar e-mails

Para filtrar e-mails, utilize os seguintes operadores e funções.

1. **Operadores de igualdade**

   - Igual (**eq**)
   - Diferente (**ne**)
   - Negação (**not**)
   - Em (**in**)
   - Possui (**has**)

2. **Operadores relacionais**

   - Menor que (**lt**)
   - Maior que (**gt**)
   - Menor ou igual a (**le**)
   - Maior ou igual a (**ge**)

3. **Operadores condicionais**

   - E (**and**)
   - Ou (**or**)

4. **Funções**

   - Começa com (**startsWith**)
   - Termina com (**endsWith**)
   - Contém (**contains**)

As principais propriedades que podem ser utilizadas para criar filtros são:

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

Essas propriedades são obtidas do JSON da resposta retornada pela consulta à API. Para revisar as 
propriedades de e-mails específicos, acesse o [Microsoft Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer), entre com sua conta do Azure e execute a seguinte consulta:

```text
https://graph.microsoft.com/v1.0/me/messages/<ID_email>
```

É importante utilizar somente aspas simples (`'`) ao indicar o valor do filtro, exceto no caso de valores booleanos (**true** / **false**). A seguir, são apresentados exemplos práticos de como criar filtros:

- E-mails não lidos = **isRead eq false**
- E-mails lidos = **isRead eq true**
- O assunto é igual a... = **subject eq 'example'**
- O assunto contém... = **contains(Subject, 'example')**
- O assunto começa com a palavra... = **startswith(Subject, 'example')**
- A data de recebimento está entre... = **ReceivedDateTime ge \<date> and ReceivedDateTime le \<date>**
- O corpo do e-mail contém... = **contains(Body/Content, 'example')**
- O remetente do e-mail é igual a... = **From/EmailAddress/Address eq 
'example@example.com'**
- O remetente do e-mail começa com... = **Startswith(From/EmailAddress/Address, 'example')**
- O e-mail possui anexos = **HasAttachments eq true**

### Como identificar e-mails (ID)

Os e-mails são identificados por um ID único e dinâmico. Isso significa que, se algumas propriedades de um e-mail forem alteradas, seu ID também será afetado. O exemplo mais claro ocorre quando um e-mail é movido para outra pasta. Por exemplo, o ID de um e-mail na Caixa de Entrada não será o mesmo depois que ele for movido para a pasta "Processados". Para utilizar o e-mail novamente, execute o comando **Listar E-mails** na pasta "Processados" e obtenha o novo ID.

Ao utilizar `filtro` e `ordenar por` na mesma consulta para obter mensagens, certifique-se de especificar as propriedades da seguinte forma:

- As propriedades que aparecem em `ordenar por` também devem aparecer em `filtro`.
- As propriedades que aparecem em `ordenar por` devem estar na mesma ordem que em `filtro`.
- As 
propriedades presentes em `ordenar por` devem aparecer em `filtro` antes de qualquer propriedade que não esteja presente em `ordenar por`.

### Erros de autenticação

Se um erro de autorização for exibido durante a autenticação delegada:

![erro](imgs/o365error.PNG)

1. Acesse Microsoft Entra ID > "Registros de aplicativos".
2. Selecione o aplicativo.
3. Acesse "Permissões de API".
4. Verifique se as permissões necessárias foram adicionadas.
5. Conceda o consentimento do administrador quando necessário.

Para autenticação de aplicativo, verifique também se está sendo usado o ID específico do locatário organizacional e um `user_id` válido.
## Descrição do comando

### Conectar a O365
  
Conectar-se à instância do aplicativo O365
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Tipo de autenticação|Delegada mantém o comportamento anterior e utiliza a sessão de um usuário. Aplicação usa client credentials, requer user_id e não utiliza refresh token.|--- Select ---|
|client_id||client_id|
|client_secret||client_secret|
|tenant_id||tenant_id|
|Usuário de destino (user_id)|Autenticação de aplicação apenas. UPN (email) ou Object ID do usuário sobre o qual o robô operará.|robot@test.com or object ID|
|session||session|
|Conectar ao Sharepoint|Somente para autenticação Delegada. No modo Aplicação, as permissões são configuradas no Azure.|-|
|Ativar caixa de correio compartilhada|Somente para autenticação Delegada. No modo Aplicação, as permissões são configuradas no Azure.|-|
|Proxy HTTPS||https://192.168.00.00:4000|
|Proxy HTTP||http://192.168.00.00:4000|
|Atribuir à variável||Variable|

### Listar todos os e-mails
  
Listar todos os e-mails, você pode especificar um filtro
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Filter||subject eq 'compras'|
|Ordenar por||importance desc|
|ID Pasta||Inbox|
|Número de e-mails para listar||25|
|Buzão compartilhado (Opcional)|Email do buzon compartilhado para acesso|sharedmailbox@outlook|
|Atribuir à variável||Variable|
|session||session|

### Listar e-mails não lidos
  
Liste todos os e-mails não lidos da sua caixa de correio
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Filter||subject eq 'compras'|
|Ordenar por||importance desc|
|ID Pasta||Inbox|
|Número de e-mails para listar||25|
|Buzão compartilhado|Email do buzon compartilhado para acesso|sharedmailbox@outlook|
|Atribuir à variável||Variable|
|session||session|

### Ler e-mail para identificação
  
Ler um e-mail usando seu ID
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Identificação do email||345|
|Caminho para download do anexo||C:\User\Desktop|
|Baixar anexos||-|
|Caminho para download mensagem html||C:\User\Desktop|
|Baixar mensagem como HTML||-|
|Marcar como lido||-|
|Corpo do e-mail HTML|Se esta caixa estiver marcada, retornará o corpo do e-mail na versão HTML.||
|E-mail completo em HTML|Se esta caixa estiver marcada, retornará o e-mail completo em versão HTML.||
|Corpo do e-mail RAW|Se esta caixa estiver marcada, retornará o corpo do e-mail na versão RAW.||
|Buzão compartilhado|Email do buzon compartilhado para acesso|sharedmailbox@outlook|
|Atribuir à variável||Variable|
|session||session|

### Enviar Email
  
Envia un email
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Para||to@mail.com, to1@mail.com|
|Cc||to2@mail.com, to3@mail.com|
|Bcc||to4@mail.com, to5@mail.com|
|Buzão compartilhado (Opcional)|Email do buzon compartilhado da qual deseja enviar o email|sharedmailbox@outlook|
|Assunto||Nuevo mail|
|Mensagem||Esto es una prueba|
|Attached File||C:\User\Desktop\test.txt|
|Pasta (vários arquivos)||C:\User\Desktop\Files|
|session||session|

### Responder Email
  
Responder um email usando seu ID
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Identificação do email||345|
|Cc||to2@mail.com, to3@mail.com|
|Bcc||to4@mail.com, to5@mail.com|
|Buzão compartilhado (Opcional)|Email do buzon compartilhado da qual deseja responder o email|sharedmailbox@outlook|
|Mensagem||Esto es una prueba|
|Attached File||C:\User\Desktop\test.txt|
|Pasta (vários arquivos)||C:\User\Desktop\Files|
|Marcar como lido||-|
|Responder ao remeteste||-|
|session||session|

### Reenviar um e-mail
  
Reenviar um e-mail usando seu ID
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Identificação do email||345|
|Para||to@mail.com, to1@mail.com|
|Cc||to2@mail.com, to3@mail.com|
|Bcc||to4@mail.com, to5@mail.com|
|Buzão compartilhado (Opcional)|Email do buzon compartilhado da qual deseja reenviar o email|sharedmailbox@outlook|
|Mensagem||This is a test.|
|Attached File||C:\User\Desktop\test.txt|
|Pasta (vários arquivos)||C:\User\Desktop\Files|
|Marcar como lido||-|
|Atribuir à variável||Variable|
|session||session|

### Baixar anexos
  
Baixar anexos de e-mail
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Identificação do email||345|
|Caminho para download do anexo||C:\User\Desktop|
|Marcar como lido||-|
|Buzão compartilhado|Opcional. Deve ser fornecido o email do buzon compartilhado.|shared@mailbox.com|
|Atribuir à variável||Variable|
|session||session|

### Marcarcomo não lido
  
Marcar um e-mail como não lido
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Identificação do email||345|
|Buzão compartilhado|Opcional. Deve ser fornecido o email do buzon compartilhado.|shared@mailbox.com|
|Atribuir à variável||Variable|
|session||session|

### Baixar .eml
  
Baixe um e-mail no formato .eml
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Identificação do email||345|
|Caminho da pasta||C:/Users/user/Documents/|
|Nome do arquivo||Mail|
|Buzão compartilhado|Opcional. Deve ser fornecido o email do buzon compartilhado.|shared@mailbox.com|
|Atribuir à variável||Variable|
|session||session|

### Lista de pastas de e-mail
  
Lista de pastas de e-mail
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Filter||displayName eq 'Processed'|
|Pasta pai|||
|Buzão compartilhado|Opcional. Deve ser fornecido o email do buzon compartilhado.|shared@mailbox.com|
|Atribuir à variável||Variable|
|session||session|

### Mover e-mail
  
Mover um email de uma pasta para outra
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Identificação do email||345|
|Identificação da pasta||345|
|Buzão compartilhado|Opcional. Deve ser fornecido o email do buzon compartilhado.|shared@mailbox.com|
|Atribuir à variável||Variable|
|session||session|

### Criar pasta
  
Cria uma nova pasta no e-mail
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID pasta Pai||Inbox or 345...|
|Nome da nova pasta||new_folder|
|Buzão compartilhado|Opcional. Deve ser fornecido o email do buzon compartilhado.|shared@mailbox.com|
|Atribuir à variável||Variable|
|session||session|

### Obter Grupos
  
Obter lista de Grupos aos quais a conta pertence
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|Filtro|Filtrar os grupos que comezan con o texto introducido.||
|Atribuir à variável||Variable|
|session||session|

### Obter Grupos
  
Obter Grupo por ID
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID do grupo||ID|
|Atribuir à variável||Variable|
|session||session|

### Obter site
  
Obter o site do Grupo
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID do grupo||ID|
|Hostname|Exemplo do link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH tirar tusitio.sharepoint.com|tusitio.sharepoint.com|
|Rota ao sitio|Exemplo do link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH tirar /sites/RecursosHumanos/SubsitioRRHH|/sites/RecursosHumanos/SubsitioRRHH|
|Atribuir à variável||Variable|
|session||session|

### Obter listas
  
Obter as listas do Site
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID do grupo||ID|
|Atribuir à variável||Variable|
|session||session|

### Obter listas por ID do Sítio
  
Obter as listas do Site
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID do Sítio||ID|
|Atribuir à variável||Variable|
|Session||session|

### Obter colunas da lista
  
Obtenha as colunas editáveis de uma Lista específica do Site
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID do Sítio||ID|
|ID da lista||ID|
|Atribuir à variável||Variable|
|session||session|

### Criar List
  
Criar uma nova lista
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID do Sítio||ID|
|Dados da lista||{'displayName': 'example_name'}|
|Atribuir à variável||Variable|
|session||session|

### Obter itens da lista
  
Obter os itens de uma Lista usando seu nome
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID do Sítio||ID|
|Hostname|Exemplo do link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH tirar tusitio.sharepoint.com|tusitio.sharepoint.com|
|Rota ao sitio|Exemplo do link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH tirar /sites/RecursosHumanos/SubsitioRRHH|/sites/RecursosHumanos/SubsitioRRHH|
|Nome da lista||name|
|Limite||10|
|Filtro do consulta||field/id1 eq 'value'|
|Ordenar por||column|
|Campos para expandir||['id1','id2',...]|
|Atribuir à variável||Variable|
|session||session|

### Obter Item
  
Obtenha um Item, usando seu ID, de uma lista
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID do Sítio||ID|
|Hostname|Exemplo do link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH tirar tusitio.sharepoint.com|tusitio.sharepoint.com|
|Rota ao sitio|Exemplo do link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH tirar /sites/RecursosHumanos/SubsitioRRHH|/sites/RecursosHumanos/SubsitioRRHH|
|Nome da lista||name|
|ID do Item||ID|
|Campos para expandir||['id1','id2',...]|
|Atribuir à variável||Variable|
|session||session|

### Criar Item
  
Criar um Item dentro de uma Lista
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID do Sítio||ID|
|Nome da lista||name|
|Dados do Item||{'title': 'data'}|
|Atribuir à variável||Variable|
|session||session|

### Criar Item
  
Eliminar um Item, usando seu ID, de uma Lista
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID do Sítio||ID|
|Nome da lista||name|
|ID do Item||ID|
|Atribuir à variável||Variable|
|session||session|

### Actualizar Item
  
Actualizar dados do Item usando seu ID
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID do Sítio||ID|
|Nome da lista||name|
|ID do Item||ID|
|Dados do Item||{'title': 'data'}|
|Atribuir à variável||Variable|
|session||session|

### Obter bibliotecas de documentos
  
Obtenha uma lista das Bibliotecas de Documentos dentro do Site
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID do Sítio||ID|
|Hostname|Exemplo do link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH tirar tusitio.sharepoint.com|tusitio.sharepoint.com|
|Rota ao sitio|Exemplo do link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH tirar /sites/RecursosHumanos/SubsitioRRHH|/sites/RecursosHumanos/SubsitioRRHH|
|Atribuir à variável||Variable|
|session||session|

### Obter documentos
  
Obtenha uma lista dos documentos dentro de uma biblioteca
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID do Sítio||ID|
|Hostname|Exemplo do link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH tirar tusitio.sharepoint.com|tusitio.sharepoint.com|
|Rota ao sitio|Exemplo do link https//tusitio.sharepoint.com/sites/RecursosHumanos/SubsitioRRHH tirar /sites/RecursosHumanos/SubsitioRRHH|/sites/RecursosHumanos/SubsitioRRHH|
|ID do Biblioteca|Você pode obter o ID da biblioteca usando o módulo 'Obter bibliotecas de documentos'|ID|
|Começar de|Caminho dentro da biblioteca de onde começar a obter os documentos. Exemplo /Documentos compartilhados/Pasta1|Path/to/folder|
|Contém|Obter apenas os documentos que contêm este texto em seu nome. Deixe vazio para obter todos os documentos.|Text|
|Atribuir à variável||Variable|
|session||session|

### Carregar documentos
  
Carregar um documento para uma biblioteca do Site
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID do Sítio||ID|
|ID do Biblioteca||ID|
|ID da Pasta||ID|
|Caminho|||
|Atribuir à variável||Variable|
|session||session|

### Baixe ou modifique o documento
  
Carregar um documento para uma biblioteca do Site
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID do Sítio||ID|
|ID do Biblioteca||ID|
|ID do Item||ID|
|Dados para modificar||{'name': 'new_name.jpg', 'description':'new_description'}|
|Atualizar dados do documento|||
|ID da pasta de destino||ID|
|Mover documento|||
|Caminho|||
|Baixar documento|||
|Excluir documento|||
|Atribuir à variável||Variable|
|session||session|

### Criar pasta do SharePoint
  
Crie uma nova pasta do SharePoint.
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|ID pasta Pai||Id de la biblioteca...|
|ID Pasta Contenedora||ID de la carpeta contenedora o 'root'|
|ID do Grupo/Local||ID del Grupo de M365|
|Nome da nova pasta||new_folder|
|Atribuir à variável||Variable|
|session||session|
