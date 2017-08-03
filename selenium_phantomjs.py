# coding=utf-8
from selenium import webdriver

# 创建浏览器
driver = webdriver.PhantomJS()
# 访问百度
driver.get("https://www.baidu.com/")
# 打印访问的页面
# print driver.page_source

# 点击登录按钮
driver.find_element_by_class_name("lb").click()
driver.save_screenshot("baidu.jpg")
# 在用户名表单输入内容
driver.find_element_by_name("userName").send_keys(u'939580700@qq.com')
# 在密码表单输入内容
driver.find_element_by_name("password").send_keys(u'Ning939580700')

# verifycode = raw_input("请输入验证码：")
# # 将验证码输入到表单内
# driver.find_element_by_id("TANGRAM__PSP_10__verifyCode").send_keys(verifycode)
# driver.find_element_by_id("TANGRAM__PSP_10__submit").click()
# driver.save_screenshot("baidu_login.jpg")
