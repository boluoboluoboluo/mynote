#!/usr/bin/python
# -*- coding:utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

#第三方SMTP服务
mail_host = "smtp.163.com"
mail_user = "xxx"
mail_pass = "xxx"	#授权码

sender = "xxx@163.com"
receivers = ['xxx@qq.com']

message = MIMEText('今天星期3..','plain','utf-8')
message['From'] = sender
message['To'] = receivers[0]

subject = 'hello..'
message['Subject'] = Header(subject,'utf-8')

try:
	# smtpObj = smtplib.SMTP()
	# smtpObj.connect(mail_host,25)
	smtpObj = smtplib.SMTP_SSL(mail_host)
	smtpObj.login(mail_user,mail_pass)
	smtpObj.sendmail(sender,receivers,message.as_string())
	print("邮件发送成功")
except smtplib.SMTPException as e:
	print("Error:无法发送邮件",e)

