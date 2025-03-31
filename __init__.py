# coding: utf-8
"""
Base para desarrollo de módulos externos.
Para obtener el modulo/Función que se esta llamando:
     GetParams("module")

Para obtener las variables enviadas desde formulario/comando Rocketbot:
    var = GetParams(variable)
    Las "variable" se define en forms del archivo package.json

Para modificar la variable de Rocketbot:
    SetVar(Variable_Rocketbot, "dato")

Para obtener una variable de Rocketbot:
    var = GetVar(Variable_Rocketbot)

Para obtener la Opción seleccionada:
    opcion = GetParams("option")


Para instalar librerías se debe ingresar por terminal a la carpeta "libs"
    
   sudo pip install <package> -t .

"""
from bs4 import BeautifulSoup
import traceback
import sys
import os
import re

base_path = tmp_global_obj["basepath"]
cur_path = base_path + "modules" + os.sep + "O365" + os.sep + "libs" + os.sep
if cur_path not in sys.path:
    sys.path.append(cur_path)

try:
    from O365 import Account
    from O365.utils.attachment import BaseAttachment, UploadSessionRequest
    from O365.drive import Storage
except:
    traceback.print_exc()
    
module = GetParams("module")

global mod_o365_session
global OutlookWellKnowFolderNames


OutlookWellKnowFolderNames= {
        'Inbox': 'Inbox',
        'Junk': 'JunkEmail',
        'Deleted Items': 'DeletedItems',
        'Drafts': 'Drafts',
        'Sent': 'SentItems',
        'Outbox': 'Outbox',
        'Archive': 'Archive'
    }

session = GetParams("session")
if not session:
    session = ''

try:
    if not mod_o365_session : #type:ignore
        mod_o365_session = {}
except NameError:
    mod_o365_session = {}

from email.utils import make_msgid
import base64
import re  
global get_regex_group
def get_regex_group(regex, string):
    matches = re.finditer(regex, string, re.MULTILINE)
    return [[group for group in match.groups()] for match in matches]

if module == "connect":
    client_id = GetParams("client_id")
    client_secret = GetParams("client_secret")
    tenant = GetParams("tenant")
    sharepoint_ = GetParams('sharepoint')
    res = GetParams("res")
    
    if session == '':
        filename = "o365_token.txt"
    else:
        filename = "o365_token_{s}.txt".format(s=session)
    
    filename = os.path.join(base_path, filename)
    # offline_access scope is needed to get the refresh token. That token is used to get a new token automatically with every connection (leaving out the first one).  
    scopes_ = ['offline_access', 'User.Read', 'Mail.ReadWrite', 'Mail.Send']
    
    if sharepoint_ and eval(sharepoint_) == True:
        share_scopes = ['Group.Read.All', 'Sites.ReadWrite.All', 'Sites.Manage.All', 'Files.ReadWrite.All']
        scopes_.extend(share_scopes)         
    
    try:
        credentials = (client_id, client_secret)
        mod_o365_session[session] = Account(credentials, tenant_id = tenant, token_filename = filename)
        if not mod_o365_session[session].is_authenticated:
            mod_o365_session[session].authenticate(scopes=scopes_)
        SetVar(res, mod_o365_session[session].is_authenticated) 
    except Exception as e:
        SetVar(res, mod_o365_session[session].is_authenticated)
        traceback.print_exc()
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

# https://learn.microsoft.com/en-us/graph/api/resources/mail-api-overview?view=graph-rest-1.0

