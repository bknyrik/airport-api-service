from time import sleep

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as PsycopgOperationalError


class Command(BaseCommand):

    def handle(self, *args, **options) -> None:
        self.stdout.write("Wait for the database...")
        db_is_up = False

        while not db_is_up:
            try:
                self.check(databases=("default",))
                db_is_up = True
            except (OperationalError, PsycopgOperationalError):
                self.stdout.write(
                    "The database is unavailable, wait for a second..."
                )
                sleep(1)

        self.stdout.write(self.style.SUCCESS("The database is available!"))
