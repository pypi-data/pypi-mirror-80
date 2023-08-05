# -*- coding:utf8 -*-
# @author：X.
# @time：2020/9/16:11:16
import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from sktest.common.log import logger


def send_email(user, pwd, toaddrs, content=None):
    # 发送邮箱服务器
    smtpserver = 'smtp.qq.com'
    # 发送用户和密码

    if user and pwd:
        if not content:
            content = f"""
            测试环境：{os.name}
            执行时间：{datetime.strftime(datetime.now(), '%Y.%m.%d-%H:%M:%S')}
            测试执行人：{os.getlogin()}
            自动化测试完成，详情请查阅附件。。。
        """
        text = MIMEText(content)
        excel_file1 = 'report/report.xlsx'
        excel_file2 = 'testcase/testcase.xlsx'
        att1 = MIMEApplication(open(excel_file1, 'rb').read())
        att1.add_header('Content-Disposition', 'attachment', filename='测试报告.xlsx')
        att2 = MIMEApplication(open(excel_file2, 'rb').read())
        att2.add_header('Content-Disposition', 'attachment', filename='测试用例.xlsx')

        m = MIMEMultipart()
        m.attach(text)
        m.attach(att1)
        m.attach(att2)
        m['Subject'] = '自动化测试报告'

        try:
            server = smtplib.SMTP('smtp.qq.com')
            server.login(user, pwd)
            server.sendmail(user, toaddrs, m.as_string())
            logger.info('**** Email sent successfully ****')
            server.quit()
        except:
            logger.exception('**** Email sent failure ****')
    else:
        logger.info('**** 没有配置任何邮件信息，不会为您发送邮件！ ****')


if __name__ == '__main__':
    c = """
        测试项目：xxx
        测试环境：xxx
        执行时间：xxx
        测试执行人：xxx
        自动化测试完成，详情请查阅附件。。。
    """
    # send_email('18573208753@163.com')
    # email_config = {}
    # send_email('receiver', 'email_content', email_config=email_config)
