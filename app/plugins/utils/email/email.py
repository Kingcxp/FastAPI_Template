import os
import datetime
import aiosmtplib

from typing import Optional, Dict
from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from ....manager import console


async def send_mail(target: str, sender_name: str, title: str, msg: str, files: Optional[Dict[str, bytes]] = None) -> bool:
    """异步发送邮件，可带附件

    Args:
        target (str): 目标邮箱地址
        sender_name (str): 发送者名称
        title (str): 邮件标题
        msg (str): 邮件正文
        files (Optional[Dict[str, bytes]]): 附件列表 Key: 文件名 Value: 文件二进制内容

    Returns:
        bool: 发送邮件是否成功，成功为 True，否则为 False
    """
    message = MIMEMultipart()
    time = datetime.datetime.today().strftime("%m-%d %H: %M")
    email = os.getenv("EMAIL")
    email_passkey = os.getenv("EMAIL_PASSKEY")
    email_host = os.getenv("EMAIL_HOST")
    if email is None or \
       email_passkey is None or \
       email_host is None:
        console.log("[red][on #F8BBD0]未配置邮箱信息，请检查环境(EMAIL, EMAIL_PASSKEY, EMAIL_HOST)变量是否设置！[/on #F8BBD0][/red]")
        return False

    message["From"] = formataddr(pair=(sender_name, email))
    message["To"] = target
    message["Subject"] = title + " -- {}".format(time)

    message.attach(MIMEText(msg, "plain", "utf-8"))

    if files is not None:
        for filename, filecontent in files.items():
            attachment = MIMEApplication(filecontent)
            attachment.add_header("Content-Disposition", "attachment", filename=filename)
            message.attach(attachment)

    try:
        async with aiosmtplib.SMTP(hostname=email_host) as server:
            await server.login(email, email_passkey)
            await server.sendmail(email, target, message.as_string())
        return True
    except Exception:
        console.print_exception(show_locals=True)
        return False
