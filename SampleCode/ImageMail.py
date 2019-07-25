# Create the root message and fill in the from, to, and subject headers
msgRoot = MIMEMultipart('related')
msgRoot['Subject'] = Subject
msgRoot['From'] = from_addr
msgRoot['To'] = to_addr
msgRoot.preamble = 'This is a multi-part message in MIME format.'

# Encapsulate the plain and HTML versions of the message body in an
# 'alternative' part, so message agents can decide which they want to display.
msgAlternative = MIMEMultipart('alternative')
msgRoot.attach(msgAlternative)

msgText = MIMEText('This is the alternative plain text message.')
msgAlternative.attach(msgText)

# We reference the image in the IMG SRC attribute by the ID we give it below
msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
msgAlternative.attach(msgText)

# This example assumes the image is in the current directory
fp = open('test.jpg', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()


# This example assumes the image is in the current directory
FileName='BinCode下線率_Summary20190715.xlsx'
fp = open(FileName, 'rb')
# 设置附件的MIME和文件名，这里是png类型:
mime = MIMEBase('text', 'xlsx', filename=FileName)
        
# 加上必要的头信息:
mime.add_header('Content-Disposition', 'attachment', filename=FileName)
        
# 把附件的内容读进来:
mime.set_payload(fp.read())
# 用Base64编码:
encoders.encode_base64(mime)
fp.close()

# Define the image's ID as referenced above
msgImage.add_header('Content-ID', '<image1>')
msgRoot.attach(msgImage)
msgRoot.attach(mime)


server = smtplib.SMTP(smtp_server, 25)       
server.send_message(msgRoot)       
server.quit() 