if module == "sendEmail":
    to_ = GetParams("to_")
    cc_ = GetParams("cc")
    bcc_ = GetParams("bcc")
    subject = GetParams("subject")
    body = GetParams("body")
    attached_file = GetParams("attached_file")
    attached_folder = GetParams("attached_folder")
    
    try:
        message = mod_o365_session[session].new_message()
        if not to_:
            raise Exception("'To' field must not be empty.")
        list_to = [to.strip() for to in to_.split(",")]
        message.to.add(list_to)
        if cc_:
            list_cc = [cc.strip() for cc in cc_.split(",")]
            message.cc.add(list_cc)
        if bcc_:
            list_bcc = [bcc.strip() for bcc in bcc_.split(",")]
            message.bcc.add(list_bcc)
        message.subject = subject
        
        if not body:
            body = ""
        
        if not "src" in body:
            message.body = body
        else:
            index = 0
            for match in get_regex_group(r"src=\"(.*)\"", body):
                path = match[0]
                
                if path.startswith(("http", "https")):
                    continue
                else:
                    image_cid = make_msgid()
                    body = body.replace(path, "cid:" + image_cid[1:-1])

                    message.attachments.add(path)
                    message.attachments[index].is_inline = True
                    message.attachments[index].content_id = image_cid[1:-1]
                index += 1
                
            message.body = body
            
        if attached_file:
            size = os.path.getsize(attached_file)
            if size > 3000000: 
                att = BaseAttachment(attachment=attached_file, parent=message)
                UploadSessionRequest(message, att)
                message.attachments.add(attached_file)
            else:
                message.attachments.add(attached_file)
        if attached_folder:
            filenames = []
            for f in os.listdir(attached_folder):
                f = os.path.join(attached_folder, f)
                filenames.append(f)
                
                size = os.path.getsize(f)
                if size > 3000000:        
                    att = BaseAttachment(attachment=f, parent=message)
                    UploadSessionRequest(message, att)

            message.attachments.add(filenames)
            
        message.send()
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "replyEmail":
    id_ = GetParams("id_")
    cc_ = GetParams("cc")
    bcc_ = GetParams("bcc")
    body = GetParams("body")
    attached_file = GetParams("attached_file")
    attached_folder = GetParams("attached_folder")
    read = GetParams("markasread")
    not_to_all = GetParams("not_to_all")
    
    if not body:
        body = ""
    
    if not id_:
        raise Exception("Missing Email ID...")
    
    to_all = True
    if not_to_all and eval(not_to_all):
        to_all = False
    
    try:
        message = mod_o365_session[session].mailbox().get_message(id_)
        # By default the behaviour is to reply all
        reply = message.reply(to_all)
        if cc_:
            list_cc = [cc.strip() for cc in cc_.split(",")]
            reply.cc.add(list_cc)
        if bcc_:
            list_bcc = [bcc.strip() for bcc in bcc_.split(",")]
            reply.bcc.add(list_bcc)
                    
        if not "src" in body:
            reply.body = body + "\n"
        else:
            index = 0
            for match in get_regex_group(r"src=\"(.*)\"", body):
                path = match[0]
                
                if path.startswith(("http", "https")):
                    continue
                else:
                    image_cid = make_msgid()
                    body = body.replace(path, "cid:" + image_cid[1:-1])

                    reply.attachments.add(path)
                    reply.attachments[index].is_inline = True
                    reply.attachments[index].content_id = image_cid[1:-1]
                index += 1
                          
            reply.body = body + "\n"
        
        if attached_file:
            size = os.path.getsize(attached_file)
            if size > 3000000: 
                att = BaseAttachment(attachment=attached_file, parent=reply)
                UploadSessionRequest(reply, att)
                reply.attachments.add(attached_file)
            else:
                reply.attachments.add(attached_file)
        if attached_folder:
            filenames = []
            for f in os.listdir(attached_folder):
                f = os.path.join(attached_folder, f)
                filenames.append(f)
                
                size = os.path.getsize(f)
                if size > 3000000:        
                    att = BaseAttachment(attachment=f, parent=reply)
                    UploadSessionRequest(reply, att)
                
            reply.attachments.add(filenames)
        reply.send()
        
        if read:
            if eval(read):
                message.mark_as_read()
        
    except Exception as e:
        traceback.print_exc()
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "forwardEmail":
    to_ = GetParams("to_")
    cc_ = GetParams("cc")
    bcc_ = GetParams("bcc")
    id_ = GetParams("id_")
    body = GetParams("body")
    attached_file = GetParams("attached_file")
    attached_folder = GetParams("attached_folder")
    read = GetParams("markasread")
    res = GetParams("res")
    
    import time
    
    if not body:
        body = ""
    
    if not id_:
        raise Exception("Missing Email ID...")
    
    try:
        message = mod_o365_session[session].mailbox().get_message(id_)
        forward = message.forward()
        if not to_:
            raise Exception("'To' field must not be empty.")
        list_to = to_.split(",")
        forward.to.add(list_to)
        if cc_:
            list_cc = [cc.strip() for cc in cc_.split(",")]
            forward.cc.add(list_cc)
        if bcc_:
            list_bcc = [bcc.strip() for bcc in bcc_.split(",")]
            forward.bcc.add(list_bcc)
            
        if not "src" in body:
            forward.body = body + "\n" 
        else:
            index = 0
            for match in get_regex_group(r"src=\"(.*)\"", body):
                path = match[0]
                
                if path.startswith(("http", "https")):
                    continue
                else:
                    image_cid = make_msgid()
                    body = body.replace(path, "cid:" + image_cid[1:-1])
                    forward.attachments.add(path)
                    forward.attachments[index].is_inline = True
                    forward.attachments[index].content_id = image_cid[1:-1]
                index += 1
        
            forward.body = body + "\n"

        if attached_file:
            size = os.path.getsize(attached_file)
            if size > 3000000: 
                att = BaseAttachment(attachment=attached_file, parent=forward)
                UploadSessionRequest(forward, att)
                forward.attachments.add(attached_file)
            else:
                forward.attachments.add(attached_file)
        if attached_folder:
            filenames = []
            for f in os.listdir(attached_folder):
                f = os.path.join(attached_folder, f)
                filenames.append(f)
                
                size = os.path.getsize(f)
                if size > 3000000:        
                    att = BaseAttachment(attachment=f, parent=forward)
                    UploadSessionRequest(forward, att)
                
            forward.attachments.add(filenames)
        forward.send()
        
        time.sleep(5)
        
        list_messages = mod_o365_session[session].mailbox().sent_folder().get_messages(limit=1, order_by="lastModifiedDateTime desc")
        for message in list_messages:
            id_f = message.object_id
            
        if read:
            if eval(read):
                message.mark_as_read()
        
        SetVar(res, id_f)
    except Exception as e:
        SetVar(res, False)
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "getAllEmails":
    folder = GetParams("folder")
    res = GetParams("res")
    limit = GetParams("limit")
    filter = GetParams("filtro") or GetParams("filter")
    order = GetParams("order")
    
    folder_ = OutlookWellKnowFolderNames.get(folder)

    if not folder:
        folder = "Inbox"
    elif folder_:
        folder = folder_
    
    if order == "" or not order:
        order = "lastModifiedDateTime desc"
    
    if filter and "lastModifiedDateTime" not in filter:
        filter = "lastModifiedDateTime gt 1900-01-01T00:00:00Z and " + filter
    
    if limit and limit != "":
        limit = int(limit)
    else:
        limit = 25
    
    try:
        list_messages = mod_o365_session[session].mailbox().get_folder(folder_id=folder).get_messages(limit=limit, query=filter, order_by=order)
        list_object_id = []
        for message in list_messages:
            list_object_id.append(message.object_id)
        SetVar(res, list_object_id)
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "getUnreadEmails":
    folder = GetParams("folder")
    res = GetParams("res")
    limit = GetParams("limit")
    filter = GetParams("filter")
    order = GetParams("order")
    
    folder_ = OutlookWellKnowFolderNames.get(folder)

    if not folder:
        folder = "Inbox"
    elif folder_:
        folder = folder_
    
    if order == "" or not order:
        order = "lastModifiedDateTime desc"
    
    if filter and "lastModifiedDateTime" not in filter:
        filter = "lastModifiedDateTime gt 1900-01-01T00:00:00Z and isRead eq false and " + filter
    else:
        filter = "lastModifiedDateTime gt 1900-01-01T00:00:00Z and isRead eq false"
    
    if limit and limit != "":
        limit = int(limit)
    else:
        limit = 25
    
    try:
        list_messages = mod_o365_session[session].mailbox().get_folder(folder_id=folder).get_messages(limit=limit, query=filter, order_by=order)
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
    download_att = GetParams("down")
    res = GetParams("res")
    id_ = GetParams("id_")
    read = GetParams("markasread")
    not_parsed = GetParams("not_parsed")
    whole = GetParams("whole")
    raw = GetParams("raw")
    download_html = GetParams("download_html")
    html_folder = GetParams("html_folder")
    
    import email
    from mailparser import mailparser
    import base64
    
    if not id_:
        raise Exception("Missing Email ID...")
    
    if download_att:
        download_att = eval(download_att)

    if download_html:
        download_html = eval(download_html)
    
    try:
        # It creates a message object and makes available attachments to be downloaded
        message = mod_o365_session[session].mailbox().get_message(id_, download_attachments=True)
        
        files = []
        # API: Used to download attachments of the read email
        for att in message.attachments:
            files.append(att.name)
            if download_att == True:
                if not os.path.isdir(att_folder):
                        raise Exception('The path does not exist.')
                file_path = os.path.normpath(os.path.join(att_folder, att.name))
                base, ext = os.path.splitext(att.name)
                base = base.strip() 
                count = 1
                while os.path.exists(file_path):
                    file_path = os.path.normpath(os.path.join(att_folder, f"{base}_{count}{ext}"))
                    count += 1
                content = att.content
                if isinstance(content, str):
                    try:
                        content = base64.b64decode(content)
                    except Exception as e:
                        PrintException(e)
                        raise
                filename, file_extension = os.path.splitext(att.name)
                if file_extension == '.eml':
                    message.attachments.save_as_eml(att, os.path.join(att_folder, att.name))
                else:
                    with open(file_path, 'wb') as f:
                        f.write(content)
                    #files.append(file_path)
                # att.save(location=file_path)
                # Gets name and extension, if it is an '.eml' (Attached email to the read email) takes a different path because the main way do not work
                #filename, file_extension = os.path.splitext(att.name)
                #if file_extension == '.eml':
                    #message.attachments.save_as_eml(att, os.path.join(att_folder, att.name))

        if download_html == True:

            if not os.path.isdir(html_folder):
                    raise Exception('The path for html does not exist.')
            html_b = BeautifulSoup(message.body, "html.parser")

            # Limpiar el asunto para obtener un nombre de archivo válido
            subjecthtml = message.subject.replace("/", "_").replace("\\", "_").replace(":", "_")
            # Crear un nombre de archivo único usando el asunto
            filenamehtml = f"{subjecthtml}.html"
            filepathhtml = os.path.join(html_folder, filenamehtml)
            #Modifico el body del mensaje para agregar remitente y asunto            
            body_tag = html_b.find("body")
            # Agregar información del remitente
            # Crear la nueva etiqueta
            new_tag = html_b.new_tag("p")
            bold_tag = html_b.new_tag("b")
            bold_tag.string = "Sender:"
            new_tag.append(bold_tag)
            sender_info = f"{message.sender.address}"
            new_tag.append(sender_info)
            # Insertar la nueva etiqueta al inicio del email_body
            body_tag.insert(0, new_tag)
            
            # Agregar el asunto
            # Crear la nueva etiqueta
            new_tag = html_b.new_tag("p")
            bold_tag = html_b.new_tag("b")
            bold_tag.string = "subject:"
            new_tag.append(bold_tag)
            sender_info = f"{message.subject}"
            new_tag.append(sender_info)
            # Insertar la nueva etiqueta al inicio del email_body
            body_tag.insert(1, new_tag)
            with open(filepathhtml, "w", encoding="utf-8") as f:
                f.write(str(html_b))
            
        # Parser: Used to download attachments within an email attached ('.eml') to the read email
        parsed_mail = mailparser.parse_from_bytes(message.get_mime_content())

        for att in parsed_mail.attachments:
            name = re.sub(r'[\\/*?:"<>|]', '',att['filename']) # att['filename']
            name = name.replace("\r","").replace("\n","")
            
            if download_att == True:                    
                if not name in files:
                    files.append(name)
                    cont = base64.b64decode(att['payload'])
                    with open(os.path.join(att_folder, name), 'wb') as file_:
                        file_.write(cont)
                        file_.close()

        # This is for the case of an email with no body
        html_body = BeautifulSoup(message.body, "html.parser")

        links = {}
        if html_body:
            for a in html_body.find_all("a"):
                # First checks the text of the a tag    
                if a.get_text():
                    key = a.get_text()
                # If None, then checks if the a tag has 'title'
                elif a.get("title"):
                    key = a.get("title")
                # If also None, the it gives a generic key
                else:
                    key = 'URL'
                # Finally it checks if the key already exists and adds a '(n°)' at the end
                x = int()
                key_2 = key
                while key in links.keys():
                    x += 1
                    key = key_2 + '(' + str(x) + ')'
                links[key]= a.get("href", '')
            
        if not_parsed and eval(not_parsed) == True:
            body = str(html_body.body)
        elif whole and eval(whole) == True:
            body = str(html_body)
        elif raw and eval(raw) == True:
            body = parsed_mail.body
        else:
            body = html_body.get_text()
            if not body:
                body = message.body

        #     if not not_parsed or not_parsed == False:
        #         body = html_body.get_text()
        #         if not body:
        #             body = message.body
        #     else:

        #         body = str(html_body) 
        # else:
        #     body = message.body
            

        message_all = {
            # Recipient object
            'sender': message.sender.address,
            # Iterate over a Recipients object (List of Recipient objects) and parses each element into string
            'cc': [str(rec) for rec in message.cc._recipients],
            'subject': message.subject,
            # Parses elements datetime.datetime into string
            'sent_time': message.sent.strftime('%d-%m-%Y %H:%M'),
            'received': message.received.strftime('%d-%m-%Y %H:%M'),
            'body': body,
            'links': links,
            'files': files
        }
        
        if read:
            if eval(read):
                message.mark_as_read()
        
        SetVar(res, message_all)
    except Exception as e:
        SetVar(res, False)
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e
    
