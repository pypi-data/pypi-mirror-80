import re

class CreditCardChecker:
    def __init__(self, card_num):
        self.card_num = card_num

    def valid(self):
        number = self.card_num.replace(' ', '')
        if len(number) < 2 or re.findall(r"\D", number):
            return False
        total = 0
        reversed_num = number[::-1]
        for i, char in enumerate(reversed_num):
            digit = int(reversed_num[i])
            if i % 2 == 1:
                digit *= 2
                if digit > 9:
                    digit -= 9
            total += digit
        return total % 10 == 0
