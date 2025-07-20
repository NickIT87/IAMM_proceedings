from dataclasses import dataclass
from typing import Tuple

# TEST DATA
# =============================================================================
sample_exists = (
    (
        "16361",
        "14520542321241",
        "14501",
        "16521263301",
        "143513361",
        "126356341",
        "1635130541",
        "16536242102541",
        "16253621",
        "16345201",
        "143315362561",
        "10315361",
    ),
    (
        "1653624",
        "1436124",
        "1436521",
        "12635621",
        "163423",
        "105423",
        "10334210",
        "1054210"
    )
)

sample_not_exists = (
    (
        "14520542321241",
        "14501",
        "16521263301",
        "143513361",
        "126356341",
        "1635130541",
        "16536242102541",
        "16253621",
        "16345201",
        "143315362561",
        "10315361",
        "191"
    ),
    (
        "1653624",
        "1436124",
        "1436521",
        "12635621",
        "163423",
        "105423",
        "10334210",
        "1054210"
    )
)

@dataclass
class DefiningPair:
    C: Tuple[str, ...]
    L: Tuple[str, ...]


class SpecCase:
    # invalid second word of L component
    defining_pair: DefiningPair = DefiningPair(
        C=("153521", "152431"),
        L=("1342531", "123241", "13412", "1523")
    )

    canonical_pair: DefiningPair = DefiningPair(
        C=('1251', '12431'),
        L=('1531', '123', '12412')
    )

    root_label = "1"


class EtalonSample:
    defining_pair: DefiningPair = DefiningPair(
        C=(
            "01210",
            "01242154312310",
            "02352510",
            "02130214210",
            "01320213025310",
            "01323510",
            "02141345320",
            "015452034531210",
            "0214130251320",
            "01352101421320",
        ),
        L=(
            "0235431302105",
            "012410120314",
        )
    )

    canonical_pair: DefiningPair = DefiningPair(
        C=(
            '013510',
            '01543120',
            '015203120',
            '01320',
            '012412510'
        ),

        L=(
            '0214',
            '0124105'
        )
    )

    root_label = "0"


class FindShortPathCase:
    defining_pair: DefiningPair = DefiningPair(
        C = ('0120', '03530', '03524150', '03114251130', '012035241130'),
        L = ('035230', '03114230', '0351130123')
    )

    canonical_pair: DefiningPair = DefiningPair(
        C = ('0120', '0350', '031150', '0514250'),
        L = ('023', '05230')
    )

    root_label = "0"


class TestCases:
    spec = SpecCase
    sample = EtalonSample
    shortPathCase = FindShortPathCase


publication_sample: DefiningPair = DefiningPair(
    C=(
        "01410",
        "0412510",
        "0142032152140",
        "0142512510",
        "041520321410",
        "041251425140",
    ),
    L=(
        "0415214",
        "0412514215",
        "01230214",
    )
)


publication_sample_expected_result: DefiningPair = DefiningPair(
    C=(
        "0152140",
        "01425140",
        "012302410",
    ),
    L=(
        "014214",
        "014215",
    )
)


COLORS: tuple = (
    'lightcoral',
    'lightblue',
    'lightgreen',
    'yellow',
    'orange',
    'magenta',
    'pink',
    'cyan'
)

# """
# 01242154312310 02352510 02130214210 01320213025310 01323510 02141345320 015452034531210 0214130251320 01352101421320
# 0235431302105 012410120314
# """
#
# """
# 013510 01543120 015203120 01320 012412510 013510 01543120 015203120 01320 012412510
# 0214 0124105
# """
