from setuptools import find_packages,setup

setup(
    name='packagepg',
    version='1.0',
    author='pg',
    author_email='',
    packages=find_packages(),
    include_package_data=True,
    description='len of random name',
    install_requires=['names']
)
