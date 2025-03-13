from flask import Flask, render_template, redirect, url_for, flash
from flask_ckeditor import CKEditor, CKEditorField
from flask_wtf import FlaskForm
import bleach
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_bootstrap import Bootstrap5
import smtplib
import os
from datetime import datetime



app_password = os.getenv('APP_PASSWORD')
app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY')
Bootstrap5(app)
ckeditor = CKEditor(app)
email_address = os.getenv('EMAIL')


app.config['CKEDITOR_PKG_TYPE'] = 'standard'
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_CONFIG'] = {'versioncheck' : False}

now_year = datetime.now().year

def clean_input(input_data):
    return bleach.clean(input_data, tags=[], strip=True)


class SendMessageForm(FlaskForm):
    name = StringField('Your Name: ', validators=[DataRequired()])
    email = StringField(label = 'Your Email Address: ', validators = [DataRequired(), Email()])
    message = CKEditorField(label= 'Your Message: ', validators=[DataRequired()])
    submit = SubmitField(label = 'Send Message')

@app.route('/', methods = ['GET', 'POST'])
def homepage():
    contact_form = SendMessageForm()
    if contact_form.validate_on_submit():
            with smtplib.SMTP('smtp.gmail.com', 587) as connection:
                connection.starttls()

                sender = clean_input(contact_form.name.data)
                email = clean_input(contact_form.email.data)
                message = clean_input(contact_form.message.data)

                connection.login(user = 'amirrezab334@gmail.com',
                                 password = app_password)
                connection.sendmail(to_addrs = email_address,
                                    from_addr = email_address,
                                    msg = f'Subject: You Have a New Message!\n\n'
                                          f'From: {sender}\n'
                                          f'Email Address: {email}\n'
                                          f'Message: {message}')
                flash('Message Sent. I Will Contact You ASAP.')
                return redirect((url_for('homepage', _anchor='page-top')))
    return render_template('index.html', form = contact_form, year = now_year)




if __name__ == '__main__':
    app.run(debug = True)