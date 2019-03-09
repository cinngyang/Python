import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE, formatdate
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header
from email import encoders

class CSS_Foramt():
    
    def GetTable(self):
        styStr="<head>"
        styStr+="<style type=""text/css""> "
        styStr+=" table { border: 0; font-family: arial; font-size:12px;} "
        styStr+=" th { background-color:yellow;} "
        styStr+=" td { border-bottom:1 solid #000000;} "
        styStr+=" .fail { color:#FF0000;} "
        styStr+="</head>"
        return styStr

class MyMail():  
    
    def __init__(self):
        self.user='cinng.yang@gmail.com'
        self.pwd='XXXXXX'
        self.server='smtp.gmail.com'
        self.port=465
    
        
    def SendHtml(self,Subject,Bodys):      
       
        htmlMsg='<html> <head> '
        htmlMsg+='<style> body {background-color: powderblue;} '
        htmlMsg+='h1  {color: blue;}'
        htmlMsg+='table { '
        htmlMsg+='font-family: arial, sans-serif; '
        htmlMsg+='border-collapse: collapse; '
        htmlMsg+='width: 100%; } '
        htmlMsg+='td, th { '
        htmlMsg+='border: 1px solid #dddddd; '
        htmlMsg+='text-align: left;'
        htmlMsg+='padding: 8px; }'
        htmlMsg+='tr:nth-child(even) {  background-color: #88dddd; } '
        htmlMsg+='</style> '
        htmlMsg+='</head>'      
       
        
        msg = MIMEText(htmlMsg+'<body><h1>Hello</h1>' +Bodys+
                       '<p>send by <a href="http://www.python.org">Python</a>...</p>' +
                       '</body></html>', 'html', 'utf-8')
        msg['Subject'] = Subject
        msg['From'] = self.user
        msg['To'] = 'cinng.yang@gmail.com'
        server = smtplib.SMTP_SSL(self.server, self.port) 
        server.login(self.user,self.pwd)
        server.send_message(msg)
        server.quit()
        print('Email sent!')
        
    def SendHtml2(self):    
        htmlMsg='<html> <head> '
        htmlMsg+='<style> body {background-color: powderblue;} '
        htmlMsg+='h1  {color: blue;}'
        htmlMsg+='table { '
        htmlMsg+='font-family: arial, sans-serif; '
        htmlMsg+='border-collapse: collapse; '
        htmlMsg+='width: 100%; } '
        htmlMsg+='td, th { '
        htmlMsg+='border: 1px solid #88ddddd; '
        htmlMsg+='text-align: left;'
        htmlMsg+='padding: 8px; }'
        htmlMsg+='tr:nth-child(even) {  background-color: #dddddd; } '
        htmlMsg+='</style> '
        htmlMsg+='</head>'
        htmlMsg+=' <body> '
        htmlMsg+='<table> <tr> <th>Company</th> <th>Contact</th> <th>Country</th> </tr> '
        htmlMsg+='<tr> <td>Alfreds Futterkiste</td>  <td>Maria Anders</td>  <td>Germany</td> </tr> '
        htmlMsg+='</table> </body>'
        htmlMsg+=' </html>'
        
        msg = MIMEText(htmlMsg, 'html', 'utf-8')
        msg['Subject'] = 'html format'
        msg['From'] = self.user
        msg['To'] = 'cinng.yang@gmail.com'
        server = smtplib.SMTP_SSL(self.server, self.port) 
        server.login(self.user,self.pwd)
        server.send_message(msg)
        server.quit()
        print('Email sent!')
        
    def SendAttachFile(self,Subject,file):
        #Attach File
        msg = MIMEMultipart()
        msg['From'] = self.user
        msg['To'] = self.user
        msg['Subject'] = Subject
        # 邮件正文是MIMEText:
       
        msg.attach(MIMEText('send with file...', 'plain', 'utf-8'))
       
        with open(file, 'rb') as f:
            # 设置附件的MIME和文件名，这里是png类型:
            mime = MIMEBase('text', 'html', filename=file)
            # 加上必要的头信息:
            mime.add_header('Content-Disposition', 'attachment', filename=file)
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            # 把附件的内容读进来:
            mime.set_payload(f.read())
            # 用Base64编码:
            encoders.encode_base64(mime)
            # 添加到MIMEMultipart:
            msg.attach(mime)
        server = smtplib.SMTP_SSL(self.server, self.port) 
        server.login(self.user,self.pwd)
        server.send_message(msg)
        server.quit()
        print('Email sent!')
    
