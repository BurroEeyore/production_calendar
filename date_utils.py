import json
from datetime import timedelta, datetime, date


class Days(object):

    @staticmethod
    def _get_all_relax_days(year):
        """ Метод получения выходных по производственному календарю (году)

        :param year: int год производственного календаря
        :return: dict календаря или пустой dict
        """

        relax_days = {}
        try:
            json_file = '/home/konovalov/projects/py3/standalonetasks/utils/{}.json'.format(year)
            with open(file=json_file) as file:
                relax_days = json.load(file)
        except:
            FileNotFoundError('Производственный календарь на {0} год не найден'.format(year))

        return relax_days.get('relax_days', {})

    @staticmethod
    def _get_years(year_from, year_till):
        """Получаем список годов между двух дат

        :param year_from: int начальный год
        :param year_till: int конечный год
        :return: list список годов
        """

        years = list()

        while year_from <= year_till:
            years.append(year_from)
            year_from += 1
        return years

    def get_next_day(self, day, is_work=True):
        """ Метод возвращает первый рабочий/выходной день, следующий за указанным

        :param date: datetime, date дата, для которой определяем
        :param is_work: bool True - рабочий, False - выходной
        :return: datetime, date or None тип соответствует param date
        """

        if not isinstance(day, (datetime, date)):
            return None
        else:
            new_day = day + timedelta(days=1)
            relax_days = self._get_all_relax_days(new_day.year).get(str(new_day.month), [])

            while new_day.day in relax_days if is_work else new_day.day not in relax_days:
                old_day = new_day
                new_day += timedelta(days=1)
                if new_day.month > old_day.month:
                    relax_days = self._get_all_relax_days(new_day.year).get(str(new_day.month), [])

            return new_day

    def is_relax_day(self, relax_date):
        """Метод возвращает True, если указанная дата - выходной день

        :param relax_date: datetime, date проверяемая дата
        :return: bool or None True - выходной, False - рабочий, None в случае ошибки
        """

        result = None
        if isinstance(relax_date, (datetime, date)):
            relax_days = self._get_all_relax_days(relax_date.year).get(str(relax_date.month), [])
            if relax_days:
                result = relax_date.day in relax_days
        return result

    def get_count_days(self, date_from, date_till):
        """Метод считает рабочие/выходные/календарные дни между 2 дат, ВКЛЮЧАЯ ГРАНИЦЫ

        :param date_from: datetime, date начало периода
        :param date_till: datetime, date конец периода
        :return: days dict содержит количество рабочих, выходных, календарных дней
        """

        days = {
            'work': 0,
            'relax': 0,
            'calendar': 0
        }

        if not all(map(lambda d: isinstance(d, (date, datetime)), (date_from, date_till))):
            return days

        if date_from > date_till:
            date_from, data_till = date_till, date_from

        all_relax_days = dict()
        years = self._get_years(date_from.year, date_till.year)
        for year in years:
            all_relax_days[year] = self._get_all_relax_days(year)

        delta = timedelta(days=1)
        while date_from <= date_till:
            if not all_relax_days.get(date_from.year).get(str(date_from.month), []):
                pass
            elif date_from.day in all_relax_days.get(date_from.year).get(str(date_from.month), []):
                days['relax'] += 1
            else:
                days['work'] += 1
            days['calendar'] += 1
            date_from += delta
        return days


if __name__ == '__main__':
    pass
