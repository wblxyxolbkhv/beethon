from setuptools import setup, find_packages     # type: ignore
from os import path

base_dir = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(base_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='beethon',
    version='0.0.1',
    description='A simple async python-based microservice framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/wblxyxolbkhv/beethon',
    author='Alexey Nikitenko (wblxyxolbkhv)',
    author_email='alexey.nikitenko1927@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='microservice amqp http',
    package_dir={'': 'beethon'},
    packages=find_packages(where='beethon'),
    python_requires='>=3.5, <4',
    install_requires=[
        'aio-pika==6.6.0',
        'aiormq==3.2.1',
        'idna==2.9',
        'multidict==4.7.5',
        'pamqp==2.3.0',
        'yarl==1.4.2',
    ],
    project_urls={
        'Bug Reports': 'https://github.com/wblxyxolbkhv/beethon/issues',
        'Source': 'https://github.com/wblxyxolbkhv/beethon',
    },
)
