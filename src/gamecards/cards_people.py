from datetime import datetime, date

######################################################################

class Person:
    def __init__(self, fname, lname, bday):
        self.firstname = fname
        self.lastname = lname
        self._bday = bday

    @property
    def fullname(self):
        return self.firstname + " " + self.lastname

    @property
    def birthday(self):
        return self._bday.strftime("%d-%b-%Y") 

    @property
    def age(self):
        return self.find_age(self._bday)

    @staticmethod
    def find_age(_birthdate):
        _birth_year = _birthdate.year
        _birth_month = _birthdate.month
        _birth_date = _birthdate.day

        _today = date.today()
        _this_year = _today.year
        _this_month = _today.month
        _this_date = _today.day

        _age_in_years = _this_year - _birth_year
        if ( (_birth_month > _this_month) or
             (_birth_month == _this_month and _birth_date > _this_date) ):
            _age_in_years -= 1
        return _age_in_years

    def tostring(self):
        return ("{}, age {} [DOB: {}]".format(self.fullname, self.age, self.birthday))

######################################################################

class Player(Person):
    def __init__(self, fname, lname, bday):
        super().__init__(fname, lname, bday)
        self._wallet = 0

    @property
    def wallet(self):
        return self._wallet

    def give_money(self, value):
        self._wallet += value

    def take_money(self, value):
        if value > self._wallet:
            raise Exception ("\n *** NOT ENOUGH MONEY IN WALLET ***")
        else:
            self._wallet -= value

######################################################################

class Dealer(Person):
    def __init__(self, fname, lname, bday, employer_in, licence_in):
        super().__init__(fname, lname, bday)
        self.employer = employer_in
        self.licence = licence_in

    def tostring(self):
        _space = 4*"\u0020"
        return ("{}NAME: {}\n{}DOB: {}\n{}REGISTRATION: {}\n{}EMPLOYER: {}"
                .format(_space, self.fullname, _space, self.birthday,
                        _space, self.licence, _space, self.employer))
    
######################################################################