if module == "downAtt":
    res = GetParams("res")
    att_folder = GetParams("att_folder")
    id_ = GetParams("id_")
    read = GetParams("markasread")
    
    from mailparser import mailparser
    import base64
    
    if not id_:
        raise Exception("Missing Email ID...")
    
    if not os.path.isdir(att_folder):
        raise Exception('The path does not exist.')
    
    try:
        # It creates a message object and makes available attachments to be downloaded
        message = mod_o365_session[session].mailbox().get_message(id_, download_attachments=True)

        att_q = int(message._Message__attachments.__str__().split(': ')[1])

        files = []
        # API: Used to download attachments of the read email
        for att in message.attachments:
            file_path = os.path.normpath(os.path.join(att_folder, att.name))
            base, ext = os.path.splitext(att.name)
            base = base.strip() 
            count = 1
            while os.path.exists(file_path):
                file_path = os.path.normpath(os.path.join(att_folder, f"{base}_{count}{ext}"))
                count += 1
            content = att.content
            if isinstance(content, str):
                try:
                    content = base64.b64decode(content)
                except Exception as e:
                    PrintException(e)
                    raise
            with open(file_path, 'wb') as f:
                f.write(content)
            files.append(file_path)

            # att.save(location=file_path)
            # Gets name and extension, if it is an '.eml' (Attached email to the read email) takes a different path because the main way do not work
            filename, file_extension = os.path.splitext(att.name)
            if file_extension == '.eml':
                message.attachments.save_as_eml(att, os.path.join(att_folder, att.name))
            
        # Parser: Used to download attachments within an email attached ('.eml') to the read email
        parsed_mail = mailparser.parse_from_bytes(message.get_mime_content())
        for att in parsed_mail.attachments:
            name = re.sub(r'[\\/*?:"<>|]', '',att['filename']) # att['filename']
            name = name.replace("\r","").replace("\n","")
     
            if not name in files:
                files.append(name)
                cont = base64.b64decode(att['payload'])
                with open(os.path.join(att_folder, name), 'wb') as file_:
                    file_.write(cont)
                    file_.close()
        
        # This is for the case of an email with no body
        html_body = BeautifulSoup(message.body, "html.parser").body
        
        if read:
            if eval(read):
                message.mark_as_read()
        
        SetVar(res, True)
    except Exception as e:
        SetVar(res, False)
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "markUnread":
    res = GetParams("res")
    id_ = GetParams("id_")
    
    if not id_:
        raise Exception("Missing Email ID...")
    
    try:
        # It creates a message object and makes available attachments to be downloaded
        message = mod_o365_session[session].mailbox().get_message(id_)
   
        unread = message.mark_as_unread()
        
        SetVar(res, unread)
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "downloadEML":
    res = GetParams("res")
    path = GetParams("path")
    name = GetParams("filename")
    id_ = GetParams("id_")
    
    if not id_:
        raise Exception("Missing Email ID...")
    if not path:
        raise Exception("Must provide a saving path...")
    if not name:
        name = "Message"
        
    try:
        # It creates a message object and makes available attachments to be downloaded
        message = mod_o365_session[session].mailbox().get_message(id_)
        path = os.path.join(path,name)
        eml = message.save_as_eml(path)
        
        SetVar(res, eml)
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "moveEmail":
    folderId = GetParams("folderId")
    id_ = GetParams("id_")
    res = GetParams("res")
    
    if folderId == "" or folderId == None:
        folderId = "Inbox"
    
    try:
        message = mod_o365_session[session].mailbox().get_message(id_)
        move = message.move(folderId)
        
        SetVar(res, move)
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "getFolders":
    query = GetParams('filter')
    parent = GetParams('parent')
    folders = GetParams('res')
    
    global get_all_folders
    
    def get_all_folders(data, list_folders, final_list = []):
        
        for d in data['value']:
            if not d in final_list:
                final_list.append(d)
            
        for folder in list_folders:
            
            child_data, list_child =  folder.get_folders()
            if child_data['value'] == []:
                continue
            # If list add each element of the list to the main list instead of adding the whole list as one element
            final_list.extend(child_data['value'])
            get_all_folders(child_data, list_child, final_list)
        
        return final_list
        
    try:   
        if parent:
            if "/" in parent:
                parent = parent.split("/")
            elif "\\" in parent:
                parent = parent.split("\\")
            else:
                parent = [parent]
            try:
                parent_folder = mod_o365_session[session].mailbox()
                parent_folder = [parent_folder]
                for p in parent:
                    parent_data, parent_folder = parent_folder[0].get_folders(query="displayName eq '{p}'".format(p=p))
                    
                if query and query != "":
                    final_data = parent_folder[0].get_folders(query=query)
                    final_list = final_data[0]['value']
                else:
                    data, list_folders = parent_folder[0].get_folders()
                    final_list = get_all_folders(data, list_folders)
            except IndexError:
                final_list = []
        else:
            if query and query != "":
                final_list = mod_o365_session[session].mailbox().get_folders(query=query)
            else:
                data, list_folders = mod_o365_session[session].mailbox().get_folders()
                final_list = get_all_folders(data, list_folders)

        SetVar(folders, final_list)
    
    except Exception as e:
        traceback.print_exc()
        SetVar(folders, False)
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e
    
