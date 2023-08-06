from setuptools import setup,find_packages

setup(
    name='kvvmail',
    version='0.0.1',
    description='simplified code of sending mail',
    Long_description=open('README.md').read()+'\n\n'+open('CHANGELOG.txt').read(),
    url='',
    author='krupal vora',
    author_email='krupal.vora@sakec.ac.in',
    License='MIT',
    classifiers=[
    'Intended Audience :: Education',
    'License :: OSI Approved :: MIT License',
    ],
    keywords='kvvmail',
    packages=['kvvmail'],
    install_requires=['smtplib']
)