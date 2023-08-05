from setuptools import setup

setup(
    name='mail_monitor',
    version='0.5',
    packages=['mail_monitor'],
    url='https://github.com/OpenJarbas/mail_monitor',
    license='Apache',
    author='jarbasAI',
    install_requires=["html2text"],
    author_email='jarbasai@mailfence.com',
    description='simple util to monitor new emails'
)
