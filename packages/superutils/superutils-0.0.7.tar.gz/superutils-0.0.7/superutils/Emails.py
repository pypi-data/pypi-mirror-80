#!/usr/bin/env python
# coding: utf-8
# author: Frank YCJ
# email: 1320259466@qq.com


from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import smtplib
import poplib
from email.parser import Parser
from email.header import decode_header

smtp_server_gmail = 'smtp.gmail.com'
smtp_port_gmail = 587

smtp_server_qq = 'smtp.qq.com'
smtp_port_qq = 465

pop3_server_gmail='pop.gmail.com'
pop3_server_qq='pop.qq.com'

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))


def _get_suffix(file_path):
    temp = str(file_path).split(".")
    return temp[len(temp) - 1]


def _get_file_name(file_path):
    str_path = str(file_path).split(".")
    if len(str_path) < 2:
        raise AttributeError("file path error.")
    temp = str_path[len(str_path) - 2]
    i = len(temp) - 1
    while i >= 0:
        if temp[i] == "/":
            break
        elif temp[i] == "\\":
            break
        else:
            i = i - 1
    return temp[i + 1:]


def send_gmail(from_addr, password, to_addr, content, subject, from_nick_name="", to_nick_name=""):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = _format_addr(u'%s <%s>' % (from_nick_name, from_addr))
    msg['To'] = _format_addr(u'%s <%s>' % (to_nick_name, to_addr))
    msg['Subject'] = Header(u'%s', 'utf-8' % subject).encode()
    server = smtplib.SMTP(smtp_server_gmail, smtp_port_gmail)
    server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

def send_gmail_html(from_addr, password, to_addr, html_content, subject, from_nick_name="", to_nick_name=""):
    msg = MIMEText(html_content, 'html', 'utf-8')
    msg['From'] = _format_addr(u'%s <%s>' % (from_nick_name, from_addr))
    msg['To'] = _format_addr(u'%s <%s>' % (to_nick_name, to_addr))
    msg['Subject'] = Header(u'%s', 'utf-8' % subject).encode()
    server = smtplib.SMTP(smtp_server_gmail, smtp_port_gmail)
    server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

def send_gmail_attach(from_addr, password, to_addr, content, subject, file_path_list, from_nick_name="",
                      to_nick_name=""):
    msg = MIMEMultipart()
    msg['From'] = _format_addr(u'%s <%s>' % (from_nick_name, from_addr))
    msg['To'] = _format_addr(u'%s <%s>' % (to_nick_name, to_addr))
    msg['Subject'] = Header(u'%s', 'utf-8' % subject).encode()
    msg.attach(MIMEText(content, 'plain', 'utf-8'))
    if not isinstance(file_path_list, list):
        raise AttributeError("Parameter error, parameter 'file_path_list' is not a list type.")
    tag = 0
    for file_path in file_path_list:
        with open(file_path, 'rb') as f:
            mime = MIMEBase('file', _get_suffix(file_path), filename=_get_file_name(file_path))
            mime.add_header('Content-Disposition', 'attachment', filename=_get_file_name(file_path))
            mime.add_header('Content-ID', '<%s>' % str(tag))
            mime.add_header('X-Attachment-Id', '%s' % str(tag))
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            msg.attach(mime)
        tag = tag + 1
    server = smtplib.SMTP(smtp_server_gmail, smtp_port_gmail)
    server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


def send_gmail_images(from_addr, password, to_addr, content, subject, image_path_list, from_nick_name="",
                      to_nick_name=""):
    msg = MIMEMultipart()
    msg['From'] = _format_addr(u'%s <%s>' % (from_nick_name, from_addr))
    msg['To'] = _format_addr(u'%s <%s>' % (to_nick_name, to_addr))
    msg['Subject'] = Header(u'%s', 'utf-8' % subject).encode()
    msg.attach(MIMEText(content, 'plain', 'utf-8'))
    if not isinstance(image_path_list, list):
        raise AttributeError("Parameter error, parameter 'file_path_list' is not a list type.")
    tag = 0
    for file_path in image_path_list:
        with open(file_path, 'rb') as f:
            mime = MIMEBase('image', _get_suffix(file_path), filename=_get_file_name(file_path))
            mime.add_header('Content-Disposition', 'attachment', filename=_get_file_name(file_path))
            mime.add_header('Content-ID', '<%s>' % str(tag))
            mime.add_header('X-Attachment-Id', '%s' % str(tag))
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            msg.attach(mime)
        msg.attach(MIMEText('<html><body><h1>Hello</h1>' +
                            '<p><img src="cid:%s"></p>' +
                            '</body></html>' % str(tag), 'html', 'utf-8'))
        tag = tag + 1
    server = smtplib.SMTP(smtp_server_gmail, smtp_port_gmail)
    server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()



def send_qq(from_addr, password, to_addr, content, subject, from_nick_name="", to_nick_name=""):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = _format_addr(u'%s <%s>' % (from_nick_name, from_addr))
    msg['To'] = _format_addr(u'%s <%s>' % (to_nick_name, to_addr))
    msg['Subject'] = Header(u'%s', 'utf-8' % subject).encode()
    server = smtplib.SMTP_SSL(smtp_server_qq, smtp_port_qq)
    server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

