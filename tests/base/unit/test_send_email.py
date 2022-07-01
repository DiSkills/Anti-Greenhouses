import base64
import json
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config
from src.base.schemas import File
from src.base.send_email import Email


def test_create_message():
    message = Email._create_message(subject='Hello world!', recipient='user@example.com')
    assert isinstance(message, MIMEMultipart)
    assert message['Subject'] == 'Hello world!'
    assert message['To'] == 'user@example.com'
    assert message['From'] == config.get_email_settings().sender_email


def test_add_only_text_to_payload():
    message = Email._create_message(subject='Hello world!', recipient='user@example.com')

    Email._add_payload(message=message, text='Hello new user!', files=[])
    payload = message.get_payload()
    assert len(payload) == 1

    text = payload[0]
    assert isinstance(text, MIMEText)
    assert text.get_content_subtype() == 'plain'
    assert text.get_payload() == 'Hello new user!'


def test_add_only_html_to_payload():
    message = Email._create_message(subject='Hello world!', recipient='user@example.com')

    Email._add_payload(message=message, text='Hello new user!', files=[], html='<strong>Hello new user!</strong>')
    payload = message.get_payload()
    assert len(payload) == 1

    html = payload[0]
    assert isinstance(html, MIMEText)
    assert html.get_content_subtype() == 'html'
    assert html.get_payload() == '<strong>Hello new user!</strong>'


def test_add_text_and_file_to_payload():
    message = Email._create_message(subject='Hello world!', recipient='user@example.com')

    content = json.dumps({'Hello': 'world!'}).encode()
    file = File(filename='info.json', type='application', subtype='json', content=content)
    Email._add_payload(message=message, text='Hello new user!', files=[file])
    payload = message.get_payload()
    assert len(payload) == 2

    text = payload[0]
    assert isinstance(text, MIMEText)
    assert text.get_content_subtype() == 'plain'
    assert text.get_payload() == 'Hello new user!'

    _json = payload[1]
    assert isinstance(_json, MIMEBase)
    assert _json.get_content_maintype() == 'application'
    assert _json.get_content_subtype() == 'json'
    assert base64.b64decode(_json.get_payload()) == content
    assert _json.get_filename() == 'info.json'
    assert 'content-disposition' in _json


def test_add_html_and_many_files_to_payload():
    message = Email._create_message(subject='Hello world!', recipient='user@example.com')

    content = json.dumps({'Hello': 'world!'}).encode()

    files = [File(filename='info.json', type='application', subtype='json', content=content) for i in range(10)]

    Email._add_payload(message=message, text='Hello new user!', files=files, html='<strong>Hello new user!</strong>')
    payload = message.get_payload()
    assert len(payload) == len(files) + 1

    html = payload[0]
    assert isinstance(html, MIMEText)
    assert html.get_content_subtype() == 'html'
    assert html.get_payload() == '<strong>Hello new user!</strong>'

    for _json in payload[1:]:
        assert isinstance(_json, MIMEBase)
        assert _json.get_content_maintype() == 'application'
        assert _json.get_content_subtype() == 'json'
        assert base64.b64decode(_json.get_payload()) == content
        assert _json.get_filename() == 'info.json'
        assert 'content-disposition' in _json


def test_the_private_method_send(mocker):
    mocker.patch('smtplib.SMTP.sendmail', return_value=None)

    message = Email._create_message(subject='Hello world!', recipient='user@example.com')
    Email._add_payload(message=message, text='Hello new user!', files=[])

    assert Email._send(message=message) is None


def test_send(mocker):
    mocker.patch('smtplib.SMTP.sendmail', return_value=None)
    assert Email.send(subject='Hello world!', recipient='user@example.com', text='Hello new user!') is None
