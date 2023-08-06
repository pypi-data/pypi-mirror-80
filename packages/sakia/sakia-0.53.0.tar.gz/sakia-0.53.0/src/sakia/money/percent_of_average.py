from typing import Optional

from .base_referential import BaseReferential
from ..data.processors import BlockchainProcessor

from PyQt5.QtCore import QCoreApplication, QT_TRANSLATE_NOOP, QLocale


class PercentOfAverage(BaseReferential):
    _NAME_STR_ = QT_TRANSLATE_NOOP("PercentOfAverage", "PoA")
    _REF_STR_ = QT_TRANSLATE_NOOP("PercentOfAverage", "{0} {1}{2}")
    _UNITS_STR_ = QT_TRANSLATE_NOOP("PercentOfAverage", "PoA")
    _FORMULA_STR_ = QT_TRANSLATE_NOOP(
        "PercentOfAverage",
        """PoA = (Q / ( M(t-1) / N)) / 100
                                        <br >
                                        <table>
                                        <tr><td>PoA</td><td>Percent of Average value</td></tr>
                                        <tr><td>Q</td><td>Quantitative value</td></tr>
                                        <tr><td>M</td><td>Monetary mass</td></tr>
                                        <tr><td>N</td><td>Members count</td></tr>
                                        </table>""",
    )
    _DESCRIPTION_STR_ = QT_TRANSLATE_NOOP(
        "PercentOfAverage",
        """Another relative referential of the money.<br />
                                          Percent of Average value PoA is calculated by dividing the quantitative value Q by the average<br />
                                           then multiply by one hundred.<br />
                                          This referential is relative and can be used to display prices and accounts, when UD growth is too slow.<br />
                                          No money creation or destruction is apparent here and every account tend to<br />
                                           the 100%.
                                          """,
    )

    def __init__(self, amount, currency, app, block_number=None):
        super().__init__(amount, currency, app, block_number)
        self._blockchain_processor = BlockchainProcessor.instanciate(self.app)

    @classmethod
    def instance(
        cls, amount: float, currency: str, app, block_number: Optional[int] = None
    ):
        """
        Init PercentOfAverage referential instance

        :param amount: Amount to transform
        :param currency: Name of currency
        :param app: Application instance
        :param block_number: Block number
        :return:
        """
        return cls(amount, currency, app, block_number)

    @classmethod
    def translated_name(cls):
        return QCoreApplication.translate(
            "PercentOfAverage", PercentOfAverage._NAME_STR_
        )

    @property
    def units(self):
        return QCoreApplication.translate(
            "PercentOfAverage", PercentOfAverage._UNITS_STR_
        )

    @property
    def formula(self):
        return QCoreApplication.translate(
            "PercentOfAverage", PercentOfAverage._FORMULA_STR_
        )

    @property
    def description(self):
        return QCoreApplication.translate(
            "PercentOfAverage", PercentOfAverage._DESCRIPTION_STR_
        )

    @property
    def diff_units(self):
        return self.units

    @staticmethod
    def base_str(base):
        return ""

    def value(self):
        """
        Return relative value of amount

        value = amount / UD(t)

        :param int amount:   Value
        :param sakia.core.community.Community community: Community instance
        :return: float
        """
        mass = self._blockchain_processor.last_mass(self.currency)
        members = self._blockchain_processor.last_members_count(self.currency)
        average = mass / members
        if average > 0:
            return self.amount / average * 100
        else:
            return self.amount

    def differential(self):
        return self.value()

    def set_referential(self, value):
        """
        Set quantitative amount from referential value

        :param value: Value in referential units
        :return:
        """
        mass = self._blockchain_processor.last_mass(self.currency)
        members = self._blockchain_processor.last_members_count(self.currency)
        average = mass / members
        self.amount = value / 100 * average
        return self

    def set_diff_referential(self, value):
        """
        Set quantitative amount from differential referential value

        :param value:
        :return:
        """
        return self.set_referential(value)

    def localized(self, units=False, show_base=False):
        value = self.value()
        localized_value = QLocale().toString(
            float(value), "f", self.app.parameters.digits_after_comma
        )

        if units:
            return QCoreApplication.translate(
                "PercentOfAverage", PercentOfAverage._REF_STR_
            ).format(localized_value, "", (self.units if units else ""))
        else:
            return localized_value

    def diff_localized(self, units=False, show_base=False):
        value = self.differential()
        localized_value = QLocale().toString(
            float(value), "f", self.app.parameters.digits_after_comma
        )

        if units:
            return QCoreApplication.translate(
                "PercentOfAverage", PercentOfAverage._REF_STR_
            ).format(localized_value, "", (self.diff_units if units else ""))
        else:
            return localized_value
