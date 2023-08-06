from robot.libraries.BuiltIn import BuiltIn


class initlib(object):
    @property
    def builtin(self):
        return BuiltIn()

    @property
    def se2lib(self):
        return self.selib

    @property
    def selib(self):
        return self.builtin.get_library_instance("SeleniumLibrary")

    def getselib(self):
        return self.selib

    @property
    def browser(self):
        return self.driver

    @property
    def driver(self):
        '''Return the currently active driver instance

        This is a proxy to the "driver" property of SeleniumLibrary
        '''
        if hasattr(self.selib, "driver"):
            return self.selib.driver
        elif hasattr(self.selib, "_current_browser"):
            return self.selib._current_browser()
        else:
            raise Exception("unable to find 'driver' or '_current browser' attribute of SeleniumLibrary")
