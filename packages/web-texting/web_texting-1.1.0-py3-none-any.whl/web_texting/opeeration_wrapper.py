import logging
import time

from .operation import Operation, element

logger = logging.getLogger(__name__)


class OperationWrapper(Operation):

    def __init__(self, browser):
        super().__init__(browser)
        logger.debug("open browser")

    # 跳转页面
    def move_to(self, url):
        logger.debug('move to url:{}'.format(url))
        super().visit(url)

    # 选取list
    def change_select(self, category, list_selector, options_selector):
        logger.debug('change select:[{}]{}:{}'.format(category, list_selector, options_selector))
        elem = element(category, list_selector)
        self.click(elem)
        time.sleep(1)
        elem = element(category, options_selector)
        self.click(elem)

    # 输入框
    def text_input(self, category, selector, val):
        logger.debug('input value:[{}]{}:{}'.format(category, selector, val))
        elem = element(category, selector)
        super().input(elem, val)

    # 点击按钮
    def clc_btn(self, category, selector):
        logger.debug('click button:[{}]{}'.format(category, selector))
        elem = element(category, selector)
        super().click(elem)

    def get_text(self, category, selector):
        logger.debug('get text:[{}]{}'.format(category, selector))
        elem = element(category, selector)
        return super().text(elem)

    def finger_move(self, from_point, to_point):
        print(self)
        logger.debug("move from {} to {}".format(from_point, to_point))

    def finger_touch(self, x, y):
        print(self)
        logger.debug('touch {}:{}'.format(x, y))
