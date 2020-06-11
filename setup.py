from setuptools import (
    find_packages,
    setup,
)

setup(
    name='django-paybox-api',
    version='0.0.1',
    author='Aiba',
    description='Django paybox api',
    url='https://github.com/aibaq/django-paybox-api',
    packages=find_packages(exclude=('*tests*',)),
    install_requires=[
        'django>=1.11',
        'requests>=2.14',
    ],
)
