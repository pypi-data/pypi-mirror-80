from selenium.common.exceptions import StaleElementReferenceException, \
    WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException


class visibility_of_all_elements(object):
    """ An expectation for checking that all elements are present on the DOM of a
    page and visible. Visibility means that the elements are not only displayed
    but also has a height and width that is greater than 0.
    locator - used to find the elements
    returns the list of WebElements once they are located and visible
    """

    def __init__(self, es):
        self.es = es

    def __call__(self, ignored):
        for element in self.es:
            if not EC._element_if_visible(element):
                return False
        return self.es


class element_should_have_attribute_value(object):
    def __init__(self, element, attributename, value):
        self.element = element
        self.attributename = attributename
        self.value = value

    def __call__(self, ignored):
        if self.value in self.element.get_attribute(self.attributename):
            return True
        else:
            return False


class element_not_be_covered_and_click(object):
    def __init__(self, driver, element):
        self.driver = driver
        self.element = element

    def __call__(self, ignored):
        try:
            action = ActionChains(self.driver)
            action.move_to_element(self.element).perform()
            self.element.click()
            return True
        except WebDriverException as e:
            if "Other element would receive the click" in repr(e):
                return False
            else:
                raise e


class presence_of_element_located(object):
    """ An expectation for checking that an element is present on the DOM
    of a page. This does not necessarily mean that the element is visible.
    locator - used to find the element
    returns the WebElement once it is located
    """

    def __init__(self, element, by, value):
        self.element = element
        self.by = by
        self.value = value

    def __call__(self, ignored):
        return _find_element(self.element, self.by, self.value)


def getBy(Byname):
    m = {
        "CSS": By.CSS_SELECTOR,
        "ID": By.ID,
        "LINK": By.LINK_TEXT,
        "NAME": By.NAME,
        "PARTIAL LINK": By.PARTIAL_LINK_TEXT,
        "TAG": By.TAG_NAME,
        "XPATH": By.XPATH
    }
    key = m.get(Byname)
    return key


def _find_element(element, by=By.ID, value=None):
    """Looks up an element. Logs and re-raises ``WebDriverException``
    if thrown."""
    try:
        return element.find_element(by, value)
    except NoSuchElementException as e:
        raise e
    except WebDriverException as e:
        raise e

