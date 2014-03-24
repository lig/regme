import codecs

from setuptools import setup


with codecs.open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='regme',
    version='0.1.1',
    description='User registration and management library using MongoEngine',
    long_description=long_description,
    url='https://github.com/lig/regme',
    author='Serge Matveenko',
    author_email='s@matveenko.ru',
    license='Apache',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Topic :: Database',
        'Framework :: Django',
    ],
    keywords='mongodb mongoengine django registration authentication',
    packages=['regme'],
    install_requires=[
        'django',
        'mongoengine',
        'blinker',
    ],
)
