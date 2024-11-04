from console_tools import log, _success, _failed, Parser
from custom_exceptions import IPAddressNotFoundError, SocketConnectionFailed
from process_tools import ping, safe_exit, socket_check


class ADB:
    @staticmethod
    def pair(ip_port=None, code=None):
        ip_addr = None
        if ip_port:
            log.info('IP_PORT:', ip_port, blankline=True)
            try:
                ip_addr, port = ip_port.split(':')
                log.info(f'IP_Port parsed into IP Address: {ip_addr} | Port: {port}')
                log.info('Performing network checks')
                if ping(ip_addr):
                    log.info(f'IP Address verification: PING > {_success}')
                if socket_check(ip_addr,port):
                    log.info(f'Port verification: SOCKET > {_success}')
            except ValueError:
                safe_exit(f'Invalid IP_PORT: {ip_port}','Please follow the format: "ip_address:port" [ 192.168.0.0:8888 ]')
            except IPAddressNotFoundError:
                safe_exit(f'IP Address verification: PING > {_failed}','Please verify the IP Address')
            except SocketConnectionFailed:
                safe_exit(f'Port verification: SOCKET > {_failed}','Please verify the Port')
        else: pass



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
