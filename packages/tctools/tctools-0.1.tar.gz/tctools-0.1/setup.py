from setuptools import setup, find_packages

setup(
    name='tctools',
    version='0.1',
    packages=find_packages(),
    package_data={
        'tctools':['README.md']
    },
    install_requires=['pymysql','pika','redis==2.10.6','redis-py-cluster==1.3.6'],
    author = 'chengxz,xiaxx',
    author_email='chengxz@jiguang.cn,xiaxx@jiguang.cn',
    url='http://www.jiguang.cn',
)