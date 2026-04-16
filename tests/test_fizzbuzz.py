from src.fizzbuzz import fizzbuzz


def test_fizzbuzz_divisible_by_both():
    assert fizzbuzz(15) == "FizzBuzz"


def test_fizzbuzz_divisible_by_both_30():
    assert fizzbuzz(30) == "FizzBuzz"


def test_fizzbuzz_zero():
    assert fizzbuzz(0) == "FizzBuzz"


def test_fizzbuzz_divisible_by_3_only():
    assert fizzbuzz(3) == "Fizz"


def test_fizzbuzz_divisible_by_3_only_9():
    assert fizzbuzz(9) == "Fizz"


def test_fizzbuzz_divisible_by_5_only():
    assert fizzbuzz(5) == "Buzz"


def test_fizzbuzz_divisible_by_5_only_10():
    assert fizzbuzz(10) == "Buzz"


def test_fizzbuzz_neither():
    assert fizzbuzz(1) == "1"


def test_fizzbuzz_neither_7():
    assert fizzbuzz(7) == "7"
