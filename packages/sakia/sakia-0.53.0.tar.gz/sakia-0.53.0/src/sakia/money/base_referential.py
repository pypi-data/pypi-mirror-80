from typing import Optional


class BaseReferential:
    """
    Interface to all referentials
    """

    def __init__(
        self, amount: float, currency: str, app, block_number: Optional[int] = None
    ):
        """
        Init base referential instance

        :param amount: Amount to transform
        :param currency: Name of currency
        :param app: Application instance
        :param block_number: Block number
        """
        self.amount = amount
        self.app = app
        self.currency = currency
        self._block_number = block_number

    # todo: remove this useless class method and replace all occurence with a classic Object() creation.
    @classmethod
    def instance(cls, amount, currency, app, block_number=None):
        return cls(amount, currency, app, block_number)

    @classmethod
    def translated_name(self):
        raise NotImplementedError()

    @property
    def units(self):
        raise NotImplementedError()

    @property
    def diff_units(self):
        raise NotImplementedError()

    def value(self):
        raise NotImplementedError()

    def differential(self):
        raise NotImplementedError()

    def set_referential(self, value):
        raise NotImplementedError()

    def set_diff_referential(self, value):
        raise NotImplementedError()

    @staticmethod
    def to_si(value, base):
        raise NotImplementedError()

    @staticmethod
    def base_str(base):
        raise NotImplementedError()

    def localized(self, units=False, show_base=False):
        raise NotImplementedError()

    def diff_localized(self, units=False, show_base=False):
        raise NotImplementedError()
