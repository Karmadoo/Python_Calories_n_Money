import datetime as dt


class Calculator:
    TIME_DIFFERENCE = dt.timedelta(days=7)

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, new_rec):
        self.records.append(new_rec)

    def get_today_stats(self):
        return sum(i.amount for i in self.records if i.date == dt.date.today())

    def get_week_stats(self):
        current = dt.date.today()
        current_delta = current - Calculator.TIME_DIFFERENCE
        return sum(i.amount for i in self.records
                   if current_delta < i.date <= current)


class Record:
    CURRENT_DATE = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, Record.CURRENT_DATE).date()


class CaloriesCalculator(Calculator):
    STOP_PHRASE = 'Хватит есть!'

    def get_calories_remained(self):
        calories = self.limit - self.get_today_stats()
        if calories <= 0:
            return CaloriesCalculator.STOP_PHRASE
        return (f'Сегодня можно съесть что-нибудь ещё, '
                f'но с общей калорийностью не более {calories} кКал')


class CashCalculator(Calculator):
    STOP_PHRASE = 'Денег нет, держись'
    ALOWED_PHRASE = ('На сегодня осталось {key1} {key2}')
    DUTY_PHRASE = ('Денег нет, держись: твой долг - {key1} {key2}')
    USD_RATE = 60.00
    EURO_RATE = 70.00
    RUB_RATE = 1.00
    CURRUNCIES = {'rub': ('руб', RUB_RATE),
                  'eur': ('Euro', EURO_RATE),
                  'usd': ('USD', USD_RATE)}

    def get_today_cash_remained(self, currency):
        cash = self.limit - self.get_today_stats()
        if cash == 0:
            return CashCalculator.STOP_PHRASE
        if currency not in CashCalculator.CURRUNCIES.keys():
            raise ValueError('Введите значение rub, eur или usd')
        cash_variable, rate = CashCalculator.CURRUNCIES[currency]
        cash = round(cash / rate, 2)
        if cash > 0:
            return CashCalculator.ALOWED_PHRASE.format(key1=cash,
                                                       key2=cash_variable)
        return CashCalculator.DUTY_PHRASE.format(key1=abs(cash),
                                                 key2=cash_variable)
