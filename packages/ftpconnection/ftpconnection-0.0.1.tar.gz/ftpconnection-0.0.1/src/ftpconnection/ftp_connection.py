from ftpconnection import logger
from ftplib import FTP
import os


class FtpConnection:
    def __init__(self):
        logger.debug('Initiating FTP Connection Class')
        self._connection_parameter = None
        self._connection = None

    def set_connection_parameter(self, **kwargs):
        self._connection_parameter = {
            "user": os.environ.get('FTP_USER') if not kwargs.get('user') else kwargs.get('user'),
            "password": os.environ.get('FTP_PASSWORD') if not kwargs.get('password') else kwargs.get('password'),
            "host": os.environ.get('FTP_HOST') if not kwargs.get('host') else kwargs.get('host'),
            "port": os.environ.get('FTP_PORT') if not kwargs.get('port') else kwargs.get('port'),
            "dir": os.environ.get('FTP_DIR') if not kwargs.get('dir') else kwargs.get('dir')
        }

    @property
    def connection(self):
        if self._connection is None:
            self.set_connection()
        if not self.validate_connection():
            self.set_connection()
        return self._connection

    def set_connection(self):
        if self._connection_parameter is None:
            self.set_connection_parameter()

        logger.debug('Creating FTP connection')
        conn = FTP(
            user=self._connection_parameter['user'],
            passwd=self._connection_parameter['password'],
            host=self._connection_parameter['host'])

        self._connection = conn
        self._connection.encoding = "utf-8"

        try:
            self._connection.cwd(self._connection_parameter['dir'])
            logger.info('FTP Connection Object Created. Connection={}'.format(str(self._connection)))
        except Exception as ce:
            logger.error('Error in making FTP connection with host={}, port={}'.format(
                self._connection_parameter['host'], self._connection_parameter['port']), exc_info=True)
            raise Exception("Connection Error with FTP connection={}".format(str(self._connection)))

    def close_connection(self):
        if self._connection is not None:
            self._connection = None

    def validate_connection(self):
        try:
            self._connection.voidcmd("NOOP")
            return True
        except Exception as e:
            logger.warning(f'{e}')
        return False
