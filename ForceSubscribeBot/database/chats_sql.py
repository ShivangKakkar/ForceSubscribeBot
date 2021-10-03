from sqlalchemy import Column, BigInteger, String, Boolean
from . import BASE, SESSION


class Chats(BASE):
    __tablename__ = "chats"
    __table_args__ = {'extend_existing': True}
    channel_id = Column(BigInteger, primary_key=True)
    force_chat = Column(BigInteger)
    action = Column(String)
    ignore_service = Column(Boolean)
    only_owner = Column(Boolean)

    def __init__(self, channel_id, force_chat, action='mute', ignore_service=True, only_owner=True):
        self.channel_id = channel_id
        self.force_chat = force_chat
        self.action = action
        self.ignore_service = ignore_service
        self.only_owner = only_owner


Chats.__table__.create(checkfirst=True)


async def num_chats():
    try:
        return SESSION.query(Chats).count()
    finally:
        SESSION.close()


async def get_force_chat(chat_id):
    q = SESSION.query(Chats).get(chat_id)
    if q and q.force_chat:
        chat = q.force_chat
        SESSION.close()
        return chat
    else:
        return None


async def change_force_chat(chat_id, force_chat):
    q = SESSION.query(Chats).get(chat_id)
    if q:
        q.force_chat = force_chat
    else:
        SESSION.add(Chats(chat_id, force_chat))
    SESSION.commit()


async def get_action(chat_id):
    q = SESSION.query(Chats).get(chat_id)
    if q and q.action:
        action = q.action
        SESSION.close()
        return action
    else:
        return None


async def change_action(chat_id, action):
    q = SESSION.query(Chats).get(chat_id)
    if q:
        q.action = action
    else:
        SESSION.add(Chats(chat_id, action))
    SESSION.commit()


async def get_ignore_service(chat_id):
    q = SESSION.query(Chats).get(chat_id)
    if q and q.ignore_service:
        ignore_service = q.ignore_service
        SESSION.close()
        return ignore_service
    else:
        return False


async def toggle_ignore_service(chat_id, value):
    q = SESSION.query(Chats).get(chat_id)
    if q:
        if value:
            q.ignore_service = True
        else:
            q.ignore_service = False
        SESSION.commit()
        return True
    else:
        return False


async def get_only_owner(chat_id):
    q = SESSION.query(Chats).get(chat_id)
    if q and q.only_owner:
        only_owner = q.only_owner
        SESSION.close()
        return only_owner
    else:
        return False


async def toggle_only_owner(chat_id, value):
    q = SESSION.query(Chats).get(chat_id)
    if q:
        if value:
            q.only_owner = True
        else:
            q.only_owner = False
        SESSION.commit()
        return True
    else:
        return False


async def chat_exists(chat_id):
    q = SESSION.query(Chats).get(chat_id)
    if q:
        return True
    else:
        return False
