import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE, formatdate
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header
from email import encoders
from datetime import datetime

#20202/12/28 Add Log

class MailTools():
            
    def __init__(self):
        self.smtp_server='mail.lextar.com'
        self.password='Lex,1234'
        self.from_addr='lexbi2@lextar.com'
        self.to_addr='chin.yang@lextar.com'

    def WiteLog(self,Msg):
        """Write Log""" 
        fileName="Err_"+datetime.now().strftime('%Y%m%d')+".err"
        with open(fileName,'a',encoding='utf-8') as fi:
            Msg=datetime.now().strftime('%Y%m%d %H:%M:%S')+","+Msg+"\n"
            fi.write(Msg)  
            fi.close()    
    
    def __format_addr(self,s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))


    def MailTest(self,to_addr):
        """MailTest to_addr"""
        try:

            msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
            msg['From'] ='LEXTAR-BI'
            msg['To'] = to_addr
            msg['Subject'] = Header('Lextar Mis Report').encode()
            server = smtplib.SMTP(self.smtp_server, 25)
            server.sendmail(self.from_addr, self.to_addr, msg.as_string())
            server.quit()        
        
        except Exception as err:
            print("MailTest", str(err))
            msg="MailTest Err"+err
            self.WiteLog(msg)  
        
    def SendHtml(self,Subject,to_addr,htmlMsg):
        """Subject,to_addr,htmlMsg"""

        try:
            msg = MIMEText(htmlMsg, 'html', 'utf-8')
            msg['From'] =self.from_addr
            msg['To'] = to_addr
            msg['Subject'] = Header(Subject).encode()
            server = smtplib.SMTP(self.smtp_server, 25)
            server.send_message(msg)
            server.quit()        
            print('Mail Send')
        
        except Exception as err:
            print("SendHtml", str(err))
            msg="SendHtml Err"+err
            self.WiteLog(msg)  
        
    def SendAttachFile(self,Subject,Msg,FileName,to_addr,cc_Addr="",html=False):
        
        """ 寄送附件Subject,Msg,FileName,to_addr,cc_Addr,html=False """
        try:


            msg = MIMEMultipart()
            msg['From'] = self.from_addr
            msg['To'] = to_addr
            msg['Subject'] = Subject
            if bool(cc_Addr): msg['CC'] = cc_Addr
        
            # 邮件正文是MIMEText:
            if (html):
                msg.attach(MIMEText(Msg, 'html', 'utf-8'))
            else :
                msg.attach(MIMEText(Msg, 'plain', 'utf-8'))           
                    
            with open(FileName, 'rb') as f:
                # 设置附件的MIME和文件名，这里是png类型:
                mime = MIMEBase('text', 'xlsx', filename=FileName)
        
                # 加上必要的头信息:
                mime.add_header('Content-Disposition', 'attachment', filename=FileName)
                mime.add_header('Content-ID', '<0>')
                mime.add_header('X-Attachment-Id', '0')
        
                # 把附件的内容读进来:
                mime.set_payload(f.read())
                # 用Base64编码:
                encoders.encode_base64(mime)
                # 添加到MIMEMultipart:
                msg.attach(mime)

            server = smtplib.SMTP(self.smtp_server, 25)       
            server.send_message(msg)       
            server.quit()
        
            if not bool(cc_Addr):
                print('Email sent!')
            else :
                print('cc Email sent!')
        
        except Exception as err:
            print("SendAttachFile", str(err))
            msg="SendAttachFile Err"+err
            self.WiteLog(msg)     
        
        
        


        
