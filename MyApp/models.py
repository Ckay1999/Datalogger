from mongoengine import Document,EmbeddedDocument,fields

class Admin(Document):
    user_id = fields.StringField(unique=True,required = True, max_length = 250)
    password =fields.StringField(max_length = 250)
    email = fields.EmailField(unique=True)
    phone =fields.IntField()


    def __str__(self):
        return self.user_id

class Operator(Document):
    user_id = fields.StringField(unique=True,required=True, max_length = 250)
    password =fields.StringField( max_length = 250)
    email = fields.EmailField(unique=True)
    phone =fields.IntField()
    department =fields.StringField()
    def __str__(self):
        return self.user_id


class Channel(Document):
    name = fields.StringField(unique=True,required=True, max_length = 250)
    unit = fields.StringField()
    minimum =fields.IntField()
    maximum =fields.IntField()

    def __str__(self):
        return self.name



class User(EmbeddedDocument):
    channel_name=fields.StringField(required=True, max_length = 250)

    def __str__(self):
        return self.channel_name

class UserOperator(Document):
    user_id = fields.StringField(unique=True,required=True, max_length = 250)
    password =fields.StringField( max_length = 250)
    email = fields.EmailField(unique=True)
    phone =fields.IntField()
    department =fields.StringField()
    channel=fields.EmbeddedDocumentField(User)
    def __str__(self):
        return self.user_id
