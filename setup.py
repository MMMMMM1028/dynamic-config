# coding=utf-8
from setuptools import setup
import sys
from dynamic_config import __version__


# 根据 Python 版本动态调整依赖
def get_install_requires():
    requires = []

    # Redis 客户端依赖（Python 2.7 兼容版本）
    if sys.version_info < (3, 0):
        requires.append('redis==3.5.3')  # Python 2.7 最后一个兼容版本
        requires.append('redis-py-cluster==2.1.3')  # 兼容 Python 2.7
        requires.append('gevent==1.4.0')  # Python 2.7 最高兼容版本
    else:
        requires.append('redis>=4.5.5')
        requires.append('redis-py-cluster>=2.1.3')
        requires.append('gevent>=23.3.1') if sys.version_info >= (3, 7) else requires.append('gevent>=21.12.0')

    return requires


setup(
    name='dynamic-config',
    version=__version__,
    description='基于Redis Cluster的动态配置管理系统，采用主动拉取(Pull)+推送(Push)双模式更新策略，内置LRU本地缓存。',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='wzc',
    author_email='wzc@xxx.com',
    url='https://github.com/yourusername/your-repo',
    packages=['dynamic_config'],
    python_requires='==2.7',
    install_requires=get_install_requires(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='redis, gevent, dynamic_config, pubsub, cluster',
)