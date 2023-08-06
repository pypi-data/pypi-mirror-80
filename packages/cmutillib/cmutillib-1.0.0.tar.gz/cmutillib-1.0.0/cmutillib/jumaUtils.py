# coding=utf-8

from .commonkeywords import commonkeywords
from SeleniumLibrary.base import keyword
from SeleniumLibrary.base.librarycomponent import LibraryComponent

from robot.api import TestSuite
from robot.reporting.resultwriter import ResultWriter
from time import sleep
from .jumalocator import jumalocator
import pathlib
from robot.utils.robottime import timestr_to_secs
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class jumaUtils(commonkeywords):

    def __init__(self):
        # LibraryComponent.__init__(self, ctx)
        pass
    def click_menu_into_page(self, *menulist):
        locator = jumalocator.locator_menu_div
        tmpstr = "/div/ul/li/"
        if "auth-manage" in self.selib.get_location() and "#/entry/" in self.selib.get_location():
            get_current_menu = False
        else:
            get_current_menu = True
            current_menu_list = self.get_webelements_new(jumalocator.current_menu_text)
        index = 0;
        for menustr in menulist:
            index += 1
            if get_current_menu == True:
                if menustr == current_menu_list[index - 1].text:
                    locator += tmpstr
                    continue
                elif index == 1:
                    current_menu_list[0].click()
                    self.wait_element_not_visible_from_element(current_menu_list[0], "xpath=./following-sibling::*")
            if index < len(menulist):
                locator += tmpstr + "div"
            else:
                locator += tmpstr
            locat_laststr = locator + "/a[descendant::strong[normalize-space(text())='" + menustr + "']]"
            self.selib.wait_until_element_is_visible(locat_laststr)
            sleep(0.5)
            self.click_element_new(locat_laststr)
            if index == len(menulist):
                self.wait_document_loaded()

    #             if index < 3 :
    #                 self.wait_element_visible_from_element(self.find_element(locat_laststr), "xpath=./following-sibling::*")
    #             element = self.find_element(locat_laststr)
    #             action = ActionChains(self.driver)
    #             action.move_to_element(element).perform()
    #             self.scroll_to_element_clickable_and_click(locat_laststr, "#c-layout-left")
    #             element.click()

    @keyword
    def wait_date_picker_visible(self):
        self.wait_elements_any_visible(jumalocator.loc_date_picker)

    @keyword
    def getDriver(self):
        return self.driver

    @keyword
    def wait_spin_loaded(self):
        """等待加载旋转框加载完毕
        """
        self.wait_element_present(jumalocator.loadding_spin, 1, False)
        self.wait_element_not_present(jumalocator.loadding_spin)

    @keyword
    def wait_message_info_loaded(self):
        self.wait_element_present(jumalocator.current_message_info, 1, False)
        self.wait_element_not_present(jumalocator.current_message_info)

    @keyword
    def get_message_info(self, timeout=None):
        return self.get_text_new(jumalocator.current_message_info, timeout)

    @keyword
    def context_menu_select(self, parent_tenantname=None, child_tenantname=None):
        if parent_tenantname != None and (parent_tenantname not in self.get_text_new(jumalocator.parent_tenant)):
            self.hide_elements_forcss(jumalocator.all_context_menu)
            self.click_element_new(jumalocator.parent_tenant)
            #             self.click_element_new(jumalocator.current_context_menu + "/a[descendant::*[normalize-space(text())='"+parent_tenantname+"']]")
            self.scroll_to_element_clickable_and_click(
                jumalocator.current_context_menu + "/a[descendant::*[normalize-space(text())='" + parent_tenantname + "']]",
                ".c-context-menu:not([style*='display: none'])")
            #             self.wait_spin_loaded()
            i = 0
            while (i < 60):
                if self.is_element_present(jumalocator.loadding_spin, 10):
                    break
                self.hide_elements_forcss(jumalocator.all_context_menu)
                self.click_element_new(jumalocator.parent_tenant)
                self.scroll_to_element_clickable_and_click(
                    jumalocator.current_context_menu + "/a[descendant::*[normalize-space(text())='" + parent_tenantname + "']]",
                    ".c-context-menu:not([style*='display: none'])")
                i += 10
            self.wait_element_not_present(jumalocator.loadding_spin)
        #             self.wait_document_loaded()
        if child_tenantname != None and (child_tenantname not in self.get_text_new(jumalocator.child_tenant)):
            self.hide_elements_forcss(jumalocator.all_context_menu)
            self.click_element_new(jumalocator.child_tenant)
            self.scroll_to_element_clickable_and_click(
                jumalocator.current_context_menu + "/a[descendant::*[normalize-space(text())='" + child_tenantname + "']]",
                ".c-context-menu:not([style*='display: none'])")
            #             self.click_element_new(jumalocator.current_context_menu + "/a[descendant::*[normalize-space(text())='"+child_tenantname+"']]")
            #             self.wait_spin_loaded()
            i = 0
            while (i < 60):
                if self.is_element_present(jumalocator.loadding_spin, 10):
                    break
                self.hide_elements_forcss(jumalocator.all_context_menu)
                self.click_element_new(jumalocator.parent_tenant)
                self.scroll_to_element_clickable_and_click(
                    jumalocator.current_context_menu + "/a[descendant::*[normalize-space(text())='" + child_tenantname + "']]",
                    ".c-context-menu:not([style*='display: none'])")
                i += 10
            self.wait_element_not_present(jumalocator.loadding_spin)

    #             self.wait_document_loaded()
    @keyword
    def select_dropdown_transfer(self, showselect_locator, text):
        """
        ivu-select-dropdown-transfer
        """
        self.hide_elements_forcss(jumalocator.all_ivuselectdropdowntransfer_css)
        self.click_element_new(showselect_locator)
        e = self.find_element(
            jumalocator.current_ivuselectdropdowntransfer + "/ul/li[normalize-space(text())='" + text + "']")
        if "ivu-select-item-selected" not in e.get_attribute("class"):
            locator2 = jumalocator.current_ivuselectdropdowntransfer + "/ul/li[normalize-space(text())='" + text + "']"
            self.scroll_to_element_clickable(locator2,
                                             ".ivu-select-dropdown.ivu-select-dropdown-transfer:not([style*='display: none'])")
            self.click_element_new(locator2)
        #             e.click()
        self.hide_elements_forcss(jumalocator.all_ivuselectdropdowntransfer_css)

    @keyword
    def dropdown_transfer_menu(self, showselect_locator, text):
        """
        ivu-dropdown-transfer下menu
        """
        self.hide_elements_forcss(jumalocator.all_ivudropdowntransfer_css)
        self.click_element_new(showselect_locator)
        self.click_element_new(
            jumalocator.current_ivudropdowntransfer + "/ul/li[descendant::*[normalize-space(text())='" + text + "']]")
        self.hide_elements_forcss(jumalocator.all_ivudropdowntransfer_css)

    @keyword
    def dropdown_transfer_treeview(self, showselect_locator, treemenu):
        """
        ivu-dropdown-transfer下treeview
        param: showselect_locator: 触发该选择框的元素的locator
        param: treemenu:  要选择的多级目录，以,相隔
        """
        self.hide_elements_forcss(jumalocator.all_ivudropdowntransfer_css)
        self.click_element_new(showselect_locator)
        treemenulist = treemenu.split(",")
        tmpstr = ""
        i = 1
        for s in treemenulist:
            if tmpstr == "":
                pass
            else:
                tmpstr += "->"
            tmpstr += s
            if i >= len(treemenulist):
                locator1 = jumalocator.current_ivudropdowntransfer + "//a[@title='" + tmpstr + "']/i[2]"
                ele = self.wait_element_visible(locator1)
                if "c-treeview-radio-checked" in ele.get_attribute("class"):
                    pass
                else:
                    ele.click()
            else:
                classtext = self.selib.get_element_attribute(
                    jumalocator.current_ivudropdowntransfer + "//a[@title='" + tmpstr + "']/i[1]", "class")
                if "c-treeview-fold-open" in classtext:
                    pass
                else:
                    self.click_element_new(jumalocator.current_ivudropdowntransfer + "//a[@title='" + tmpstr + "']")
                    locator2 = jumalocator.current_ivudropdowntransfer + "//a[@title='" + tmpstr + "']/following-sibling::*[contains(@class,'c-treeview-child') and contains(@style,'display: block')]"
                    self.scroll_to_element_clickable(locator2, "div:not([style*='display: none']) .ivu-dropdown-menu")
                    self.wait_element_visible(locator2)
            #                     self.wait_element_present(jumalocator.current_ivudropdowntransfer + "//a[@title='"+tmpstr+"']/following-sibling::*[contains(@class,'c-treeview-child') and contains(@style,'display: block')]")
            i += 1
        self.hide_elements_forcss(jumalocator.all_ivudropdowntransfer_css)

    def exec_keyword(self, path_to_file, keyword, arg=None):
        """    执行RobotFramework的关键字
        :param path_to_file: String，RobotFramework文件的路径，一般是执行文件的相对路径，绝对路径也可以
        :param keyword: String，执行的关键字
        :param arg: List[String], 执行关键字的参数，如果没有则不传
        :return: None， 没有返回则表示执行通过，可以查看执行文件目录下的log.html来定位问题
        """
        suite = TestSuite('Test')
        suite.resource.imports.resource(path_to_file)
        test = suite.tests.create('TEST', tags=['smoke'])
        if arg:
            if isinstance(arg, list):
                test.keywords.create(keyword.decode('utf-8'), args=arg)
            else:
                raise TypeError('args must be list')
        else:
            test.keywords.create(keyword.decode('utf-8'))
        result = suite.run(critical='smoke')
        if result.suite.status == 'PASS':
            pass
        else:
            ResultWriter('test.xml').write_results()

    @keyword
    def get_table_element(self, rownum, colnum, tableindex=1, findpath=None):
        """获得table中元素
        :param tableindex: int类型,第几个table
        :param rownum: int类型,要找元素所在行
        :param colnum: int类型,要找元素所在列
        """
        tbodys = self.get_webelements_new(jumalocator.table_bodys)
        if findpath == None:
            findpath = ""
        return self.wait_element_visible_from_element(tbodys[int(tableindex) - 1],
                                                      "xpath=./table/tbody/tr[" + rownum + "]/td[" + colnum + "]" + findpath)

    @keyword
    def table_select_all(self, tableindex=1):
        loc = jumalocator.loc_table_select_all + str(tableindex) + jumalocator.loc_table_select_all_2
        if "ivu-checkbox-checked" not in self.find_element(loc).get_attribute("class"):
            self.click_element_new(loc)

    @keyword
    def table_deselect_all(self, tableindex=1):
        loc = jumalocator.loc_table_select_all + str(tableindex) + jumalocator.loc_table_select_all_2
        if "ivu-checkbox-checked" in self.find_element(loc).get_attribute("class"):
            self.click_element_new(loc)

    @keyword
    def table_select_row(self, rowindex, tableindex=1):
        loc = jumalocator.loc_table_select_index + str(tableindex) + jumalocator.loc_table_select_index2 + str(
            rowindex) + jumalocator.loc_table_select_index3
        if "ivu-checkbox-checked" not in self.find_element(loc).get_attribute("class"):
            self.click_element_new(loc)

    @keyword
    def table_deselect_row(self, rowindex, tableindex=1):
        loc = jumalocator.loc_table_select_index + str(tableindex) + jumalocator.loc_table_select_index2 + str(
            rowindex) + jumalocator.loc_table_select_index3
        if "ivu-checkbox-checked" in self.find_element(loc).get_attribute("class"):
            self.click_element_new(loc)

    @keyword
    def table_select_rows(self, tableindex=1, *rowindexlist):
        for rowindex in self.get_table_row_count(tableindex):
            if rowindex in rowindexlist:
                self.table_select_row(rowindex, tableindex)
            else:
                self.table_deselect_row(rowindex, tableindex)

    @keyword
    def click_table_element(self, rownum, colnum, tableindex=1, findpath=None):
        self.get_table_element(rownum, colnum, tableindex, findpath).click()

    @keyword
    def get_table_element_text(self, rownum, colnum, tableindex=1, findpath=None):
        return self.get_table_element(rownum, colnum, tableindex, findpath).text

    @keyword
    def get_table_row_text_list(self, rownum, tableindex=1):
        """获得table中某一行所有元素文本的列表
        :param tableindex: int类型,第几个table
        :param rownum: int类型,要找元素所在行
        :param colnum: int类型,要找元素所在列
        """
        l = []
        tbodys = self.find_elements(jumalocator.table_bodys)
        es = self.wait_elements_visible_from_element(tbodys[int(tableindex) - 1],
                                                     "xpath=./table/tbody/tr[" + rownum + "]/td")
        for e in es:
            l.append(e.text)
        return l

    @keyword
    def get_table_result_count(self, tableindex=1):
        rn = self.find_elements(jumalocator.loc_table_resultnum)
        rtext = rn[int(tableindex) - 1].text.split(",")[0]
        return self.get_num_from_string(rtext)

    @keyword
    def get_table_row_count(self, tableindex=1):
        return len(self.find_elements(
            jumalocator.loc_table_select_index + str(tableindex) + jumalocator.loc_table_select_index_all))

    @keyword
    def is_table_result_empty(self, timeout=None):
        if self.is_element_visible(jumalocator.loc_ivu_table_tip, timeout) and not (
        self.is_element_visible(jumalocator.loc_ivu_table_body, timeout)):
            return True
        elif not (self.is_element_visible(jumalocator.loc_ivu_table_tip, timeout)) and self.is_element_visible(
                jumalocator.loc_ivu_table_body, timeout):
            return False

    @keyword
    def wait_table_loaded(self, timeout=None):
        self.wait_element_present(jumalocator.current_table_loading, timeout)
        self.wait_element_not_present(jumalocator.current_table_loading, timeout)

    @keyword
    def click_modal_btn_for_text(self, text):
        es = self.find_elements(jumalocator.loc_current_modal_warp)
        index = 0
        ls = []
        maxsize = 0
        maxindex = 0
        while (index < len(es)):
            jstext = "var e = document.querySelectorAll('.ivu-modal-wrap:not(.ivu-modal-hidden)')[" + str(
                index) + "];var a = window.getComputedStyle(e).zIndex;return a;"
            size = int(self.driver.execute_script(jstext))
            ls.append(size)
            if maxsize <= size:
                maxsize = size
                maxindex = index
            index += 1
        self.find_element_from_parent(es[maxindex], jumalocator.current_modal_btn_for_text + text + "']]").click()

    #         self.click_button_new(jumalocator.current_modal_btn_for_text+text+"']]")
    @keyword
    def auto_complete_list_select(self, showlist_locator, text, selectindex=1):
        ele = self.find_element(showlist_locator)
        self.find_element_from_parent(ele, jumalocator.loc_auto_complete_close).click();
        self.input_text_new(showlist_locator, text)
        auto_list_id = self.find_element_from_parent(ele, jumalocator.loc_find_auto_complete_list).get_attribute("id")
        #         auto_list_id = self.get_webelement_new(jumalocator.auto_list).get_attribute("id")
        self.wait_element_not_present(jumalocator.auto_list_active)
        self.click_element_new(
            jumalocator.auto_list_select + auto_list_id + jumalocator.auto_list_select_tailstr + str(selectindex) + "]")
        self.wait_element_not_visible(jumalocator.auto_list_select + auto_list_id + "']")

    @keyword
    def auto_complete_list_select_new(self, showlist_locator, text, selectindex=1):
        self.hide_elements_forcss(jumalocator.all_ivuselectdropdowntransfer_css)
        ele = self.find_element(showlist_locator)
        ele.click();
        self.input_text_new(showlist_locator, text)
        self.wait_element_not_present(jumalocator.auto_list_active)
        e = self.find_element(
            jumalocator.current_ivuselectdropdowntransfer + "/ul/li[normalize-space(text())='" + text + "']")
        if "ivu-select-item-selected" not in e.get_attribute("class"):
            locator2 = jumalocator.current_ivuselectdropdowntransfer + "/ul/li[normalize-space(text())='" + text + "']"
            self.scroll_to_element_clickable(locator2,
                                             ".ivu-select-dropdown.ivu-select-dropdown-transfer:not([style*='display: none'])")
            self.click_element_new(locator2)
        #             e.click()
        self.hide_elements_forcss(jumalocator.all_ivuselectdropdowntransfer_css)

    @keyword
    def select_date(self, showlist_locator, datestr):
        self.hide_elements_forcss(jumalocator.date_picker_css)
        self.wait_page_loaded()
        self.click_until_element_visible(showlist_locator, jumalocator.loc_date_picker)
        ls = datestr.split("-")
        year = int(ls[0])
        month = int(ls[1])
        day = int(ls[2])
        c_year = self.get_num_from_string(self.get_text_new(jumalocator.select_year))
        c_month = self.get_num_from_string(self.get_text_new(jumalocator.select_month))
        if year == c_year and month == c_month:
            pass
        else:
            self.click_element_new(jumalocator.select_year)
            tmp_first_year = int(self.get_text_new(jumalocator.year_first_cell))
            tmp_last_year = int(self.get_element_attribute_new(jumalocator.year_last_cell, "innerText"))
            while year < tmp_first_year:
                self.click_element_new(jumalocator.prev_btn_arrow_double)
                tmp_first_year = int(self.get_text_new(jumalocator.year_first_cell))
            while year > tmp_last_year:
                self.click_element_new(jumalocator.next_btn_arrow_double)
                tmp_last_year = int(self.get_element_attribute_new(jumalocator.year_last_cell, "innerText"))
            self.click_element_new(jumalocator.year_to_select_cell + str(year) + "']")
            self.click_element_new(jumalocator.month_to_select_cell + str(month) + "]")
        self.click_element_new(jumalocator.day_to_select_cell + str(day) + "']]")

    @keyword
    def upload_attach(self, filepath):
        ph = pathlib.Path(filepath)
        if ph.exists() == False:
            raise FileNotFoundError
        if ph.is_file() == False:
            raise FileNotFoundError
        self.click_button_new(jumalocator.select_attachfile_btn)
        sleep(2)
        self.windows_loadfile(filepath)
        self.wait_attach_uploaded()

    @keyword
    def common_upload_attach(self, locator_showupload, filepath):
        self.click_element_new(locator_showupload)
        self.upload_attach(filepath)
        self.click_element_new(jumalocator.loc_file_attach_upload_save)
        self.wait_modal_invisible_for_title("上传附件")

    @keyword
    def wait_attach_uploaded(self):
        timeout = timestr_to_secs(self.selib.get_selenium_timeout())
        WebDriverWait(self.driver, int(timeout), 1).until(lambda x: self.is_attach_uploaded())

    @keyword
    def is_attach_uploaded(self):
        es = self.get_webelements_new(jumalocator.loc_attach_files_status)
        for e in es:
            ls = e.text.split("/")
            if ls[0] != ls[1]:
                return False
        return True

    @keyword
    def select_tabs_bar(self, text):
        self.click_element_new(jumalocator.locator_tabs_tab_1 + text + jumalocator.locator_tabs_tab_2)
        self.wait_table_loaded()

    @keyword
    def common_first_row_operate(self, is_table_btn_left=False, more_operate=None):
        if is_table_btn_left == True:
            self.click_element_new(jumalocator.first_row_operate_left)
        elif more_operate == None:
            self.click_element_new(jumalocator.first_row_operate_right)
        else:
            self.dropdown_transfer_menu(jumalocator.first_row_operate_right, more_operate)

    @keyword
    def wait_modal_invisible(self):
        self.selib.element_should_be_visible(jumalocator.loc_current_modal_warp)
        self.selib.wait_until_element_is_not_visible(jumalocator.loc_current_modal_warp)

    @keyword
    def wait_modal_invisible_for_title(self, title):
        self.selib.element_should_be_visible(jumalocator.loc_current_modal_warp_xpath + title + "']]")
        self.selib.wait_until_element_is_not_visible(jumalocator.loc_current_modal_warp_xpath + title + "']]")

    #     @keyword
    #     def wait_modal_not_present(self):
    #         self.wait_element_not_present(jumalocator.loc_current_modal_warp)
    #     @keyword
    #     def wait_modal_not_present_for_title(self,title):
    #         self.wait_element_not_present(jumalocator.loc_current_modal_warp_xpath+title+"']]")
    @keyword
    def select_many_checkbox(self, *selectindex):
        if len(selectindex) == 0:
            return
        ele = self.find_element(jumalocator.loc_checkbox_group)
        es = self.wait_elements_visible_from_element(ele, jumalocator.loc_checkbox)
        i = 0
        while i < len(es):
            if "ivu-checkbox-wrapper-checked" in es[i].get_attribute("class"):
                if str(i + 1) in selectindex or (i + 1) in selectindex:
                    pass
                else:
                    es[i].click()
            else:
                if str(i + 1) in selectindex or (i + 1) in selectindex:
                    es[i].click()
            i = i + 1

    @keyword
    def get_many_checkbox_selected(self):
        ele = self.find_element(jumalocator.loc_checkbox_group)
        es = self.wait_elements_visible_from_element(ele, jumalocator.loc_checkbox)
        ls = []
        i = 0
        while i < len(es):
            if "ivu-checkbox-wrapper-checked" in es[i].get_attribute("class"):
                ls.append(str(i + 1))
            i = i + 1
        return ls

    @keyword
    def check_msg(self, expect_msg):
        msg = self.get_message_info()
        self.builtin.should_contain(msg, expect_msg)

    @keyword
    def select_cascader_transfer(self, show_locator, string):
        """选择class类型为ivu-cascader-transfer的选择框
        """
        ls = string.split(",")
        self.hide_elements_forcss(jumalocator.all_cascader_transfer_css)
        self.click_element_new(show_locator)
        self.wait_element_have_attribute_value(jumalocator.loc_current_cascader_transfer, "class",
                                               jumalocator.slide_up_active)
        self.wait_element_have_not_attribute_value(jumalocator.loc_current_cascader_transfer, "class",
                                                   jumalocator.slide_up_active)
        ele = self.find_element(jumalocator.loc_cascader_transfer)
        index = 0
        for s in ls:
            self.find_element_from_parent(ele,
                                          jumalocator.loc_cascader_transfer2 + s + jumalocator.loc_cascader_transfer3).click()
            index += 1
            if index < len(ls):
                ele = self.find_element_from_parent(ele, jumalocator.loc_cascader_transfer4)
        self.hide_elements_forcss(jumalocator.all_cascader_transfer_css)

    @keyword
    def wait_modal_loaded(self):
        #         self.wait_element_present(jumalocator.loc_current_modal_mask_xpath)
        #         self.wait_element_not_present(jumalocator.loc_current_modal_mask_xpath)
        self.wait_element_have_attribute_value(jumalocator.loc_current_modal_mask, "class", "fade-enter-active")
        self.wait_element_have_not_attribute_value(jumalocator.loc_current_modal_mask, "class", "fade-enter-active")

    @keyword
    def wait_modal_loaded_for_text(self, title):
        self.wait_element_have_attribute_value(jumalocator.loc_current_modal_mask_text_path + title + "']]", "class",
                                               "fade-enter-active")
        self.wait_element_have_not_attribute_value(jumalocator.loc_current_modal_mask_text_path + title + "']]",
                                                   "class", "fade-enter-active")

    @keyword
    def table_resultnum_should_be(self, resultnum):
        self.builtin.should_be_equal(self.get_table_result_count(), int(resultnum))

    @keyword
    def table_result_should_be_empty(self, timeout=2):
        self.builtin.should_be_true(self.is_table_result_empty(int(timeout)))

    @keyword
    def table_result_should_not_be_empty(self, timeout=2):
        self.builtin.should_not_be_true(self.is_table_result_empty(int(timeout)))

    @keyword
    def common_spread(self):
        spread_btn = self.find_element(jumalocator.loc_spread_btn)
        if "arrow-open" in self.find_element_from_parent(spread_btn, 'xpath=.//span/i').get_attribute("class"):
            spread_btn.click()

    @keyword
    def click_modal_btn_by_text(self, text):
        es = self.find_elements(jumalocator.loc_current_modal_warp)
        index = 0
        ls = []
        maxsize = 0
        maxindex = 0
        while (index < len(es)):
            jstext = "var e = document.querySelectorAll('.ivu-modal-wrap:not(.ivu-modal-hidden)')[" + str(
                index) + "];var a = window.getComputedStyle(e).zIndex;return a;"
            size = int(self.driver.execute_script(jstext))
            ls.append(size)
            if maxsize <= size:
                maxsize = size
                maxindex = index
            index += 1
        self.find_element_from_parent(es[maxindex], jumalocator.loc_modal_button_find + text + "')]]").click()

    @keyword
    def click_modal_body_btn_by_text(self, text):
        es = self.find_elements(jumalocator.loc_current_modal_warp)
        index = 0
        ls = []
        maxsize = 0
        maxindex = 0
        while (index < len(es)):
            jstext = "var e = document.querySelectorAll('.ivu-modal-wrap:not(.ivu-modal-hidden)')[" + str(
                index) + "];var a = window.getComputedStyle(e).zIndex;return a;"
            size = int(self.driver.execute_script(jstext))
            ls.append(size)
            if maxsize <= size:
                maxsize = size
                maxindex = index
            index += 1
        self.find_element_from_parent(es[maxindex], jumalocator.loc_modal_body_button_find + text + "')]]").click()

    @keyword
    def export(self, is_confirm_alert=False, confirm_btn_text='确定', is_select_fields=False, select_fields=None,
               select_fields_confirm_btn_text='确定'):
        """导出
        :param is_confirm_alert: 是否有确认弹窗
        :param confirm_btn_text: 确认导出按钮的文本显示
        :param is_select_fields: 是否选择导出字段
        :param select_fields: 导出字段，以逗号分隔
        :param select_fields_confirm_btn_text: 确认导出字段的按钮的文本显示
        """
        self.click_element_new(jumalocator.loc_export)
        self.wait_page_loaded()
        if is_select_fields == True:
            es = self.find_elements(jumalocator.loc_select_export_fields)
            if select_fields != None and select_fields.strip():
                sflist = select_fields.split(",")
                for e in es:
                    if e.get_attribute("title") in sflist:
                        if "ivu-icon-android-checkbox-outline-blank" in self.find_element_from_parent(e,
                                                                                                      "xpath=.//i").get_attribute(
                                "class"):
                            e.click()
                        else:
                            pass
                    else:
                        if "ivu-icon-android-checkbox-outline-blank" not in self.find_element_from_parent(e,
                                                                                                          "xpath=.//i").get_attribute(
                                "class"):
                            e.click()
            self.click_modal_btn_by_text(select_fields_confirm_btn_text)
        if is_confirm_alert == True:
            self.click_modal_btn_by_text(confirm_btn_text)

    @keyword
    def treemenu_right_click_and_select(self, treemenu, text):
        treemenulist = treemenu.split(",")
        locator = jumalocator.loc_treeWithContextMenu_div
        tmpstr = "/ul/li"
        index = 1
        for menustr in treemenulist:
            locator += tmpstr
            locat_laststr = locator + "[@data-title='" + menustr + "']"
            if index < len(treemenulist):
                if 'c-treeview-fold-open' not in self.find_element(locat_laststr + "/a/i").get_attribute("class"):
                    self.click_element_new(locat_laststr + "/a/i")
            else:
                action = ActionChains(self.driver)
                ele = self.find_element(locat_laststr)
                action.move_to_element(ele).perform()
                action.context_click(ele).perform()
                self.click_button_new(jumalocator.loc_c_pop_menu_btn + str(text) + jumalocator.loc_c_pop_menu_btn2)
            index += 1

    @keyword
    def editableTable_add(self, add_locator, type, items):
        if int(type) == 1:
            if not (isinstance(items, list)):
                raise Exception("type=1时,参数itemlist需要传入list")
            else:
                for item in items:
                    if not (isinstance(item, dict)):
                        raise Exception("参数itemlist中元素必须是dict类型数据")
                index = 1
                self.click_button_new(add_locator)
                for item in items:
                    for i in item:
                        self.input_text_new(jumalocator.loc_editableTable_item_input + str(
                            index) + jumalocator.loc_editableTable_item_input2 + str(
                            i) + jumalocator.loc_editableTable_item_input3, item[i])
                    self.click_button_new(
                        jumalocator.loc_editableTable_item_input + str(index) + jumalocator.loc_editableTable_item_save)
                    self.wait_spin_loaded()
                    index += 1
        elif int(type) == 2:
            if not (isinstance(items, dict)):
                raise Exception("type=2时参数itemlist需要传入dict")
            else:
                for item in items:
                    if not (isinstance(items[item], dict)):
                        raise Exception("参数itemlist中元素必须是dict类型数据")
                self.click_button_new(add_locator)
                for item in items:
                    for i in items[item]:
                        self.input_text_new(jumalocator.loc_editableTable_item_input + str(
                            item) + jumalocator.loc_editableTable_item_input2 + str(
                            i) + jumalocator.loc_editableTable_item_input3, items[item][i])
                    self.click_button_new(
                        jumalocator.loc_editableTable_item_input + str(item) + jumalocator.loc_editableTable_item_save)
                    self.wait_spin_loaded()

    @keyword
    def click_filter_group_by_text(self, text):
        if self.find_elements(jumalocator.status_search_text2) and len(text) != 0:
            if self.is_element_present(jumalocator.status_search_text, 1):
                if text not in self.get_text_new(jumalocator.status_search_text, 1):
                    self.click_element_new(jumalocator.status_search + text + jumalocator.status_search_loctail)
            else:
                self.click_element_new(jumalocator.status_search + text + jumalocator.status_search_loctail)
