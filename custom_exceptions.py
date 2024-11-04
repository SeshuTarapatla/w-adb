

class IPAddressNotFoundError(Exception):
    def __init__(self):
        self.message = "Raised when IP Address not found or unreachable in network"

class SocketConnectionFailed(Exception):
    def __init__(self):
        self.message = "Raised when IP Address:Port Socket connection timeout or unavailable"
