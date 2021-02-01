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
sys.path.append(cur_path)
from O365 import Account
import os

module = GetParams("module")
global credentials
global account

if module == "connect":
    client_id = GetParams("client_id")
    client_secret = GetParams("client_secret")
    try:
        credentials = (client_id, client_secret)
        account = Account(credentials)
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

if module == "getAllEmails":
    res = GetParams("res")
    filtro = GetParams("filtro")
    try:
        list_messages = account.mailbox().get_messages()
        list_object_id = []
        for message in list_messages:
            if filtro:
                if message.subject.find(filtro) != -1:
                    list_object_id.append(message.object_id)
            if not filtro:
                list_object_id.append(message.object_id)
        SetVar(res,list_object_id)
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "getAllEmails":
    res = GetParams("res")
    filtro = GetParams("filtro")
    try:
        list_messages = account.mailbox().get_messages()
        list_object_id = []
        for message in list_messages:
            if filtro:
                if message.subject.find(filtro) != -1:
                    list_object_id.append(message.object_id)
            if not filtro:
                list_object_id.append(message.object_id)
        SetVar(res,list_object_id)
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e

if module == "readEmail":
    import json
    att_folder = GetParams("att_folder")
    res = GetParams("res")
    id_= GetParams("id_")
    try:
        message = account.mailbox().get_message(id_,download_attachments = True)
        for att in message.attachments:
            att.save(att_folder)
        message_all = {
            'body': message.body,
            'cc': message.cc,
            'sender': message.sender.address,
            'sent_time': message.sent,
            'received': message.received
        }
        SetVar(res, message_all)
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
        PrintException()
        raise e
