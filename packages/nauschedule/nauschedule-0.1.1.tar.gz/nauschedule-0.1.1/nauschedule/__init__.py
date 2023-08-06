import requests


class NAUScheduler:
    def __init__(self):
        self._group_scheduler_url = 'http://rozklad.nau.edu.ua/api/v1/schedule'
        self._department_url = 'http://rozklad.nau.edu.ua/api/v1/departments'

    def get_departments(self):
        """list with info about department"""
        response = requests.get(self._department_url).json()['departments']
        return response

    def get_department_codes(self):
        """ :return dict where key its shortname departments value its code of departments """
        result = {}
        departments = self.get_departments()

        for department in departments:
            result.update({department['SHORT']: department['CODE']})

        return result

    @staticmethod
    def get_group_stream_and_code(group_number: str):
        return group_number[-1]

    @staticmethod
    def get_group_course(group_number: str):
        return group_number[0]

    def _correct_department_name(self, dep_name):
        department_codes = self.get_department_codes()
        try:
            return True, department_codes[dep_name]
        except KeyError:
            return False, 'Неправильное название факультета.'

    def get_schedule(self, department_name: str, group_number: str, subgroup=1, only_lecture=None, only_practice=None):
        department_codes = self.get_department_codes()
        group_code = self.get_group_stream_and_code(group_number)
        group_stream = group_code
        group_course = self.get_group_course(group_number)

        correct_department_name = self._correct_department_name(department_name)

        if correct_department_name[0]:

            url = f'{self._group_scheduler_url}/{department_codes[department_name]}/{group_course}/{group_stream}/{group_code}/{subgroup}'
            response = requests.get(url).json()

            if response['status']:

                if only_lecture and only_practice:
                    return 'Допустимо выбрать только 1 флаг, если вам нужно получить все пары - пропустите установку флагов.'

                elif only_lecture:
                    lectures = {}
                    for date in response['schedule']:
                        if response['schedule'][date]['isLecture']:
                            lectures.update({date: response['schedule'][date]})
                    return lectures

                elif only_practice:
                    practices = {}
                    for date in response['schedule']:
                        print(date)
                        if not response['schedule'][date]['isLecture']:
                            practices.update({date: response['schedule'][date]})
                    return practices

                else:
                    return response['schedule']

            else:
                return response['message']
        else:
            return correct_department_name[1]

if __name__ == '__main__':
    nau = NAUScheduler()
    print(nau.get_schedule('ФАЕТ', '05'))
