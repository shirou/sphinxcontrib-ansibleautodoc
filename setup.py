# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


requires = ['Sphinx>=1.4', 'setuptools']

setup(
    name='sphinxcontrib_ansibleautodoc',
    version='0.0.4',
    url='http://github.com/shirou/sphinxcontrib-ansibleautodoc',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-ansibleautodoc',
    license='BSD',
    author='WAKAYAMA Shirou',
    author_email='shirou.faw@gmail.com',
    description='autodoc for ansible playbook',
    long_description=open("README.rst").read(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
