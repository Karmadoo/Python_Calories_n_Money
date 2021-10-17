import datetime as dt


class Calculator:
    TIME_DELTA = dt.timedelta(days=7)

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, new_rec):
        self.records.append(new_rec)

    def get_today_stats(self):
        tooday = dt.date.today()
        return sum(record.amount for record in self.records if
                   record.date == tooday)

    def get_week_stats(self):
        current = dt.date.today()
        current_delta = current - self.TIME_DELTA
        return sum(record.amount for record in self.records
                   if current_delta < record.date <= current)


class Record:
    DATE_TOODAY = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, self.DATE_TOODAY).date()


class CaloriesCalculator(Calculator):
    STOP = 'Хватит есть!'
    ALLOWED = ('Сегодня можно съесть что-нибудь ещё, '
               'но с общей калорийностью не более {number} кКал')

    def get_calories_remained(self):
        calories = self.limit - self.get_today_stats()
        if calories <= 0:
            return self.STOP
        return self.ALLOWED.format(number=calories)


class CashCalculator(Calculator):
    STOP = 'Денег нет, держись'
    ALOWED = 'На сегодня осталось {number} {currency}'
    DUTY = 'Денег нет, держись: твой долг - {number} {currency}'
    ERROR = 'Ошибка. Значение валюты должно быть поддерживаемым'
    USD_RATE = 60.00
    EURO_RATE = 70.00
    RUB_RATE = 1.00
    CURRUNCIES = {'rub': ('руб', RUB_RATE),
                  'eur': ('Euro', EURO_RATE),
                  'usd': ('USD', USD_RATE)}

    def get_today_cash_remained(self, currency):
        cash = self.limit - self.get_today_stats()
        if currency not in self.CURRUNCIES:
            raise ValueError(self.ERROR)
        if cash == 0:
            return self.STOP
        cash_variable, rate = self.CURRUNCIES[currency]
        cash = round(cash / rate, 2)
        if cash > 0:
            return self.ALOWED.format(number=cash,
                                      currency=cash_variable)
        return self.DUTY.format(number=abs(cash),
                                currency=cash_variable)
