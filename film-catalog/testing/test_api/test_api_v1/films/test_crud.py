import random
from os import getenv
from unittest import TestCase

if getenv("TESTING") != "1":
    msg = "Environment not ready for testing"
    raise OSError(msg)


def total(a: int, b: int) -> int:
    return a + b


class TotalTestCase(TestCase):
    def test_total(self) -> None:
        num_a = random.randint(1, 50)
        num_b = random.randint(1, 50)
        result = total(num_a, num_b)
        expected_result = num_a + num_b
        self.assertEqual(result, expected_result)