if module == "newFolder":
    parent = GetParams("parent")
    new_folder = GetParams("new_folder")
    res = GetParams("res")
    
    try:
        try:
            parent = mod_o365_session[session].mailbox().get_folder(folder_id = parent)
        except:
            parent = mod_o365_session[session].mailbox()
        
        parent.create_child_folder(new_folder)
        SetVar(res, True)
    
    except Exception as e:
        SetVar(res, False)
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

"""-----------------------------------------------------------------------------------------------------------------------------------------------------"""

# https://learn.microsoft.com/en-us/graph/api/resources/sharepoint?view=graph-rest-1.0

global mod_o365_endpoints

mod_o365_endpoints = {
    'get_user_groups': '/users/{user_id}/memberOf',
    'get_group_by_id': '/groups/{group_id}',
    'get_group_by_mail': '/groups/?$search="mail:{group_mail}"&$count=true',
    'list_groups': '/groups',
    'list_groups_delta': '/groups/delta',
    'get_group_site': '/groups/{group_id}/sites/{site_name}',
    'get_site_lists': '/groups/{group_id}/sites/{site_name}/lists',
    'get_list': '/groups/{group_id}/sites/{site_name}/lists/{list_id}/columns'
    }

def list_groups(gs):
    """ Returns list of groups orderer alphabetically by name
    
    :rtype: list[{Group Name: name, Group Id: ID}]
    
    """

    url = gs.build_url(mod_o365_endpoints.get('list_groups'))
    response = gs.con.get(url)
    if not response:
        return None
    data = response.json()
    groups = []
    for g in data['value']:
        group = {}  
        group['displayName'] = g['displayName']
        group['id'] = g['id']
        groups.append(group)
        groups.sort(key = lambda g: g['displayName'])

    # Add this endpoint, because in some cases the groups one does not returns everything 
    url = gs.build_url(mod_o365_endpoints.get('list_groups_delta'))
    response = gs.con.get(url)
    if not response:
        return None
    data = response.json()
    for g in data['value']:
        group = {}  
        group['displayName'] = g['displayName']
        group['id'] = g['id']
        if group not in groups:
            groups.append(group)
            groups.sort(key = lambda g: g['displayName'])
    
    return groups

