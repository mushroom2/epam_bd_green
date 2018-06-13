import paramiko


def run_sj():
    host = '127.0.0.1'
    user = 'root'
    secret = 'sfera1488'
    port = 2222
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=port)
    stdin, stdout, stderr = client.exec_command('source /opt/rh/python27/enable')
    data = stdout.read() + stderr.read()
    stdin, stdout, stderr = client.exec_command('spark-submit ./spark1.py')
    data = stdout.read() + stderr.read()
    print(data)
    client.close()
