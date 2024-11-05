from console_tools import log, _success, _failed, Parser
from custom_exceptions import IPAddressNotFoundError, SocketConnectionFailed
from process_tools import ping, safe_exit, socket_check, _exec
from re import search as re_search


class ADB:
    @staticmethod
    def network_check(ip_addr, port):
        try:
            log.info('Performing network checks')
            if ping(ip_addr):
                log.info(f'IP Address verification: PING > {_success}')
            if socket_check(ip_addr, port):
                log.info(f'Port verification: SOCKET > {_success}')
        except IPAddressNotFoundError:
            safe_exit(f'IP Address verification: PING > {_failed}', f'Please check the IP Address [{ip_addr}]')
        except SocketConnectionFailed:
            safe_exit(f'Port verification: SOCKET > {_failed}', f'Please check the Port [{port}]')

    @staticmethod
    def fetch_guid(output):
        log.info('Fetching GUID from the output')
        pattern = r"guid=([a-zA-Z0-9\-]+)"
        match = re_search(pattern, output)
        guid = match.group(1) if match else None
        return guid

    @staticmethod
    def pair(ip_port=None, code=None):
        ip_addr = None
        port = None
        if ip_port:
            log.info('IP_PORT:', ip_port, blankafter=True)
            try:
                ip_addr, port = ip_port.split(':')
                log.info(f'IP_Port parsed into IP Address: {ip_addr} | Port: {port}')
                ADB.network_check(ip_addr, port)
            except ValueError:
                safe_exit(f'Invalid IP_PORT: {ip_port}','Please follow the format: "ip_address:port" [ 192.168.0.0:8888 ]')
        else:
            log.info()
            log.info('Enter the following details >\n')
            ip_addr = input('IP Address : ')
            port    = input('Port       : ')
            code    = input('Code       : ')
            print()
            ADB.network_check(ip_addr, port)
        if not code:
            try:
                log.info()
                log.info('Enter the following details >\n')
                code    = int(input('Code       : '))
            except ValueError:
                print()
                safe_exit(f'Invalid code: {code}','Please enter a valid code')
        print()
        cmd = f'adb pair "{ip_addr}:{port}" "{code}"'
        log.info(f'Trying to pair device')
        log.info(f'adb command: {cmd}')
        with log.status('Pairing Android device over WiFi'):
            output = _exec(cmd)
        if output.returncode == 0:
            output = output.stdout.decode()
            log.info(f'Output: {output}')
            device = {
                "ip_addr": ip_addr,
                "guid": ADB.fetch_guid(output)
            }
            log.info(f'DEVICE: {device}')
        else:
            safe_exit('Pairing over WiFi failed',f'Please check the code [{code}]')


def main():
    parser = Parser()
    args = parser.parse_args()

    def flag_warns(_args,_yes=True,_all=True):
        if _yes and _args.yes:
            log.warning('-y flag is not be used with --pair')
        if _all and _args.all:
            log.warning('-a flag is not be used with --pair')

    if args.pair is not None:
        log.info("Mode: PAIR")

        # Pre-checks
        flag_warns(args)

        # pair device
        ip_port, code = (args.pair + [None, None])[:2]
        ADB.pair(ip_port, code)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
