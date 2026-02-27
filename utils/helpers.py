import string


def escape_html(text):
    html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
    }
    return "".join(html_escape_table.get(c, c) for c in text)


def create_fake_message(chat_id, from_user, message_id=None):

    class FakeChat:
        def __init__(self, id):
            self.id = id

    class FakeMessage:
        def __init__(self, chat_id, from_user, message_id=None):
            self.chat = FakeChat(chat_id)
            self.from_user = from_user
            self.id = message_id or 0

    return FakeMessage(chat_id, from_user, message_id)