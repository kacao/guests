class Vouchers:
    def __init__(self):
        self._vouchers = None

    def reset(self, vouchers):
        """
        convert a list of voucher from unifi controller's response
        into a dict by create_time
        """
        self._vouchers = {}
        for voucher in vouchers:
            self._vouchers[voucher['create_time']] = voucher

    def get_list(self):
        if self._vouchers:
            return self._vouchers.copy()
        else:
            return None

    def by_time(self, create_time):
        return self._voucher[create_time]

