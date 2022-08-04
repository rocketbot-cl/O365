# coding: utf-8
"""
Base para desarrollo de modulos externos.
Para obtener el modulo/Funcion que se esta llamando:
     GetParams("module")

Para obtener las variables enviadas desde formulario/comando Rocketbot:
    var = GetParams(variable)
    Las "variable" se define en forms del archivo package.json

Para modificar la variable de Rocketbot:
    SetVar(Variable_Rocketbot, "dato")

Para obtener una variable de Rocketbot:
    var = GetVar(Variable_Rocketbot)

Para obtener la Opcion seleccionada:
    opcion = GetParams("option")


Para instalar librerias se debe ingresar por terminal a la carpeta "libs"
    
   sudo pip install <package> -t .

"""

base_path = tmp_global_obj["basepath"]
cur_path = base_path + "modules" + os.sep + "O365" + os.sep + "libs" + os.sep
if cur_path not in sys.path:
    sys.path.append(cur_path)
from enum import Enum
from O365 import Account

from bs4 import BeautifulSoup
import os

module = GetParams("module")
global credentials
global account

if module == "connect":
    client_id = GetParams("client_id")
    client_secret = GetParams("client_secret")
    tenant = GetParams("tenant")
    try:
        credentials = (client_id, client_secret)
        account = Account(credentials, tenant_id = tenant)
        if not account.is_authenticated:
            account.authenticate(scopes=['basic', 'message_all'])
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "sendEmail":
    to_ = GetParams("to_")
    cc = GetParams("cc")
    subject = GetParams("subject")
    body = GetParams("body")
    attached_file = GetParams("attached_file")
    attached_folder = GetParams("attached_folder")
    try:
        message = account.new_message()
        list_mails = to_.split(",")
        message.to.add(list_mails)
        message.subject = subject
        message.body = body
        if attached_file:
            message.attachments.add(attached_file)
        if attached_folder:
            filenames = []
            for f in os.listdir(attached_folder):
                f = os.path.join(attached_folder, f)
                filenames.append(f)
            message.attachments.add(filenames)
        message.send()
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e


if module == "getFolders":
    
    from O365 import utils

    def get_folders_new(mailbox, limit=None, *, query=None, order_by=None, batch=None):

        NEXT_LINK_KEYWORD = '@odata.nextLink'
        
        if mailbox.root:
            url = mailbox.build_url(mailbox._endpoints.get('root_folders'))
        else:
            url = mailbox.build_url(
                mailbox._endpoints.get('child_folders').format(id=mailbox.folder_id))

        if limit is None or limit > mailbox.protocol.max_top_value:
            batch = mailbox.protocol.max_top_value

        params = {'$top': batch if batch else limit}

        if order_by:
            params['$orderby'] = order_by

        if query:
            if isinstance(query, str):
                params['$filter'] = query
            else:
                params.update(query.as_params())

        response = mailbox.con.get(url, params=params)
        if not response:
            return []

        data = response.json()
        
        # Everything received from cloud must be passed as self._cloud_data_key
        self_class = getattr(mailbox, 'folder_constructor', type(mailbox))
        
        folders = [self_class(parent=mailbox, **{mailbox._cloud_data_key: folder}) for
                folder in data.get('value', [])]
        
        next_link = data.get(NEXT_LINK_KEYWORD, None)
        
        if batch and next_link:
            return utils.Pagination(parent=mailbox, data=folders, constructor=self_class,
                            next_link=next_link, limit=limit)
        else:
            return self_class
    
    
    res = GetParams('folders')
    
    list_folders = get_folders_new(account.mailbox())
    print(list_folders)
    
    SetVar(res, list_folders)

if module == "getAllEmails":
    folder = GetParams("folder")
    res = GetParams("res")
    filter = GetParams("filter")
    
    OutlookWellKnowFolderNames = {
        'Inbox': 'Inbox',
        'Junk': 'JunkEmail',
        'Deleted Items': 'DeletedItems',
        'Drafts': 'Drafts',
        'Sent': 'SentItems',
        'Outbox': 'Outbox',
        'Archive': 'Archive'
    }
    
    if OutlookWellKnowFolderNames.get(folder) == None:
        pass
    else:
        folder = OutlookWellKnowFolderNames.get(folder)
    
    if folder == "" or folder == None:
        folder = "Inbox"
    
    try:
        list_messages = account.mailbox().folder_constructor(parent=account.mailbox(), name=folder,
                                                             folder_id=folder).get_messages(query=filter)
        list_object_id = []
        for message in list_messages:
            list_object_id.append(message.object_id)
        SetVar(res, list_object_id)
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "readEmail":
      
    att_folder = GetParams("att_folder")
    res = GetParams("res")
    id_ = GetParams("id_")
    read = GetParams("markasread")
    
    try:
        message = account.mailbox().get_message(id_, download_attachments=True)
        files = []
        for att in message.attachments:
            files.append(att.name)
            att.save(att_folder)
        message_all = {
            'sender': message.sender.address,
            'cc': message.cc,
            'subject': message.subject,
            'sent_time': message.sent,
            'received': message.received,
            'body': BeautifulSoup(message.body, "html.parser").body.get_text(),
            'files': files
        }
        if read == True:
            message.mark_as_read()
        
        SetVar(res, message_all)
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e
