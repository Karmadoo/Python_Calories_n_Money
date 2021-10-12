import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, new_rec):
        self.new_rec = new_rec
        self.records.append(new_rec)

    def get_today_stats(self):
        sp_td = 0
        for i in self.records:
            if i.date == dt.date.today():
                sp_td += i.amount
        return sp_td

    def get_week_stats(self):
        current = dt.datetime.now().date()
        differ = dt.timedelta(days=7)
        sp_wk = 0
        for i in self.records:
            if current - differ < i.date <= current:
                sp_wk += i.amount
        return sp_wk

    def day_reminder(self):
        d_reminder = self.limit - self.get_today_stats()
        return d_reminder


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories = self.day_reminder()
        if calories <= 0:
            return 'Хватит есть!'
        else:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {calories} кКал')


class CashCalculator(Calculator):
    USD_RATE = 71.00
    EURO_RATE = 83.00
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currency):
        CURRUNCIES = {'rub': ('руб', self.RUB_RATE),
                      'eur': ('Euro', self.EURO_RATE),
                      'usd': ('USD', self.USD_RATE)}
        self.currency = currency
        cash = self.day_reminder()
        if cash == 0:
            return 'Денег нет, держись'
        currency_name, rate = CURRUNCIES[currency]
        cash = round(cash / rate, 2)
        if cash > 0:
            return f'На сегодня осталось {cash} {currency_name}'
        else:
            cash = abs(cash)
            return f'Денег нет, держись: твой долг - {cash} {currency_name}'
