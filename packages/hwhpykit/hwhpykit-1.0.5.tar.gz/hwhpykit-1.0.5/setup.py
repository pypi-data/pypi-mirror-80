import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='hwhpykit',  # 包名字
    version='1.0.5',  # 包版本
    description='My toolbox',  # 简单描述
    author='louishwh',  # 作者
    author_email='louishwh@gmail.com',  # 作者邮箱
    url='',  # 包的主页
    #packages=['hwhpykit.cache']
    packages=setuptools.find_packages(),
    python_requires='>=3.6',

    long_description=long_description,
    long_description_content_type="text/markdown",
)

install_requires=[
    'redis>=3.5.3'
    'pymysql>=0.10.0'
]