
import os
import binascii


class FakeBank:
    def __init__(self):
        self._users_card_to_pin = {
            "12341234": "1234",
            "75615123": "5432" 
        }
        self._balance = {
            "12341234": "$100,000",
            "75615123": "$1,433,000",
        }
        self._keys = {}

    def authenticate(self, card_number, pin):
        if self._users_card_to_pin[card_number] == pin:
            hash_str = binascii.hexlify(os.urandom(16))
            self._keys[hash_str] = card_number
            return hash_str
        else:
            raise Exception('authentication error')

    def get_balance(self, card_number, hash_str):
        user_card = self._keys.get(hash_str, None)
        if user_card == card_number:
            return self._balance[user_card]
        else:
            raise Exception('secret key is wrong')

    def widthdraw(self, card_number, hash_str, amount):
        user_card = self._keys.get(hash_str, None)
        if user_card == card_number:
            if amount > self._balance[user_card]:
                raise Exception('balance is not enough')
            else:
                self._balance[user_card] -= amount
                return True
        else:
           raise Exception('secret key is wrong') 
    
    def deposit(self, card_number, hash_str, amount):
        user_card = self._keys.get(hash_str, None)
        if user_card == card_number:
            self._balance[user_card] += amount
            return True
        else:
           raise Exception('secret key is wrong') 

class FakeMechanicalDispenser:

    def widthraw(self, amount):
        print('widthrawing', amount)
    
    def deposit(self):
        amount = 10000
        print('depositting', amount)
        return amount


class ATM:

    def __init__(self, bank, mechanical_dispenser):
        self._user_card_number = None
        self._user_is_authenticated = False
        self._user_secret_key = None
        self._bank = bank
        self._mechanical_dispenser = mechanical_dispenser
        self._current_cash = 100000

    def authenticate(self, card_number, pin):
        """Given a card numbeer and a pin, authenticate the user
        :param card_number: an string of numbers 
        :param pin: a 4 digit string
        """
        try:
            self._secret_key = self.bank.authenticate(card_number, pin)
            self._card_number = card_number
            return True
        except Exception:
            self._card_number = None
            self._is_authenticated == False
            return False

    def get_balance(self):
        if self._is_authenticated:
            return self.bank.get_balance(self._card_number, self._secret_key)
        else:
            raise Exception('not authenticated')

    def widthdraw(self, amount):
        if self._is_authenticated:
            try: 
                self.bank.widthdraw(self._card_number, self._secret_key, amount)
            except Exception:
                raise Exception('balance is not enough')

            try:
                self._mechanical_dispenser.widthdraw(amount)
            except Exception:
                raise Exception("not enough bills in the ATM")

        else:
            raise Exception('not authenticated')
    
    def deposit(self):
        if self._is_authenticated:
            amount = self._mechanical_dispenser.deposit()
            self.bank.deposit(self._card_number, self._secret_key, amount)
            
        else:
            raise Exception('not authenticated')


if __name__ == '__main__':
    bank = FakeBank()
    dispenser = FakeMechanicalDispenser()
    atm = ATM(bank, dispenser)