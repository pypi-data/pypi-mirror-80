import amino
from typing import BinaryIO

class Raid:
    def __init__(self, email: str, password: str):
        self.cl = amino.Client()
        self.cl.login(email=email, password=password)
        print('\nLogged in!')    

    def communities(self, start: int = 0, size: int = 25):
        com = self.cl.sub_clients(start=start, size=size)

        for name,id in zip(com.name,com.comId):
            print(name,id)

    def chats(self, comId: str, start: int = 0, size: int = 25):
        """
        List of Chats the account is in.

        **Parameters**
            - *comId* : ID of the Community
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **200** (:meth:`Chat List <amino.lib.util.objects.threadList>`) : **Success**

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """   
        sub_client = amino.SubClient(comId=comId, profile=self.cl.profile)
        chat = sub_client.get_chat_threads(start=start, size=size)
        for name,id in zip(chat.title,chat.chatId):
            print(name,id)

    def standart(self, comId: str, chatId: str, message: str = None, file: BinaryIO = None, fileType: str = None,  stickerId: str = None):
        """
        Standard raid in Chat.

        **Parameters**
            - **message** : Message to be sent
            - **comId** : ID of the Community
            - **chatId** : ID of the Chat.
            - **file** : File to be sent.
            - **fileType** : Type of the file.
                - ``audio``, ``image``, ``gif``
            - **stickerId** : Sticker ID to be sent.

        **Returns**
            - **200** (int) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **106** (:meth:`AccessDenied <amino.lib.util.exceptions.AccessDenied>`) : Access denied.

            - **1605** (:meth:`ChatFull <amino.lib.util.exceptions.ChatFull>`) : ``Unknown Message``

            - **1663** (:meth:`ChatViewOnly <amino.lib.util.exceptions.ChatViewOnly>`) : ``Unknown Message``

            - **Other** (:meth:`SpecifyType <amino.lib.util.exceptions.SpecifyType>`, :meth:`JSON Object <JSONObject>`)
        """
        sub_client = amino.SubClient(comId=comId, profile=self.cl.profile)
        while True:
            if file:
                with open(file, 'rb') as d:
                    sub_client.send_message(message=message, chatId=chatId, fileType=fileType, file=d)
                    d.close()
            else:        
                sub_client.send_message(message=message, chatId=chatId, stickerId=stickerId)  

    def with_messageType(self, comId: str, chatId: str, message: str = None, messageType: int = 100):
        """
        Standard raid in Chat.

        **Parameters**
            - **message** : Message to be sent
            - **comId** : ID of the Community
            - **chatId** : ID of the Chat.
            - **messageType** : Type of the message.

        **Returns**
            - **200** (int) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **106** (:meth:`AccessDenied <amino.lib.util.exceptions.AccessDenied>`) : Access denied.

            - **1605** (:meth:`ChatFull <amino.lib.util.exceptions.ChatFull>`) : ``Unknown Message``

            - **1663** (:meth:`ChatViewOnly <amino.lib.util.exceptions.ChatViewOnly>`) : ``Unknown Message``

            - **Other** (:meth:`SpecifyType <amino.lib.util.exceptions.SpecifyType>`, :meth:`JSON Object <JSONObject>`)
        """

        sub_client = amino.SubClient(comId=comId, profile=self.cl.profile)
        while True:
            sub_client.send_message(message=message, chatId=chatId, messageType=messageType)

    def with_nickname(self, comId: str, chatId: str):
        """
        Join and leave an Chat.

        **Parameters**
            - **comId** : ID of the Community
            - **chatId** : ID of the Chat.

        **Returns**
            - **200** (int) : **Success**

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """

        sub_client = amino.SubClient(comId=comId, profile=self.cl.profile)
        while True:
            sub_client.join_chat(chatId=chatId)
            sub_client.leave_chat(chatId=chatId)

    def send_online_users(self, comId: str, message: str):
        sub_client = amino.SubClient(comId=comId, profile=self.cl.profile)
        
        st = 0
        users = []
        for x in range(100):
            profile = sub_client.get_online_users(start=st, size=100).profile
            if len(profile.userId) == 0:
                break
            users += profile.userId
            st += 100
        for user in users:
            sub_client.start_chat(userId=user, message=message)
        
    def post_blog(self, comId: str, title: str, content: str, categoriesList: list = None, backgroundColor: str = None, fansOnly: bool = False):
        sub_client = amino.SubClient(comId=comId, profile=self.cl.profile)
        
        while True:
            sub_client.post_blog(title=title, content=content, categoriesList=categoriesList,backgroundColor=backgroundColor, fansOnly=fansOnly)
 
    def post_wiki(self, comId: str, title: str, content: str, icon: str = None, keywords: str = None, backgroundColor: str = None, images: list = None, fansOnly: bool = False):
        sub_client = amino.SubClient(comId=comId, profile=self.cl.profile)
 
        while True:
            sub_client.post_wiki(title=title, content=content, icon=icon, keywords=keywords,backgroundColor=backgroundColor, images=images, fansOnly=fansOnly)
    
    def comment(self, comId: str, message: str, userId: str = None, blogId: str = None, wikiId: str = None, replyTo: str = None, isGuest: bool = False):
        sub_client = amino.SubClient(comId=comId, profile=self.cl.profile)
        
        while True:
            sub_client.comment(message=message, userId=userId, blogId=blogId, wikiId=wikiId, replyTo=replyTo, isGuest=isGuest)