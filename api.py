from flask import Flask, request
import psycopg2
import json
from dotenv import load_dotenv
import os
from datetime import datetime
import re

app = Flask(__name__)

load_dotenv()

db_params = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}


def save_to_json(logs):
    with open('web_logs.json', 'a') as file:
        json.dump(logs, file)
        file.write('\n')


@app.route('/upload_logs', methods=['POST'])
def upload_logs():
    file = request.files['file']
    logs = file.read().decode('utf-8')

    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    for log in logs.splitlines():
        log_parts = log.strip().split(' ')
        if len(log_parts) >= 8:
            timestamp_str = re.search(r'\[(.*?)\]', log).group(1)
            timestamp_str = timestamp_str.rsplit(':', 1)[0]
            timestamp = datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M')

            ip = log_parts[0]
            method = log_parts[5].strip('"')
            url = log_parts[6].strip('"')[:255]
            status_code = int(log_parts[8])
            response_size = int(log_parts[9])

            message = ' '.join(log_parts[10:]).strip('"')[:255]

            cursor.execute(
                "INSERT INTO logs (timestamp, ip, method, url, status_code, response_size, message) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (timestamp, ip, method, url, status_code, response_size, message))

            log_data = {
                'timestamp': timestamp.strftime('%Y-%m-%d %H:%M'),
                'ip': ip,
                'method': method,
                'url': url,
                'status_code': status_code,
                'response_size': response_size,
                'message': message
            }
            save_to_json(log_data)

    conn.commit()
    cursor.close()
    conn.close()

    return 'Логи успешно загружены в базу данных и сохранены в JSON файле!'

if __name__ == '__main__':
    app.run()
