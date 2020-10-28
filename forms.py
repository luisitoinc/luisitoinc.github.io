from wtforms import Form
from wtforms import StringField, TextField
from wtforms.fields.html5 import EmailField


class LoginForm(Form):

    Region = StringField("Region")
    email = EmailField("Correo electronico")
    comment = TextField("Comentario")
