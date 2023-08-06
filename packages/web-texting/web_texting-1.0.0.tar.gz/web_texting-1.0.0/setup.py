from setuptools import setup

setup(
    # 以下为必需参数
    name='web_texting',  # 模块名
    version='1.0.0',  # 当前版本
    description='A Web test module',  # 简短描述
    py_modules=["web_texting"],  # 单文件模块写法
    # ckages=find_packages(exclude=['contrib', 'docs', 'tests']),  # 多文件模块写法


    # 以下均为可选参数
    long_description="A Web test module",  # 长描述
    url='https://github.com/lishimeng/web_texting',  # 主页链接
    author='li shimeng',  # 作者名
    author_email='316527907@qq.com',  # 作者邮箱
    install_requires=['selenium', 'bottle'],  # 依赖模块
    extras_require={  # 分组依赖模块，可使用pip install sampleproject[dev] 安装分组内的依赖
    },
    package_data={  # 模块所需的额外文件
    },
    entry_points={  # 新建终端命令并链接到模块函数
    },
    project_urls={  # 项目相关的额外链接
        'Source': 'https://github.com/lishimeng/web_texting',
    },
)
