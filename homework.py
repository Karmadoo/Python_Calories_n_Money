import datetime as dt


class Calculator:
    WEEK = dt.timedelta(days=7)

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
        current_delta = current - self.WEEK
        return sum(record.amount for record in self.records
                   if current_delta < record.date <= current)


class Record:
    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, self.DATE_FORMAT).date()


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
    ERROR = 'Ошибка. Введенный параметр {wrong} не поддерживается.'
    USD_RATE = 60.00
    EURO_RATE = 70.00
    RUB_RATE = 1.00
    CURRUNCIES = {'rub': ('руб', RUB_RATE),
                  'eur': ('Euro', EURO_RATE),
                  'usd': ('USD', USD_RATE)}

    def get_today_cash_remained(self, currency):
        if currency not in self.CURRUNCIES:
            raise ValueError(self.ERROR.format(wrong=currency))
        cash = self.limit - self.get_today_stats()
        if cash == 0:
            return self.STOP
        name, rate = self.CURRUNCIES[currency]
        cash = round(cash / rate, 2)
        if cash > 0:
            return self.ALOWED.format(number=cash,
                                      currency=name)
        return self.DUTY.format(number=abs(cash),
                                currency=name)
