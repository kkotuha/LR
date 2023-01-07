import re
import subprocess

server_ip = 'server'


def client():
    pro = subprocess.Popen(
        ['iperf', '-c', f'{server_ip}', '-i', '1', '-u'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    pro.wait()
    return pro.stdout.read().decode('utf8'), pro.stderr.read().decode('utf8')


def parser():
    keys = ['Interval', 'Transfer', 'Bandwidth']
    result = []
    stdout, stderr = client()
    parser_result_interval = re.compile(r'[0-9].[0-9]{4}-[0-9].[0-9]{4}')
    parser_result_transfer = re.compile(r'[0-9]+\sKBytes')
    parser_result_bandwidth = re.compile(r'[0-9].[0-9]{2}\sMbits/sec')
    grouped_result = list(
        zip(
            parser_result_interval.findall(stdout),
            parser_result_transfer.findall(stdout),
            parser_result_bandwidth.findall(stdout)
        )
    )
    for res in grouped_result:
        result.append({key: value for key, value in list(zip(keys, res))})

    return result, stderr


if __name__ == '__main__':
     result, error = parser()
