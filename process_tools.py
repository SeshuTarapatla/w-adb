from socket import socket, AF_INET, SOCK_STREAM
from subprocess import run
from console_tools import log
from custom_exceptions import IPAddressNotFoundError, SocketConnectionFailed


_exec = lambda cmd: run(cmd, shell=True, capture_output=True)
_output = lambda cmd: _exec(cmd).stdout.decode()


def safe_exit(errorMsg, exitMsg=None):
    log.error(errorMsg)
    if exitMsg: print(exitMsg)
    print()
    log.error('Process exited with non-zero status')
    exit(-1)


def ping(ip):
    with log.status(f'Checking ping status to: {ip}'):
        cmd = f'ping -n 1 {ip}'
        if 'round trip' in _output(cmd):
            return True
        else:
            raise IPAddressNotFoundError()


def socket_check(ip, port, timeout=5):
    port = int(port)
    with log.status(f'Checking socket connection to {ip}:{port}'):
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            try:
                sock.connect((ip, port))
                return True
            except:
                raise SocketConnectionFailed()