from setuptools import setup

setup(
    # 以下为必需参数
    name='web_texting',  # 模块名
    version='1.1.0',  # 当前版本
    description='A Web test module',  # 简短描述
    packages=['web_texting'],
    py_modules=[],  # 单文件模块写法
    # ckages=find_packages(exclude=['contrib', 'docs', 'tests']),  # 多文件模块写法

    # 以下均为可选参数
    url='https://github.com/lishimeng/web_texting',  # 主页链接
    author='li shimeng',  # 作者名
    author_email='316527907@qq.com',  # 作者邮箱
    install_requires=['selenium', 'bottle'],  # 依赖模块
    project_urls={  # 项目相关的额外链接
        'Source': 'https://github.com/lishimeng/web_texting',
    },
)
