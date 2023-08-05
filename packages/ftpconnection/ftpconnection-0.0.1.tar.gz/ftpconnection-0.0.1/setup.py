from setuptools import setup

setup(
    name='ftpconnection',
    packages=['ftpconnection'],
    package_dir={'ftpconnection': 'src/ftpconnection'},
    version='0.0.1',
    license='MIT',
    platforms='cross-platfom, platform-independent',
    description='FTP Connections and Queries Handler',
    author='Yogesh Yadav',
    author_email='yogeshdtu@gmail.com',
    url='https://github.com/ByPrice/ftpconnection',
    download_url='https://github.com/ByPrice/ftpconnection',
    keywords=['ftp', 'ftpconnection', 'ftpqueries'],
    install_requires=[
       'python-dotenv>=0.10.3', 'python-dateutil >=2.8.1'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: File Transfer Protocol (FTP)',
        'Programming Language :: Python :: 3.6',
    ],
)
