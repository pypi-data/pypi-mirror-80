from .opeeration_wrapper import OperationWrapper


def assert_message(expect, actual):
    return 'expect [{}], but [{}]'.format(expect, actual)


class OperationExecutor:

    def __init__(self, browser):
        self.ow = OperationWrapper(browser)
        self.cur_step = None

    def update_step(self, step):
        self.cur_step = step

    def visit(self, operation_config):
        url = operation_config['url']
        self.ow.visit(url)

    def input(self, operation_config):
        selector_category = operation_config['selectorCategory']
        selector = operation_config['selector']
        value = operation_config['value']
        self.ow.text_input(selector_category, selector, value)

    def click(self, operation_config):
        selector_category = operation_config['selectorCategory']
        selector = operation_config['selector']
        self.ow.clc_btn(selector_category, selector)

    def select(self, operation_config):
        selector_category = operation_config['selectorCategory']
        selector = operation_config['selector']
        option_selector = operation_config['optionSelector']
        self.ow.change_select(selector_category, selector, option_selector)

    def snapshot(self, operation_config):
        name = None
        if operation_config is not None and hasattr(operation_config, 'name'):
            name = operation_config['name']
        if name is None:
            name = '{}.png'.format(self.cur_step["id"])
        self.ow.snapshot(name)

    def close(self):
        self.ow.close()

    def assert_url(self, operation_config):
        expect = operation_config['url']
        actual = self.ow.browser.current_url
        assert expect == actual, assert_message(expect, actual)

    def assert_title(self, operation_config):
        expect = operation_config['title']
        actual = self.ow.browser.title
        assert expect == actual, assert_message(expect, actual)

    def assert_text(self, operation_config):
        selector_category = operation_config['selectorCategory']
        selector = operation_config['selector']
        expect = operation_config['text']
        actual = self.ow.get_text(selector_category, selector)
        assert expect == actual, assert_message(expect, actual)