def get_group_by_id(gs, group_id = None):
    """ Returns Microsoft O365/AD group with given id
    :param group_id: group id of group
    :rtype: Group
    """

    if not group_id:
        raise RuntimeError('Provide the group_id')

    if group_id:
        # get channels by the team id
        url = gs.build_url(mod_o365_endpoints.get('get_group_by_id').format(group_id=group_id))

    response = gs.con.get(url)

    if not response:
        return None

    data = response.json()

    return data

def get_group_site(gs, group_id = None, group_site = None):
    """ Returns Microsoft O365/AD group with given id
    :param group_id: group id of group
    :rtype: Group
    """

    if not group_id:
        raise RuntimeError('Provide the group_id')

    if group_id:
        # get channels by the team id
        url = gs.build_url(mod_o365_endpoints.get('get_group_site').format(group_id=group_id, site_name=group_site))

    response = gs.con.get(url)

    if not response:
        return None

    data = response.json()

    return data

def get_site_lists(gs, group_id = None, group_site = None):
    """ Returns Microsoft O365/AD group with given id
    :param group_id: group id of group
    :rtype: Group
    """

    if not group_id:
        raise RuntimeError('Provide the group_id')

    if group_id:
        # get channels by the team id
        url = gs.build_url(mod_o365_endpoints.get('get_site_lists').format(group_id=group_id, site_name=group_site))

    response = gs.con.get(url)

    if not response:
        return None

    data = response.json()

    return data

