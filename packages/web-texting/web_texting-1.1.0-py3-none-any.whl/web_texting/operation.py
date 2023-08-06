import logging
from time import sleep

from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)


# 选取控件
def element(category, selector):
    if category in (By.ID, By.XPATH, By.LINK_TEXT, By.PARTIAL_LINK_TEXT, By.NAME, By.TAG_NAME, By.CLASS_NAME,
                    By.CSS_SELECTOR):

        elem = (category, selector)
        return elem
    else:
        return None


class Operation:

    # 构造函数
    def __init__(self, browser):
        self.browser = browser

    def get_driver(self):
        return self.browser

    # 元素定位 3.0 :基于str来生成元素定位
    def locator(self, loc):
        return self.browser.find_element(*loc)

    # 元素的输入
    def input(self, loc, txt):
        self.locator(loc).send_keys(txt)

    def select(self, loc, target):
        self.locator(loc).click()
        sleep(1)
        self.locator(target).click()

    # 元素的点击
    def click(self, loc):
        self.locator(loc).click()

    def text(self, loc):
        return self.locator(loc).text

    # 访问指定URL
    def visit(self, url):
        self.browser.get(url)

    # 关闭浏览器 ，释放资源
    def close(self):
        wait = 3
        logger.debug('will close the browser after {} seconds'.format(wait))
        sleep(wait)
        self.browser.quit()

    # 页面最大化
    def max_window(self):
        self.browser.maximize_window()

    def snapshot(self, filename):
        self.browser.save_screenshot(filename)
