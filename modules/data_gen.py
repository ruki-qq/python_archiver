from datetime import datetime
from random import choice
from typing import Any, ClassVar

from attrs import define
from dateutil.relativedelta import relativedelta
from mimesis import Address, Datetime, Gender, Locale, Person


@define
class DataGenerator:
    GENDERS: ClassVar[list] = [i for i in Gender.__members__.values()]
    LOCALES: ClassVar[list] = [
        i.value for i in Locale.__members__.values() if i.value != 'et'
    ]
    PERSON_COL_NAMES: list[str] = [
        'full_name',
        'country_code',
        'gender',
        'age',
        'birth_date',
        'address',
        'phone_number',
        'email',
        'password',
        'political_views',
        'academic_degree',
    ]

    def generate_person_profile(self) -> list:
        locale = choice(self.LOCALES)
        birth_date: Any = Datetime().date(1950, 2005)
        age: int = relativedelta(datetime.now(), birth_date).years
        birth_date = birth_date.strftime('%m/%d/%Y')
        person = Person(locale)
        address: str = Address(locale).address()
        gender = choice(self.GENDERS)

        return [
            person.full_name(gender),
            locale,
            gender.value,
            age,
            birth_date,
            address,
            person.phone_number(),
            person.email(),
            person.password(),
            person.political_views(),
            person.academic_degree(),
        ]

    def generate_table(self, rows) -> list[list]:
        while rows < 500_000 or rows > 2_000_000:
            rows = int(
                input('Please, provide number in range (500_000, 2_000_000): ')
            )
        return [self.generate_person_profile() for _ in range(rows)]


person = DataGenerator()
