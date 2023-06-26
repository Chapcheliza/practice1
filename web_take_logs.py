import json
import os
from paramiko import SSHClient, AutoAddPolicy
from datetime import datetime
import re
import psycopg2

db_params = {
    'host': '158.160.63.207',
    'database': 'kal',
    'user': 'chapcheliza',
    'password': 'admin'
}

ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())
ssh.connect('158.160.63.207', username='chapcheliza', password='')

log_path = '/var/log/apache2/access.log'

logs = []
with ssh.open_sftp() as sftp:
    with sftp.open(log_path) as file:
        for log in file:
            log_parts = log.strip().split(' ')
            if len(log_parts) >= 8:
                timestamp_str = re.search(r'\[(.*?)\]', log).group(1)
                timestamp_str = timestamp_str.rsplit(':', 1)[0]
                timestamp = datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M')

                ip = log_parts[0]
                method = log_parts[5].strip('"')
                url = log_parts[6].strip('"')[:255]

                status_code = log_parts[8]
                if status_code.isdigit():
                    status_code = int(status_code)
                else:
                    status_code = None

                response_size = log_parts[9].strip('"')
                if response_size.isdigit():
                    response_size = int(response_size)
                else:
                    response_size = None

                message = ' '.join(log_parts[10:]).strip('"')[:255]

                log_data = {
                    'timestamp': timestamp.strftime('%Y-%m-%d %H:%M'),
                    'ip': ip,
                    'method': method,
                    'url': url,
                    'status_code': status_code,
                    'response_size': response_size,
                    'message': message
                }
                logs.append(log_data)

ssh.close()

with open('web_logs.json', 'w') as json_file:
    json.dump(logs, json_file)

connection = psycopg2.connect(**db_params)
cursor = connection.cursor()

for log_data in logs:
    cursor.execute(
        "INSERT INTO logs (timestamp, ip, method, url, status_code, response_size, message) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (
            log_data['timestamp'],
            log_data['ip'],
            log_data['method'],
            log_data['url'],
            log_data['status_code'],
            log_data['response_size'],
            log_data['message']
        )
    )

connection.commit()

cursor.close()
connection.close()

print('Логи успешно сохранены в JSON файле и базе данных.')
