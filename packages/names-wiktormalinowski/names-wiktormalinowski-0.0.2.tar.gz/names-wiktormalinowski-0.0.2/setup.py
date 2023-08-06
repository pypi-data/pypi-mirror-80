from setuptools import find_packages, setup

setup(
    name='names-wiktormalinowski',
    version='0.0.2',
    author='Wiktor Malinowski',
    author_email='abc@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    description='Super useful library',
    scripts = ['bin/get_name_wiktormalinowski.py', 'bin/get_name_wiktormalinowski.bat'],
    install_requires=['names']
)
