import os
import sys

from setuptools import setup, find_packages

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    print("Now tag me :)")
    print("  git tag -a {0} -m 'version {0}'".format(__import__('pynamodb').__version__))
    print("  git push --tags")
    sys.exit()

install_requires = [
    'six',
    'botocore>=1.2.0',
    'python-dateutil>=2.1,<3.0.0',
]

setup(
    name='pynamodb-dax',
    version=__import__('pynamodb').__version__,
    packages=find_packages(),
    url='https://github.com/thanakijwanavit/PynamoDB',
    author='Nic Wanavit (fork)',
    author_email='nwanavit@gmail.com',
    description='fork to pynamodb for supporting dax',
    long_description=open('README.rst').read(),
    zip_safe=False,
    license='MIT',
    keywords='python dynamodb amazon dax',
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
    ],
    extras_require={
        'signals': ['blinker>=1.3,<2.0']
    },
)
