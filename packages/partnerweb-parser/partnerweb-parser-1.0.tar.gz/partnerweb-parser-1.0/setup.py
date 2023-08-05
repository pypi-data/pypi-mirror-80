from distutils.core import setup

setup(
    name='partnerweb-parser',
    packages=['partnerweb-parser'],
    version='1.0',
    license='MIT',
    description='Partnerweb beeline parser',
    author='chanterelly',
    author_email='partnerweb3@gmail.com',
    url='https://github.com/ChanTerelLy/partnerweb-parser',
    download_url='https://github.com/ChanTerelLy/partnerweb-parser/archive/1.0.tar.gz',
    keywords=['partnerweb', 'beeline'],
    install_requires=[
        'aiohttp',
        'pytz',
        'requests',
        'beautifulsoup4',
        'gevent',
        'grequests',
        'lxml',
        'openpyxl',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
)
