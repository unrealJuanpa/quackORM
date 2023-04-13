from setuptools import setup

setup(
    name='quackORM',
    version='0.1',
    description='An ORM that supports mysql and sounds like a duck :D',
    url='https://github.com/unrealJuanpa/quackORM.git',
    author='unrealJuanpa',
    author_email='juanpacloud@gmail.com',
    license='MIT',
    packages=['quackORM'],
    install_requires=[
        'mysql.connector'
    ],
    zip_safe=False,
)
