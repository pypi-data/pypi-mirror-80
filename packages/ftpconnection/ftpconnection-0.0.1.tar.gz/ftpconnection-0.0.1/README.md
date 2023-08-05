FTP Adapter for Connection and Query Handling


## System Dependency

* Python 3.6.8
* pipenv


## Development Setup

1) Clone the repo 
2) cd ftpconnection
3) pipenv install
4) pipenv shell

Start developing

# Package ftpconnection
python version must be 3.6.8
### Build
python setup.py build

### Distribute
python setup.py sdist

### Dependency

### Use 
It wil load environment variable automatically, so all you need to do is make sure these environment variables are present. 
It will also autoload .env ( example .env.dist , rename it to .env) file before running, so you can also put these variables in your .env file. 

Needed Environment variables are 

```
# FTP
FTP_HOST=******
FTP_PORT=****
FTP_USER=***********
FTP_PASSWORD=*****@
FTP_DIR=~

```

```
from ftpconnection import FTPConnection 

ftp = FTPConnection()
connection = ftp.connection

When all done , please do ftp.close_connection()

```




