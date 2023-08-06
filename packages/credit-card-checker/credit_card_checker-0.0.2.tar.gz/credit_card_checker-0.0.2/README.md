# credit_card_checker_py

I published this package on PyPI
https://pypi.org/project/credit-card-checker/

To install the package, please add the package to your Pipfile.

or run `pip3 install credit_card_checker`

## Validating a Number

Strings of length 1 or less are not valid. Spaces are allowed in the input,
but they should be stripped before checking. All other non-digit characters
are disallowed.

## Example 1: valid credit card number

```text
4539 1488 0343 6467
```

The first step of the Luhn algorithm is to double every second digit,
starting from the right. We will be doubling

```text
4_3_ 1_8_ 0_4_ 6_6_
```

If doubling the number results in a number greater than 9 then subtract 9
from the product. The results of our doubling:

```text
8569 2478 0383 3437
```

Then sum all of the digits:

```text
8+5+6+9+2+4+7+8+0+3+8+3+3+4+3+7 = 80
```

If the sum is evenly divisible by 10, then the number is valid. This number is valid!

## Example 2: invalid credit card number

```text
8273 1232 7352 0569
```

Double the second digits, starting from the right

```text
7253 2262 5312 0539
```

Sum the digits

```text
7+2+5+3+2+2+6+2+5+3+1+2+0+5+3+9 = 57
```

57 is not evenly divisible by 10, so this number is not valid.

---

## example usage

```
>>> from credit_card_checker import CreditCardChecker
>>> CreditCardChecker('234 567 891 234').valid()
True
>>> CreditCardChecker('8273 1232 7352 0569').valid()
False
```

## test

To run the tests, run `pytest credit_card_checker_test.py`

Alternatively, run the pytest module:
`python3 -m pytest credit_card_checker_test.py`
