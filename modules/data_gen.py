from datetime import datetime
from random import choice
from typing import Any, ClassVar

from attrs import define, field
from dateutil.relativedelta import relativedelta
from mimesis import Address, Datetime, Gender, Locale, Person
from progress.bar import IncrementalBar


@define
class DataGenerator:
    """Random data tables generation.

    Available fake data:
     Personal profiles leak base

    Parameters:
     ----------
     rows: int
         Number of rows in resulting table
    """

    rows: int = field()

    # @rows.validator
    # def check_range(self, attribute, value):
    #     if value < 500_000 or value > 2_000_000:
    #         raise ValueError(
    #             'You must provide number between 500 thousands and 2 millions'
    #         )

    GENDERS: ClassVar[list] = [i for i in Gender.__members__.values()]
    LOCALES: ClassVar[list] = [
        i.value for i in Locale.__members__.values() if i.value != 'et'
    ]

    def generate_person_profile(self) -> list:
        """Generate single row with profile data."""

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
            person.blood_type(),
        ]

    def generate_table(self) -> list[list]:
        """Generate full table with provided rows number."""

        result: list[list] = []
        with IncrementalBar(
            'Generating', max=self.rows, suffix='%(elapsed)d s.'
        ) as bar:
            for _ in range(self.rows):
                result.append(self.generate_person_profile())
                bar.next()
        return result
