from src.fizzbuzz import fizzbuzz


def test_fizz():
    assert fizzbuzz(3) == "Fizz"
    assert fizzbuzz(6) == "Fizz"
    assert fizzbuzz(9) == "Fizz"


def test_buzz():
    assert fizzbuzz(5) == "Buzz"
    assert fizzbuzz(10) == "Buzz"
    assert fizzbuzz(20) == "Buzz"


def test_fizzbuzz():
    assert fizzbuzz(15) == "FizzBuzz"
    assert fizzbuzz(30) == "FizzBuzz"
    assert fizzbuzz(0) == "FizzBuzz"


def test_number():
    assert fizzbuzz(1) == "1"
    assert fizzbuzz(2) == "2"
    assert fizzbuzz(7) == "7"
    assert fizzbuzz(11) == "11"