def send_qq_html(from_addr, password, to_addr, html_content, subject, from_nick_name="", to_nick_name=""):
    msg = MIMEText(html_content, 'html', 'utf-8')
    msg['From'] = _format_addr(u'%s <%s>' % (from_nick_name, from_addr))
    msg['To'] = _format_addr(u'%s <%s>' % (to_nick_name, to_addr))
    msg['Subject'] = Header(u'%s', 'utf-8' % subject).encode()
    server = smtplib.SMTP_SSL(smtp_server_qq, smtp_port_qq)
    server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

def send_qq_attach(from_addr, password, to_addr, content, subject, file_path_list, from_nick_name="",
                      to_nick_name=""):
    msg = MIMEMultipart()
    msg['From'] = _format_addr(u'%s <%s>' % (from_nick_name, from_addr))
    msg['To'] = _format_addr(u'%s <%s>' % (to_nick_name, to_addr))
    msg['Subject'] = Header(u'%s', 'utf-8' % subject).encode()
    msg.attach(MIMEText(content, 'plain', 'utf-8'))
    if not isinstance(file_path_list, list):
        raise AttributeError("Parameter error, parameter 'file_path_list' is not a list type.")
    tag = 0
    for file_path in file_path_list:
        with open(file_path, 'rb') as f:
            mime = MIMEBase('file', _get_suffix(file_path), filename=_get_file_name(file_path))
            mime.add_header('Content-Disposition', 'attachment', filename=_get_file_name(file_path))
            mime.add_header('Content-ID', '<%s>' % str(tag))
            mime.add_header('X-Attachment-Id', '%s' % str(tag))
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            msg.attach(mime)
        tag = tag + 1
    server = smtplib.SMTP_SSL(smtp_server_qq, smtp_port_qq)
    server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


def send_qq_images(from_addr, password, to_addr, content, subject, image_path_list, from_nick_name="",
                      to_nick_name=""):
    msg = MIMEMultipart()
    msg['From'] = _format_addr(u'%s <%s>' % (from_nick_name, from_addr))
    msg['To'] = _format_addr(u'%s <%s>' % (to_nick_name, to_addr))
    msg['Subject'] = Header(u'%s', 'utf-8' % subject).encode()
    msg.attach(MIMEText(content, 'plain', 'utf-8'))
    if not isinstance(image_path_list, list):
        raise AttributeError("Parameter error, parameter 'file_path_list' is not a list type.")
    tag = 0
    for file_path in image_path_list:
        with open(file_path, 'rb') as f:
            mime = MIMEBase('image', _get_suffix(file_path), filename=_get_file_name(file_path))
            mime.add_header('Content-Disposition', 'attachment', filename=_get_file_name(file_path))
            mime.add_header('Content-ID', '<%s>' % str(tag))
            mime.add_header('X-Attachment-Id', '%s' % str(tag))
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            msg.attach(mime)
        msg.attach(MIMEText('<html><body><h1>Hello</h1>' +
                            '<p><img src="cid:%s"></p>' +
                            '</body></html>' % str(tag), 'html', 'utf-8'))
        tag = tag + 1
    server = smtplib.SMTP_SSL(smtp_server_qq, smtp_port_qq)
    server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()




# ==============================================================================

def _guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

def _decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def _get_email_info(msg, func,indent=0):
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = _decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = _decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            func('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            func('%spart %s' % ('  ' * indent, n))
            func('%s--------------------' % ('  ' * indent))
            _get_email_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = _guess_charset(msg)
            if charset:
                content = content.decode(charset)
            func('%sText: %s' % ('  ' * indent, content + '...'))
        else:
            func('%sAttachment: %s' % ('  ' * indent, content_type))



def receive_email_gmail(account,password,recive_data_func):
    if not callable(recive_data_func):
        raise AttributeError("The parameter is incorrect and a function that accepts data is required.")
    server = poplib.POP3_SSL(pop3_server_gmail)
    # server.set_debuglevel(1)
    recive_data_func(server.getwelcome())
    # 认证:
    server.user(account)
    server.pass_(password)
    recive_data_func('Messages: %s. Size: %s' % server.stat())
    resp, mails, octets = server.list()
    # 获取最新一封邮件, 注意索引号从1开始:
    resp, lines, octets = server.retr(len(mails))
    # 解析邮件:
    msg = Parser().parsestr('\r\n'.join(lines))
    # 打印邮件内容:
    _get_email_info(msg,recive_data_func)
    # 慎重:将直接从服务器删除邮件:
    # server.dele(len(mails))
    # 关闭连接:
    server.quit()



def receive_email_qq(account,password,recive_data_func):
    if not callable(recive_data_func):
        raise AttributeError("The parameter is incorrect and a function that accepts data is required.")
    server = poplib.POP3_SSL(pop3_server_qq)
    # server.set_debuglevel(1)
    recive_data_func(server.getwelcome())
    # 认证:
    server.user(account)
    server.pass_(password)
    recive_data_func('Messages: %s. Size: %s' % server.stat())
    resp, mails, octets = server.list()
    # 获取最新一封邮件, 注意索引号从1开始:
    resp, lines, octets = server.retr(len(mails))
    # 解析邮件:
    msg = Parser().parsestr('\r\n'.join(lines))
    # 打印邮件内容:
    _get_email_info(msg,recive_data_func)
    # 慎重:将直接从服务器删除邮件:
    # server.dele(len(mails))
    # 关闭连接:
    server.quit()
