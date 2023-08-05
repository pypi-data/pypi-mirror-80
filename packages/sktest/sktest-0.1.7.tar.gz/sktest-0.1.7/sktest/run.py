# -*-coding:utf8-*-
# @auth 小哥哥
# @time 2020/8/24 10:00

import os
from datetime import datetime
from sktest.sktest.autotest import AutoTest
from sktest.common.emailtool import send_email


class Config:
    def __init__(self, excel_file_path='', case_sheet_name='', browser_name='',
                 executable_path='', case_object_name='', email_account='', email_password='',
                 email_receiver=None):
        if excel_file_path:
            self.excel_file_path = excel_file_path
        else:
            self.excel_file_path = 'testcase/testcase.xlsx'
        if case_sheet_name:
            self.case_sheet_name = case_sheet_name
        else:
            self.case_sheet_name = 'case'
        if browser_name:
            self.browser_name = browser_name
        else:
            self.browser_name = 'Chrome'
        if executable_path:
            self.executable_path = executable_path
        else:
            self.executable_path = executable_path
        if case_object_name:
            self.case_object_name = case_object_name
        else:
            self.case_object_name = 'UI Automation testing'

        self.email_account = email_account

        self.email_password = email_password

        self.email_receiver = email_receiver



class Run(Config):
    def __init__(self):
        super(Run, self).__init__()

        # self.__browser_config = {"browserName": self.browser_name, "executable_path": self.executable_path}
        # self.__email_config = {'user': self.email_account, "password": self.email_password}
        # self.__receiver = self.email_receiver
        # self.__case_object_name = self.case_object_name

    def run(self):
        auto = AutoTest(self.excel_file_path, self.case_sheet_name, {"browserName": self.browser_name, "executable_path": self.executable_path})
        run_time = datetime.strftime(datetime.now(), "%Y/%m/%d %H:%M:%S")
        auto.run()

        email_content = f"""
                测试项目：{self.case_object_name}
                测试环境：{os.name}
                执行时间：{run_time}
                测试执行人：{os.getlogin()}
                自动化测试完成，详情请查阅附件。。。
            """
        send_email(self.email_account,self.email_password,self.email_receiver, email_content)


# TODO 后续扩展：
#                1.错误截图 --  done 出错截取整个屏幕
#               2.日志可以考虑分类保存  -- done 按天分割
#              3.生成测试报告  -- done
#             4.邮件发送 -- done
#            5.集成到Jenkins -- 待完成
#           6.整体框架容错性检测  -- 待完成

# TODO v2.0
#         1.增加时间监测
#         2.兼容app测试
