from src.number_utils import number_to_words


def test_zero():
    assert number_to_words(0) == 'zero'


def test_forty_two():
    assert number_to_words(42) == 'forty two'


def test_one_hundred():
    assert number_to_words(100) == 'one hundred'


def test_nine_hundred_ninety_nine():
    assert number_to_words(999) == 'nine hundred ninety nine'


def test_single_digits():
    assert number_to_words(1) == 'one'
    assert number_to_words(9) == 'nine'


def test_teens():
    assert number_to_words(11) == 'eleven'
    assert number_to_words(19) == 'nineteen'


def test_exact_tens():
    assert number_to_words(20) == 'twenty'
    assert number_to_words(90) == 'ninety'


def test_hundreds_with_remainder():
    assert number_to_words(115) == 'one hundred fifteen'
    assert number_to_words(256) == 'two hundred fifty six'
