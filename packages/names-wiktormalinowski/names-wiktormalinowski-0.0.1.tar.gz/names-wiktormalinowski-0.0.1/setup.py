from setuptools import find_packages, setup

setup(
    name='names-wiktormalinowski',
    version='0.0.1',
    author='Wiktor Malinowski',
    author_email='abc@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    description='Super useful library',
    install_requires=['names']
)