def get_list_columns(gs, group_id = None, group_site = None, list_id= None):
    """Returns a list with the editable columns that the given list has.

    Args:
        gs (Group Object): _description_
        group_id (str, optional): _description_. Defaults to None.
        group_site (str, optional): _description_. Defaults to None.
        list_id (str, optional): _description_. Defaults to None.

    Raises:
        RuntimeError: _description_
        RuntimeError: _description_

    Returns:
        _type_: _description_
    """

    if not group_id:
        raise RuntimeError('Provide the group_id')

    if not list_id:
        raise RuntimeError('Provide the list_id')
    
    if group_id and list_id:
        # get channels by the team id
        url = gs.build_url(mod_o365_endpoints.get('get_list').format(group_id=group_id, site_name=group_site, list_id=list_id))

    response = gs.con.get(url)

    if not response:
        return None

    data = response.json()
    data_ = []
    # Iteratares over every column present and returns only the ones that are editable.
    for column in data['value']:
        if column['readOnly'] == False:
            data_.append(column)
    
    return data_

def get_libraries(s, site_id = None):
    """Returns a list with all the drives within the passed site. 

    Args:
        s (Sharepoint Object): _description_
        site_id (str, optional): _description_. Defaults to None.

    Returns:
        list: List of drives within the site
    """
    global Storage
    
    store = Storage(parent=s, main_resource='/sites/{id}'.format(id=site_id))
    
    url = store.build_url(store._endpoints.get('list_drives'))

    response = store.con.get(url)

    data = response.json()

    return data

def get_documents(sd, site_id = None, drive_id = None):
    """Returns a list with all the drives within the passed site. 

    Args:
        s (Sharepoint Object): _description_
        site_id (str, optional): _description_. Defaults to None.

    Returns:
        list: List of drives within the site
    """
    global Storage
    
    store = Storage(parent=sd, main_resource='/sites/{id}'.format(id=site_id))
    
    url = store.build_url(store._endpoints.get('list_drives'))

    response = store.con.get(url)

    data = response.json()

    return data

global Pagination_O365
from O365.utils import Pagination as Pagination_O365
from O365.sharepoint import SharepointList

def get_items_no_index(self, limit=None, *, query=None, order_by=None, batch=None, expand_fields=None):
    
    url = self.build_url(self._endpoints.get('get_items'))

    if limit is None or limit > self.protocol.max_top_value:
        batch = self.protocol.max_top_value

    params = {'$top': batch if batch else limit}

    if expand_fields is not None:
        params['expand'] = self.build_field_filter(expand_fields)
        
    if order_by:
        params['$orderby'] = order_by

    if query:
        if isinstance(query, str):
            params['$filter'] = query
        else:
            params.update(query.as_params())

    kwargs = {"headers": {'Prefer':"HonorNonIndexedQueriesWarningMayFailRandomly"}}
    
    response = self.con.get(url, params, **kwargs)

    if not response:
        return []

    data = response.json()
    next_link = data.get('@odata.nextLink', None)

    items = [self.list_item_constructor(parent=self, **{self._cloud_data_key: item})
            for item in data.get('value', [])]

    if batch and next_link:
        return Pagination_O365(parent=self, data=items, constructor=self.list_item_constructor,
                        next_link=next_link, limit=limit)
    else:
        return items

