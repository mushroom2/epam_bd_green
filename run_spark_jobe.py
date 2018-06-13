import paramiko


def run_sj():
    host = 'sandbox-hdp.hortonworks.com'
    user = 'root'
    secret = 'sfera1488'
    port = 2222
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=port)
    stdin, stdout, stderr = client.exec_command('spark-context ./spark1.py')
    data = stdout.read() + stderr.read()
    print(data)
    client.close()
