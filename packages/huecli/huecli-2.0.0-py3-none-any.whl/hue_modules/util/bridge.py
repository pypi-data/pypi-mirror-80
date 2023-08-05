from phue import Bridge as pBridge


class Bridge:
    @staticmethod
    def init_bridge(bridge_addr):
        b = pBridge(bridge_addr)
        b.connect()
        b.get_api()
        return b