def get_item_by_id_custom(self, item_id, expand_fields=None):
    """ Returns a sharepoint list item based on id
    :param int item_id: item id to search for
    :param expand_fields: specify user-defined fields to return,
    True will return all fields
    :type expand_fields: list or bool         
    :return: Sharepoint Item
    :rtype: SharepointListItem
    """

    url = self.build_url(self._endpoints.get('get_item_by_id').format(item_id=item_id))
    
    params = {}
    
    if expand_fields is not None:
        params['expand'] = self.build_field_filter(expand_fields)
    
    response = self.con.get(url, params=params)

    if not response:
        return []

    data = response.json()
    # Modificted to return the whole data of the item and the item object itself
    return data

SharepointList.get_items_no_index = get_items_no_index
SharepointList.get_item_by_id_custom = get_item_by_id_custom

if module == "listGroups":

    res = GetParams("res")

    try:
        groups_list = list_groups(mod_o365_session[session].groups())

        SetVar(res, groups_list) 

    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "group":

    group_ = GetParams("groupId")
    res = GetParams("res")

    try:

        group = get_group_by_id(mod_o365_session[session].groups(), group_)

        SetVar(res, group)

    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "site":

    group_ = GetParams("groupId")
    res = GetParams("res")

    try:
        
        site = get_group_site(mod_o365_session[session].groups(), 
                              group_, 
                              get_group_by_id(mod_o365_session[session].groups(), group_)['displayName']
                              )

        SetVar(res, site)

    except Exception as e:
        print(traceback.format_exc())
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "siteLists":

    group_ = GetParams("groupId")
    res = GetParams("res")

    try:
          
        sp_lists = get_site_lists(mod_o365_session[session].groups(), 
                              group_, 
                              get_group_by_id(mod_o365_session[session].groups(), group_)['displayName']
                              )

        SetVar(res, sp_lists)

    except Exception as e:
        print(traceback.format_exc())
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "getListColumns":

    group_ = GetParams("groupId")
    list_id = GetParams("listId")
    res = GetParams("res")

    try:
          
        list = get_list(mod_o365_session[session].groups(), 
                              group_, 
                              get_group_by_id(mod_o365_session[session].groups(), group_)['displayName'],
                              list_id
                              )

        SetVar(res, list)

    except Exception as e:
        print(traceback.format_exc())
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "createList":
    site_ = GetParams("siteId") # site_id: a comma separated string of (host_name, site_collection_id, site_id)
    listInfo = GetParams("listInfo")
    res = GetParams("res")

    try:
        
        if isinstance(eval(listInfo), dict): 
            new_list = mod_o365_session[session].sharepoint().get_site(site_).create_list(eval(listInfo))   
        else:
            raise Exception ("Data must be dictionary type...")
        
        SetVar(res, new_list)

    except Exception as e:
        SetVar(res, False)
        print(traceback.format_exc())
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "listItems":
    
    site_ = GetParams("siteId") # site_id: a comma separated string of (host_name, site_collection_id, site_id)
    listName = GetParams("listName")
    limit = GetParams("limit") or 10
    query = GetParams("query") or None
    order_by = GetParams("order_by") or None
    expand_fields = GetParams("expand_fields") or None
    res = GetParams("res")

    try:
        sp_list = mod_o365_session[session].sharepoint().get_site(site_).get_list_by_name(listName).get_items_no_index(limit=int(limit), query=query, order_by=order_by, batch=50)
        
        if expand_fields.startswith("[") and expand_fields.endswith("]"):
            expand_fields = eval(expand_fields)
        else:
            expand_fields = expand_fields.split(",")
        
        items = []
        for item in sp_list:
            data = mod_o365_session[session].sharepoint().get_site(site_).get_list_by_name(listName).get_item_by_id_custom(item.object_id, expand_fields=expand_fields)
            items.append(data)
        
        
        
        SetVar(res, items)

    except Exception as e:
        print(traceback.format_exc())
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "getItem":
    
    site_ = GetParams("siteId") # site_id: a comma separated string of (host_name, site_collection_id, site_id)
    listName = GetParams("listName")
    itemId = GetParams("itemId")
    expand_fields = GetParams("expand_fields") or None
    res = GetParams("res")
    
    try:
        
        data = mod_o365_session[session].sharepoint().get_site(site_).get_list_by_name(listName).get_item_by_id_custom(itemId, expand_fields=expand_fields)

        SetVar(res, data)

    except Exception as e:
        print(traceback.format_exc())
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e
    
