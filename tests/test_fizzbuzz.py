from src.fizzbuzz import fizzbuzz


def test_divisible_by_both_3_and_5():
    assert fizzbuzz(15) == "FizzBuzz"
    assert fizzbuzz(30) == "FizzBuzz"


def test_divisible_by_3_only():
    assert fizzbuzz(3) == "Fizz"
    assert fizzbuzz(9) == "Fizz"


def test_divisible_by_5_only():
    assert fizzbuzz(5) == "Buzz"
    assert fizzbuzz(20) == "Buzz"


def test_not_divisible():
    assert fizzbuzz(1) == "1"
    assert fizzbuzz(7) == "7"
    assert fizzbuzz(11) == "11"
