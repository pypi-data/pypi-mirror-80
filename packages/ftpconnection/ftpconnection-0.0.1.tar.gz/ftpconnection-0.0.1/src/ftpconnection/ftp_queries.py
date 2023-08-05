from ftpconnection import logger
from dateutil import parser
from datetime import datetime
import datetime
from io import BytesIO

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
CURRENT_TIME = datetime.datetime.strptime(datetime.datetime.utcnow().strftime(DATE_TIME_FORMAT), DATE_TIME_FORMAT)


def get_file_type(file_permission_string):
    if 'd' in file_permission_string:
        return 'directory'
    return 'file'


def get_file_datetime(file_modify_time):
    last_modified = str(parser.parse(file_modify_time))
    file_datetime = datetime.datetime.strptime(last_modified, DATE_TIME_FORMAT)
    return file_datetime


def get_file_metadata(file_info):
    meta_data = file_info.split(maxsplit=9)
    file_type = get_file_type(meta_data[0])
    file_size = int(int(meta_data[4]) / 1024)
    file_name = meta_data[8]
    file_modify_time = meta_data[5] + " " + meta_data[6] + " " + meta_data[7]
    file_datetime = get_file_datetime(file_modify_time)
    return [file_name, file_type, file_size, file_datetime]


def get_required_files(ftp, after_time, before_time, file_types={'file', 'directory'}):
    files_temp_info = []
    files_info = []
    ftp.connection.dir('.', files_temp_info.append)
    for current_file_info in files_temp_info:
        meta_data = get_file_metadata(current_file_info)
        if meta_data[1] in file_types and after_time <= meta_data[3] <= before_time:
            files_info.append(meta_data)

    files_info.sort(key=lambda i: i[3])

    for f in files_info:
        logger.info(f'{f}')

    return files_info


def remove_required_files(ftp, after_time, before_time, file_types={'file', 'directory'}, exclude_files={}):
    files_temp_info = []
    ftp.connection.dir('.', files_temp_info.append)
    for current_file_info in files_temp_info:
        meta_data = get_file_metadata(current_file_info)
        file_name = meta_data[0]
        file_type = meta_data[1]

        if file_type in file_types and after_time <= meta_data[3] <= before_time and file_name not in exclude_files:
            logger.info(f'Removing {meta_data}')
            if file_type == 'file':
                ftp.connection.delete(file_name)
            if file_type == 'directory':
                files = list(ftp.connection.nlst(file_name))
                for f in files:
                    ftp.connection.delete(f)
                ftp.connection.rmd(file_name)


def upload_file(ftp, file_name: str, file_content: str):
    binary_content = BytesIO(bytearray(file_content, encoding='utf-8'))
    ftp.connection.storbinary(f'STOR {file_name}', binary_content)