if module == "createItem":

    site_ = GetParams("siteId") # site_id: a comma separated string of (host_name, site_collection_id, site_id)
    listName = GetParams("listName")
    itemInfo = GetParams("newData")
    res = GetParams("res")

    try:

        new_item = mod_o365_session[session].sharepoint().get_site(site_).get_list_by_name(listName).create_list_item(eval(itemInfo))

        SetVar(res, True)
        
    except Exception as e:
        SetVar(res, False)
        print(traceback.format_exc())
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "deleteItem":

    site_ = GetParams("siteId") # site_id: a comma separated string of (host_name, site_collection_id, site_id)
    listName = GetParams("listName")
    itemId = GetParams("itemId")
    res = GetParams("res")

    try:
        
        listName = listName.encode()
        
        del_item = mod_o365_session[session].sharepoint().get_site(site_).get_list_by_name(listName).delete_list_item(itemId)

        SetVar(res, del_item)

    except Exception as e:
        SetVar(res, False)
        print(traceback.format_exc())
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "updateItem":

    site_ = GetParams("siteId") # site_id: a comma separated string of (host_name, site_collection_id, site_id)
    listName = GetParams("listName")
    itemId = GetParams("itemId")
    itemInfo = GetParams("newData")
    res = GetParams("res")

    try:       
        data, item_ = mod_o365_session[session].sharepoint().get_site(site_).get_list_by_name(listName).get_item_by_id(itemId)
        item_.update_fields(eval(itemInfo))
        updated_item = item_.save_updates()
        
        SetVar(res, updated_item)

    except Exception as e:
        SetVar(res, False)
        print(traceback.format_exc())
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e
    
if module == "getDocumentLibraries":

    site_ = GetParams("siteId") # site_id: a comma separated string of (host_name, site_collection_id, site_id)
    res = GetParams("res")

    try:
   
        libraries = get_libraries(mod_o365_session[session].sharepoint(), site_)
        
        SetVar(res, libraries)

    except Exception as e:
        SetVar(res, False)
        print(traceback.format_exc())
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e
    
if module == "documentsList":

    site_ = GetParams("siteId") # site_id: a comma separated string of (host_name, site_collection_id, site_id)
    drive_ = GetParams("driveId")
    res = GetParams("res")
    
    def get_drive_contents(drive):
        """Recursively iterates through the content of a drive (at first) and checks if each item if a folder
          or a file. If the case is the it is a Folder, it calls the function again to get its sub-folders 
          and files and so on, until it gets every file within the drive.

        Args:
            drive (Drive Items Generator): Collection of drive items
        """
        global get_drive_contents
        global folders, files
        
        for doc in drive:
            file = {}
            if doc.is_folder:
                folder = doc.get_items()
                folder_ = {'name': doc.name,
                        'object_id': doc.object_id,
                        'parent': doc.get_parent(),
                        'parent_id': doc.get_parent().object_id,
                }
                folders.append(folder_)     
                get_drive_contents(folder)
                
            if doc.is_file:
                file = {'name': doc.name,
                        'object_id': doc.object_id,
                        'parent': doc.get_parent(),
                        'parent_id': doc.get_parent().object_id,
                }
                files.append(file)     
    
    try:
        drive = mod_o365_session[session].sharepoint().get_site(site_).get_document_library(drive_).get_items()
        
        folders = []
        files = []
        
        get_drive_contents(drive)

        contents = {'folders': folders, 'files': files}
        
        SetVar(res, contents)

    except Exception as e:
        SetVar(res, False)
        print(traceback.format_exc())
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e
    
if module == 'upload_item':
    site_ = GetParams("siteId") # site_id: a comma separated string of (host_name, site_collection_id, site_id)
    drive_ = GetParams("driveId")
    folder_id = GetParams("folderId")
    path_ = GetParams("path")
    res = GetParams("res")
    
    try:
        folder_ = mod_o365_session[session].sharepoint().get_site(site_).get_document_library(drive_).get_item(folder_id)
        
        if folder_.is_folder and os.path.exists(path_):
            response = folder_.upload_file(path_)
        
        SetVar(res, response)
        
    except Exception as e:
        SetVar(res, False)
        print(traceback.format_exc())
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e
    
if module == 'modify_item':
    site_ = GetParams("siteId") # site_id: a comma separated string of (host_name, site_collection_id, site_id)
    drive_ = GetParams("driveId")
    item_ = GetParams("itemId")
    update_ = GetParams("update")
    data_ = GetParams("data") # dict: only name and description are allowed at the moment
    move_ = GetParams("move")
    target_folder = GetParams("target_id")
    download_ = GetParams("download")
    path_ = GetParams('path')
    delete_ = GetParams("delete")
    res = GetParams("res")
    
    try:
        
        item = mod_o365_session[session].sharepoint().get_site(site_).get_document_library(drive_).get_item(item_)
        
        if update_ and eval(update_) and isinstance(eval(data_), dict):
            data_ = eval(data_)
            item.update(name=data_.get('name', item.name), description=data_.get('name', item.description))
        
        if move_ and eval(move_):
            target = mod_o365_session[session].sharepoint().get_site(site_).get_document_library(drive_).get_item(target_folder)
            if target.is_folder:
                item.move(target)
        
        if download_ and eval(download_) and os.path.exists(path_):
            item.download(to_path = path_)            
            
        if delete_ and eval(delete_):
            item.delete()
        
        SetVar(res, True)
    except Exception as e:
        SetVar(res, False)
        traceback.print_exc()
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e