from selenium.webdriver.common.by import By


class JobConfig(object):
    Id = 'id'
    Name = 'name'
    Steps = 'steps'


class StepConfig(object):
    Id = 'id'
    Name = 'name'
    Operator = 'operator'


class OperatorConfig(object):
    Category = 'category'
    Config = 'operatorConfig'


# 选择器类型，这个不会再添加新的了
class SelectorCategory(By):
    _version = 1
