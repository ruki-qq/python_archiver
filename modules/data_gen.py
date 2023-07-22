from attr._make import Attribute
from attrs import define, field
from mimesis import Person
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

    @rows.validator
    def check_range(self, attribute: Attribute, value: int):
        if value < 500_000 or value > 2_000_000:
            raise ValueError(
                'You must provide number between 500 thousands and 2 millions'
            )

    def generate_person_profile(self) -> list[str | int]:
        """Generate single row with profile data."""

        person: Person = Person()

        return [
            person.full_name(),
            person.height(),
            person.gender(),
            person.age(),
            person.language(),
            person.phone_number(),
            person.email(),
            person.password(),
            person.political_views(),
            person.academic_degree(),
            person.blood_type(),
        ]

    def generate_table(self) -> list[list[str | int]]:
        """Generate full table with provided rows number."""

        result: list[list[str | int]] = []
        with IncrementalBar(
            'Generating', max=self.rows, suffix='%(elapsed)d s.'
        ) as bar:
            for _ in range(self.rows):
                result.append(self.generate_person_profile())
                bar.next()
        return result
