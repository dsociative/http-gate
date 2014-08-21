from setuptools import setup, find_packages


setup(
    name='http_gate',
    version='',
    packages=find_packages(),
    url='',
    license='',
    author='dsociative',
    author_email='admin@geektech.ru',
    description='',
    install_requires=[
        'tornado',
        'pytest',
        'pyzmq'
    ],
    entry_points={
        'console_scripts': [
            'http_gate = http_gate.app:main',
        ]
    }
)
