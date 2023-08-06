'''
Created on 2019年2月22日

@author: 67362
'''
# coding=utf-8
from .initLib import initlib
from SeleniumLibrary.base import keyword
from selenium.webdriver.common.keys import Keys
from SeleniumLibrary.base.librarycomponent import LibraryComponent
from selenium.common.exceptions import TimeoutException, WebDriverException, \
    NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from robot.utils.robottime import timestr_to_secs
from builtins import isinstance
from .commonutils import getBy, visibility_of_all_elements, \
    element_should_have_attribute_value, element_not_be_covered_and_click, \
    presence_of_element_located
from win32 import win32gui
from win32.lib import win32con
from time import sleep
import json
import traceback
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
import jpype
from .dubboenum import clustertype, rpc_protocol, registry_protocol, loadbalance
import os.path
import json

class commonkeywords(initlib):

    def __init__(self):
        # LibraryComponent.__init__(self, ctx)
        pass
    @keyword
    def get_builtin(self):
        return self.builtin

    @keyword
    def is_element_visible(self, locator, timeout=None):
        ls = locator.split("=", 1)
        selector = ls[0].upper()
        locpath = ls[1]
        if timeout == None:
            timeout = timestr_to_secs(self.selib.get_selenium_timeout())
        try:
            WebDriverWait(self.driver, int(timeout)).until(EC.visibility_of_element_located((getBy(selector), locpath)))
            return True
        except TimeoutException:
            return False

    @keyword
    def is_element_present(self, locator, timeout=None):
        ls = locator.split("=", 1)
        selector = ls[0].upper()
        locpath = ls[1]
        if timeout == None:
            timeout = timestr_to_secs(self.selib.get_selenium_timeout())
        try:
            WebDriverWait(self.driver, int(timeout)).until(EC.presence_of_element_located((getBy(selector), locpath)))
            return True
        except TimeoutException:
            return False

    @keyword
    def wait_element_present(self, locator, timeout=None, throwexception=True):
        ls = locator.split("=", 1)
        selector = ls[0].upper()
        locpath = ls[1]
        if timeout == None:
            timeout = timestr_to_secs(self.selib.get_selenium_timeout())
        try:
            return WebDriverWait(self.driver, int(timeout)).until(
                EC.presence_of_element_located((getBy(selector), locpath)))
        except TimeoutException as e:
            if throwexception:
                traceback.print_exc()
                raise NoSuchElementException("找不到定位为：" + locator + "的元素")
            else:
                return

    @keyword
    def wait_elements_present(self, locator, timeout=None):
        ls = locator.split("=", 1)
        selector = ls[0].upper()
        locpath = ls[1]
        if timeout == None:
            timeout = timestr_to_secs(self.selib.get_selenium_timeout())
        try:
            return WebDriverWait(self.driver, int(timeout)).until(
                EC.presence_of_all_elements_located((getBy(selector), locpath)))
        except TimeoutException as e:
            traceback.print_exc()
            raise NoSuchElementException("找不到定位为：" + locator + "的元素")

    @keyword
    def wait_text_to_be_present_in_element(self, locator, text, timeout=None):
        ls = locator.split("=", 1)
        selector = ls[0].upper()
        locpath = ls[1]
        if timeout == None:
            timeout = timestr_to_secs(self.selib.get_selenium_timeout())
        try:
            return WebDriverWait(self.driver, int(timeout)).until(
                EC.text_to_be_present_in_element((getBy(selector), locpath), text))
        except TimeoutException as e:
            traceback.print_exc()
            raise Exception("定位为：" + locator + "的元素不存在指定的文本：" + text)

    @keyword
    def wait_text_to_be_present_in_element_value(self, locator, text, timeout=None):
        ls = locator.split("=", 1)
        selector = ls[0].upper()
        locpath = ls[1]
        if timeout == None:
            timeout = timestr_to_secs(self.selib.get_selenium_timeout())
        try:
            return WebDriverWait(self.driver, int(timeout)).until(
                EC.text_to_be_present_in_element_value((getBy(selector), locpath), text))
        except TimeoutException as e:
            traceback.print_exc()
            raise Exception("定位为：" + locator + "的元素的value中不存在指定的文本：" + text)

    @keyword
    def wait_element_visible(self, locator, timeout=None):
        ls = locator.split("=", 1)
        selector = ls[0].upper()
        locpath = ls[1]
        if timeout == None:
            timeout = timestr_to_secs(self.selib.get_selenium_timeout())
        try:
            return WebDriverWait(self.driver, int(timeout)).until(
                EC.visibility_of_element_located((getBy(selector), locpath)))
        except TimeoutException as e:
            traceback.print_exc()
            raise ElementNotVisibleException("定位为：" + locator + "的元素不可见")

    @keyword
    def wait_element_not_visible(self, locator, timeout=None):
        ls = locator.split("=", 1)
        selector = ls[0].upper()
        locpath = ls[1]
        if timeout == None:
            timeout = timestr_to_secs(self.selib.get_selenium_timeout())
        try:
            return WebDriverWait(self.driver, int(timeout)).until_not(
                EC.visibility_of_element_located((getBy(selector), locpath)))
        except TimeoutException as e:
            traceback.print_exc()
            raise Exception("定位为：" + locator + "的元素超过等待时间依然可见")

    @keyword
    def wait_element_not_present(self, locator, timeout=None):
        ls = locator.split("=", 1)
        selector = ls[0].upper()
        locpath = ls[1]
        if timeout == None:
            timeout = timestr_to_secs(self.selib.get_selenium_timeout())
        try:
            return WebDriverWait(self.driver, int(timeout)).until_not(
                EC.presence_of_element_located((getBy(selector), locpath)))
        except TimeoutException as e:
            traceback.print_exc()
            raise Exception("定位为：" + locator + "的元素超过等待时间依然存在")

    @keyword
    def wait_elements_all_visible(self, locator, timeout=None):
        ls = locator.split("=", 1)
        selector = ls[0].upper()
        locpath = ls[1]
        if timeout == None:
            timeout = timestr_to_secs(self.selib.get_selenium_timeout())
        try:
            return WebDriverWait(self.driver, int(timeout)).until(
                EC.visibility_of_all_elements_located((getBy(selector), locpath)))
        except TimeoutException as e:
            traceback.print_exc()
            raise ElementNotVisibleException("定位为：" + locator + "的元素集存在不可见元素")

    @keyword
    def wait_elements_any_visible(self, locator, timeout=None):
        ls = locator.split("=", 1)
        selector = ls[0].upper()
        locpath = ls[1]
        if timeout == None:
            timeout = timestr_to_secs(self.selib.get_selenium_timeout())
        try:
            return WebDriverWait(self.driver, int(timeout)).until(
                EC.visibility_of_any_elements_located((getBy(selector), locpath)))
        except TimeoutException as e:
            traceback.print_exc()
            raise ElementNotVisibleException("定位为：" + locator + "的元素集都不可见")

    @keyword
    def wait_element_clickable(self, locator, timeout=None):
        ls = locator.split("=", 1)
        selector = ls[0].upper()
        locpath = ls[1]
        if timeout == None:
            timeout = timestr_to_secs(self.selib.get_selenium_timeout())
        try:
            return WebDriverWait(self.driver, int(timeout)).until(
                EC.element_to_be_clickable((getBy(selector), locpath)))
        except TimeoutException as e:
            traceback.print_exc()
            raise Exception("定位为：" + locator + "的元素不可点击")

    @keyword
    def is_element_clickable(self, locator, timeout=None):
        ls = locator.split("=", 1)
        selector = ls[0].upper()
        locpath = ls[1]
        if timeout == None:
            timeout = timestr_to_secs(self.selib.get_selenium_timeout())
        try:
            WebDriverWait(self.driver, int(timeout)).until(EC.element_to_be_clickable((getBy(selector), locpath)))
            return True
        except TimeoutException:
            return False

    @keyword
    def is_element_not_be_covered_and_yes_to_click(self, locator, timeout=None):
        if timeout == None:
            timeout = timestr_to_secs(self.selib.get_selenium_timeout())
        try:
            e = self.find_element(locator)
            return WebDriverWait(self.driver, int(timeout)).until(element_not_be_covered_and_click(self.driver, e))
        except TimeoutException:
            return False

    @keyword
    def wait_element_visible_from_element(self, element, locator, timeout=None):
        ls = locator.split("=", 1)
        selector = ls[0].upper()
        locpath = ls[1]
        if timeout == None:
            timeout = timestr_to_secs(self.selib.get_selenium_timeout())
        try:
            return WebDriverWait(self.driver, int(timeout)).until(
                EC.visibility_of(element.find_element(getBy(selector), locpath)))
        except TimeoutException as e:
            traceback.print_exc()
            raise NoSuchElementException("定位为" + element.location + "的元素下定位为：" + locator + "的元素不可见")

    @keyword
    def wait_element_present_from_element(self, element, locator, timeout=None):
        ls = locator.split("=", 1)
        selector = ls[0].upper()
        locpath = ls[1]
        if timeout == None:
            timeout = timestr_to_secs(self.selib.get_selenium_timeout())
        try:
            return WebDriverWait(self.driver, int(timeout)).until(
                presence_of_element_located(element, getBy(selector), locpath))
        except TimeoutException as e:
            traceback.print_exc()
            raise NoSuchElementException("定位为" + element.location + "的元素下找不到定位为：" + locator + "的元素")

    @keyword
    def wait_element_not_visible_from_element(self, element, locator, timeout=None):
        ls = locator.split("=", 1)
        selector = ls[0].upper()
        locpath = ls[1]
        if timeout == None:
            timeout = timestr_to_secs(self.selib.get_selenium_timeout())
        try:
            return WebDriverWait(self.driver, int(timeout)).until_not(
                EC.visibility_of(element.find_element(getBy(selector), locpath)))
        except TimeoutException as e:
            traceback.print_exc()
            raise Exception("定位为" + element.location + "的元素下定位为：" + locator + "的元素超过等待时间依然可见")

    @keyword
    def wait_elements_visible_from_element(self, element, locator, timeout=None):
        ls = locator.split("=", 1)
        selector = ls[0].upper()
        locpath = ls[1]
        if timeout == None:
            timeout = timestr_to_secs(self.selib.get_selenium_timeout())
        try:
            e1 = element.find_elements(getBy(selector), locpath)
            return WebDriverWait(self.driver, int(timeout)).until(visibility_of_all_elements(e1))
        except TimeoutException as e:
            traceback.print_exc()
            raise ElementNotVisibleException("定位为" + locator + "的元素下定位为" + locator + "的元素不是全部可见")

    @keyword
    def wait_element_not_clickable(self, locator, timeout=None):
        ls = locator.split("=", 1)
        selector = ls[0].upper()
        locpath = ls[1]
        if timeout == None:
            timeout = timestr_to_secs(self.selib.get_selenium_timeout())
        try:
            return WebDriverWait(self.driver, int(timeout)).until_not(
                EC.element_to_be_clickable((getBy(selector), locpath)))
        except TimeoutException as e:
            traceback.print_exc()
            raise Exception("定位为：" + locator + "的元素超过等待时间依旧可点击")

    @keyword
    def wait_element_have_attribute_value(self, locator, attributename, value, timeout=None):
        if timeout == None:
            timeout = timestr_to_secs(self.selib.get_selenium_timeout())
        try:
            return WebDriverWait(self.driver, int(timeout)).until(
                element_should_have_attribute_value(self.find_element(locator), attributename, value))
        except TimeoutException as e:
            traceback.print_exc()
            raise Exception("定位为：" + locator + "的元素属性" + attributename + "的值超过等待时间仍旧不包含:" + value + "，期望包含")

    @keyword
    def wait_element_have_not_attribute_value(self, locator, attributename, value, timeout=None):
        if timeout == None:
            timeout = timestr_to_secs(self.selib.get_selenium_timeout())
        try:
            return WebDriverWait(self.driver, int(timeout)).until_not(
                element_should_have_attribute_value(self.find_element(locator), attributename, value))
        except TimeoutException as e:
            traceback.print_exc()
            raise Exception("定位为：" + locator + "的元素属性" + attributename + "的值超过等待时间仍旧包含:" + value + "，期望不包含")

    @keyword
    def click_button_new(self, locator, timeout=None):
        #         self.selib.wait_until_element_is_visible(locator, timeout,error=None)
        time1 = int(time.time())
        self.wait_element_clickable(locator, timeout)
        use_time = int(time.time()) - time1
        try:
            self.selib.click_button(locator)
        except WebDriverException as e:
            if "Other element would receive the click" in repr(
                    e) or "element click intercepted: Element is not clickable at point" in repr(e):
                if timeout == None:
                    timeout = timestr_to_secs(self.selib.get_selenium_timeout())
                self.click_on_hide_element(locator, int(timeout) - use_time)
            #                 self.is_element_not_be_covered_and_yes_to_click(locator, timeout - use_time)
            else:
                traceback.print_exc()
                raise Exception("定位为：" + locator + "的元素不可点击")

    @keyword
    def click_element_new(self, locator, timeout=None):
        #         self.selib.wait_until_element_is_visible(locator, timeout,error=None)
        time1 = int(time.time())
        self.wait_element_clickable(locator, timeout)
        use_time = int(time.time()) - time1
        try:
            self.selib.click_element(locator)
        except WebDriverException as e:
            if "Other element would receive the click" in repr(
                    e) or "element click intercepted: Element is not clickable at point" in repr(e):
                if timeout == None:
                    timeout = timestr_to_secs(self.selib.get_selenium_timeout())
                self.click_on_hide_element(locator, int(timeout) - use_time)
            #                 self.is_element_not_be_covered_and_yes_to_click(locator, timeout - use_time)
            else:
                traceback.print_exc()
                raise Exception("定位为：" + locator + "的元素不可点击")

    @keyword
    def click_until_element_visible(self, locator1, locator2, timeout=None):
        index = 1
        if timeout == None:
            timeout = timestr_to_secs(self.selib.get_selenium_timeout())
        while index <= int(timeout) and not self.is_element_visible(locator2, 1):
            self.click_element_new(locator1)
            index += 1

    @keyword
    def click_image_new(self, locator, timeout=None):
        #         self.selib.wait_until_element_is_visible(locator, timeout,error=None)
        time1 = int(time.time())
        self.wait_element_clickable(locator, timeout)
        use_time = int(time.time()) - time1
        try:
            self.selib.click_image(locator)
        except WebDriverException as e:
            if "Other element would receive the click" in repr(
                    e) or "element click intercepted: Element is not clickable at point" in repr(e):
                if timeout == None:
                    timeout = timestr_to_secs(self.selib.get_selenium_timeout())
                self.click_on_hide_element(locator, int(timeout) - use_time)
            #                 self.is_element_not_be_covered_and_yes_to_click(locator, timeout - use_time)
            else:
                traceback.print_exc()
                raise Exception("定位为：" + locator + "的元素不可点击")

    @keyword
    def click_link_new(self, locator, timeout=None):
        #         self.selib.wait_until_element_is_visible(locator, timeout,error=None)
        time1 = int(time.time())
        self.wait_element_clickable(locator, timeout)
        use_time = int(time.time()) - time1
        try:
            self.selib.click_link(locator)
        except WebDriverException as e:
            if "Other element would receive the click" in repr(
                    e) or "element click intercepted: Element is not clickable at point" in repr(e):
                if timeout == None:
                    timeout = timestr_to_secs(self.selib.get_selenium_timeout())
                self.click_on_hide_element(locator, int(timeout) - use_time)
            #                 self.is_element_not_be_covered_and_yes_to_click(locator, timeout - use_time)
            else:
                traceback.print_exc()
                raise Exception("定位为：" + locator + "的元素不可点击")

    @keyword
    def double_click_element_new(self, locator, timeout=None):
        #         self.selib.wait_until_element_is_visible(locator,timeout,error=None)
        self.wait_element_clickable(locator, timeout)
        self.selib.double_click_element(locator)

    @keyword
    def input_text_new(self, locator, text):
        self.clear_input_text(locator)
        self.selib.input_text(locator, text)

    @keyword
    def clear_input_text(self, locator):
        self.press_keys(locator, self.keys("CONTROL"), "a")
        self.press_keys(locator, self.keys("BACKSPACE"))

    @keyword
    def find_element(self, locator, timeout=None):
        self.wait_element_present(locator, timeout)
        return self.selib.get_webelement(locator)

    @keyword
    def find_elements(self, locator, timeout=None):
        self.wait_elements_present(locator, timeout)
        return self.selib.get_webelements(locator)

    @keyword
    def get_webelement_new(self, locator):
        self.wait_element_present(locator)
        return self.selib.get_webelement(locator);

    @keyword
    def get_webelements_new(self, locator):
        self.wait_elements_present(locator)
        return self.selib.get_webelements(locator);

    @keyword
    def find_element_from_parent(self, element, locator):
        ls = locator.split("=", 1)
        selector = ls[0].upper()
        locpath = ls[1]
        self.wait_element_present_from_element(element, locator)
        return element.find_element(getBy(selector), locpath)

    @keyword
    def press_keys(self, locator, *keystr):
        self.selib.wait_until_element_is_visible(locator)
        self.find_element(locator).send_keys(keystr)

    @keyword
    def element_text_should_be_new(self, locator, expected, message=None, ignore_case=False, timeout=None):
        self.wait_element_present(locator, timeout)
        self.selib.element_text_should_be(locator, expected, message, ignore_case)

    @keyword
    def element_textcontent_should_be(self, locator, expected, ignore_space=False):
        tcontent = self.find_element(locator).get_attribute('textContent')
        if ignore_space != False:
            tcontent = tcontent.replace(" ", "")
        self.builtin.should_be_equal(tcontent, expected)

    @keyword
    def element_value_should_be(self, locator, expected):
        self.builtin.should_be_equal(self.get_value_new(locator), expected)

    @keyword
    def element_should_be_visible_new(self, locator, message=None):
        self.wait_element_present(locator)
        self.selib.element_should_be_visible(locator, message)

    @keyword
    def element_should_not_be_visible_new(self, locator, message=None):
        self.wait_element_present(locator)
        self.selib.element_should_not_be_visible(locator, message)

    @keyword
    def keys(self, keyname):
        map = {
            "NULL": Keys.NULL,
            "HELP": Keys.HELP,
            "CANCEL": Keys.CANCEL,
            "BACKSPACE": Keys.BACKSPACE,
            "BACK_SPACE": Keys.BACKSPACE,
            "TAB": Keys.TAB,
            "CLEAR": Keys.CLEAR,
            "RETURN": Keys.RETURN,
            "ENTER": Keys.ENTER,
            "SHIFT": Keys.SHIFT,
            "LEFT_SHIFT": Keys.SHIFT,
            "CONTROL": Keys.CONTROL,
            "LEFT_CONTROL": Keys.LEFT_CONTROL,
            "ALT": Keys.ALT,
            "LEFT_ALT": Keys.ALT,
            "PAUSE": Keys.PAUSE,
            "ESCAPE": Keys.ESCAPE,
            "SPACE": Keys.SPACE,
            "PAGE_UP": Keys.PAGE_UP,
            "PAGE_DOWN": Keys.PAGE_DOWN,
            "END": Keys.END,
            "HOME": Keys.HOME,
            "LEFT": Keys.LEFT,
            "ARROW_LEFT": Keys.ARROW_LEFT,
            "RIGHT": Keys.RIGHT,
            "ARROW_UP": Keys.ARROW_UP,
            "ARROW_Right": Keys.ARROW_RIGHT,
            "UP": Keys.UP,
            "DOWN": Keys.DOWN,
            "ARROW_DOWN": Keys.ARROW_DOWN,
            "MULTIPLY": Keys.MULTIPLY,
            "ADD": Keys.ADD,
            "SEPARATOR": Keys.SEPARATOR,
            "SUBTRACT": Keys.SUBTRACT,
            "DECIMAL": Keys.DECIMAL,
            "DIVIDE": Keys.DIVIDE,
            "SEMICOLON": Keys.SEMICOLON,
            "EQUALS": Keys.EQUALS,
            "DELETE": Keys.DELETE,
            "INSERT": Keys.INSERT,
            "NUMPAD0": Keys.NUMPAD0,
            "NUMPAD1": Keys.NUMPAD1,
            "NUMPAD2": Keys.NUMPAD2,
            "NUMPAD3": Keys.NUMPAD3,
            "NUMPAD4": Keys.NUMPAD4,
            "NUMPAD5": Keys.NUMPAD5,
            "NUMPAD6": Keys.NUMPAD6,
            "NUMPAD7": Keys.NUMPAD7,
            "NUMPAD8": Keys.NUMPAD8,
            "NUMPAD9": Keys.NUMPAD9,
            "META": Keys.META,
            "COMMAND": Keys.COMMAND,
            "F1": Keys.F1,
            "F2": Keys.F2,
            "F3": Keys.F3,
            "F4": Keys.F4,
            "F5": Keys.F5,
            "F6": Keys.F6,
            "F7": Keys.F7,
            "F8": Keys.F8,
            "F9": Keys.F9,
            "F10": Keys.F10,
            "F11": Keys.F11,
            "F12": Keys.F12
        }
        key = map.get(keyname)
        if key is None:
            key = keyname
        return key

    @keyword
    def get_text_for_element(self, element):
        return element.text

    @keyword
    def get_text_new(self, locator, timeout=None):
        self.wait_element_present(locator, timeout)
        return self.selib.get_text(locator)

    @keyword
    def check_value_from_dic_to_list(self, *l, **dic):
        if isinstance(dic, dict):
            for key in dic:
                self.builtin.should_be_equal(l[int(key)], dic[key])
        else:
            raise Exception

    @keyword
    def scrollToHead(self):
        js = "var q=document.body.scrollTop=0"
        self.driver.execute_script(js)

    @keyword
    def wait_jquery_loaded(self, timeout=None):
        self.selib.wait_for_condition("return jQuery.active == 0", timeout)

    @keyword
    def get_num_from_string(self, string):
        l = list(filter(str.isdigit, string))
        return int(''.join(l))

    @keyword
    def windows_loadfile(self, file):
        browsertype = self.get_browser_type()
        tmpstr = ""
        if browsertype == 'chrome' or browsertype == 'edge':
            tmpstr = u'打开'
        elif browsertype == 'firefox':
            tmpstr = u'上传附件'
        dialog = win32gui.FindWindow('#32770', tmpstr)  # 对话框
        ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None)
        ComboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, 'ComboBox', None)
        Edit = win32gui.FindWindowEx(ComboBox, 0, 'Edit', None)  # 上面三句依次寻找对象，直到找到输入框Edit对象的句柄
        button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 确定按钮Button 
        win32gui.SendMessage(Edit, win32con.WM_SETTEXT, None, file)  # 往输入框输入绝对地址
        win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 按button

    @keyword
    def get_browser_type(self):
        ls = str(self.driver).split(".")
        return ls[2].lower()

    @keyword
    def exc_func_from_dict(self, **dic):
        for key in dic:
            eval(key)(*dic[key])

    @keyword
    def get_value_new(self, locator):
        self.wait_element_present(locator)
        return self.selib.get_value(locator)

    @keyword
    def get_element_attribute_new(self, locator, attribute=None):
        self.wait_element_present(locator)
        return self.selib.get_element_attribute(locator, attribute)

    @keyword
    def get_element_count_new(self, locator):
        self.wait_element_present(locator)
        return self.selib.get_element_count(locator)

    @keyword
    def assign_id_to_element_new(self, locator, id):
        self.selib.wait_until_element_is_enabled(locator)
        self.selib.assign_id_to_element(locator, id)

    @keyword
    def checkbox_should_be_selected_new(self, locator):
        self.selib.wait_until_element_is_enabled(locator)
        self.selib.checkbox_should_be_selected(locator)

    @keyword
    def checkbox_should_not_be_selected_new(self, locator):
        self.selib.wait_until_element_is_enabled(locator)
        self.selib.checkbox_should_not_be_selected(locator)

    @keyword
    def choose_file_new(self, locator, filepath):
        self.selib.wait_until_element_is_enabled(locator)
        self.selib.choose_file(locator, filepath)

    @keyword
    def clear_element_text_new(self, locator):
        self.selib.wait_until_element_is_enabled(locator)
        self.selib.clear_element(locator)

    @keyword
    def drag_and_drop_new(self, locator, target):
        self.selib.wait_until_element_is_enabled(locator)
        self.selib.drag_and_drop(locator, target)

    @keyword
    def drag_and_drop_by_offset_new(self, locator, xoffset, yoffset):
        self.selib.wait_until_element_is_enabled(locator)
        self.selib.drag_and_drop_by_offset(locator, xoffset, yoffset)

    @keyword
    def table_cell_should_contain_new(self, locator, row, column, expected, loglevel=None):
        self.selib.wait_until_element_is_enabled(locator)
        self.selib.table_cell_should_contain(locator, row, column, expected, loglevel)

    @keyword
    def select_frame_new(self, locator):
        ls = locator.split("=", 1)
        selector = ls[0].upper()
        locpath = ls[1]
        timeout = timestr_to_secs(self.selib.get_selenium_timeout())
        try:
            WebDriverWait(self.driver, int(timeout)).until(
                EC.frame_to_be_available_and_switch_to_it((getBy(selector), locpath)))
        except TimeoutException as e:
            traceback.print_exc()
            raise Exception("切换到定位为：" + locator + "的iframe失败")

    @keyword
    def hide_elements_forcss(self, csstext):
        jstext = "var es = document.querySelectorAll(\"." + csstext + ":not([style*='display: none'])\");for (var i = 0; i < es.length; i++) {es[i].style.display='none'};"
        self.driver.execute_script(jstext)

    @keyword
    def wait_page_loaded(self, timeout=None):
        self.se2lib.wait_for_condition("return ($.active == 0)", timeout)

    @keyword
    def wait_document_loaded(self, timeout=None):
        self.se2lib.wait_for_condition("return (document.readyState == 'complete')", timeout)
        self.scrollToHead()

    @keyword
    def scroll_to_bottom(self, scroll_css):
        jstext = "document.querySelectorAll(\"" + scroll_css + "\")[0].scrollTop=100000"
        self.driver.execute_script(jstext)

    @keyword
    def scroll_to_element_clickable_and_click(self, locator, scroll_css):
        jstext = "document.querySelectorAll(\"" + scroll_css + "\")[0].scrollTop="
        self.driver.execute_script(jstext + "0")
        index = 1
        while index <= 100 and not (
                self.is_element_clickable(locator, 1) and self.is_element_not_be_covered_and_yes_to_click(locator, 1)):
            self.driver.execute_script(jstext + str(100 * index))
            index += 1

    @keyword
    def scroll_to_element_clickable(self, locator, scroll_css):
        jstext = "document.querySelectorAll(\"" + scroll_css + "\")[0].scrollTop="
        self.driver.execute_script(jstext + "0")
        index = 1
        while index <= 100 and not (self.is_element_clickable(locator, 1)):
            self.driver.execute_script(jstext + str(100 * index))
            index += 1

    @keyword
    def click_on_hide_element(self, locator, timeout=None):
        self.driver.execute_script("arguments[0].click()", self.find_element(locator, timeout));

    @keyword
    def juma_string_to_json(self, strlist):
        """可以用来转换string对象为list或者dic，如["a","b"]转为列表,{"a":"b"}转为字典
        """
        try:
            list_list = json.loads(strlist)
        except Exception as e:

            raise e
        return list_list

    @keyword
    def current_date(self):
        strDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 这里格式是‘%Y-%m-%d’，可有其他格式，也可只求年和月。
        return strDate

    @keyword
    def move_to_element(self, locator):
        element = self.find_element(locator)
        action = ActionChains(self.driver)
        action.move_to_element(element).perform()

    @keyword
    def dic_to_json(self,dic):
        return json.dumps(dic)

    @keyword
    def wait_until(self, condition,timeout=10,internal=1):
        timesec = 0
        while True:
            if self._is_true(condition) or timesec >= timeout:
                break
            else:
                timesec += internal
                sleep(internal)
    def _is_true(self, condition):
        if self._is_string(condition):
            condition = self.builtin.evaluate(condition)
        return bool(condition)

    def _is_string(self,item):
        return isinstance(item, str)
