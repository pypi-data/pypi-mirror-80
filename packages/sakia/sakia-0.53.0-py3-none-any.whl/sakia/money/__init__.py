from .quantitative import Quantitative
from .relative import Relative
from .quant_zerosum import QuantitativeZSum
from .relative_zerosum import RelativeZSum
from .percent_of_average import PercentOfAverage

Referentials = (
    Quantitative,
    Relative,
    PercentOfAverage,
    QuantitativeZSum,
    RelativeZSum,
)
