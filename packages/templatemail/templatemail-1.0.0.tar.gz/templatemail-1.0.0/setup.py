from setuptools import setup, Extension
from os import path

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='templatemail',
    version='1.0.0',
    packages=['templatemail', 'templatemail.engines'],
    package_data={'templatemail': ['templates/*.html', 'templates/mailgun-transactional/*.html']},
    url='https://github.com/kkinder/templatemail',
    license='Apache 2.0',
    author='Ken Kinder',
    author_email='ken@kkinder.com',
    description='Templated Email for Python',
    python_requires='>=3.6',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'requests',
        'Jinja2'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Communications :: Email',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
