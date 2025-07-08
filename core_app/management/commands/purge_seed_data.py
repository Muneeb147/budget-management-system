from django.core.management.base import BaseCommand
from core_app.models import Brand, Campaign, Spend, DaypartingSchedule


class Command(BaseCommand):
    help = "Delete all seeded test data"

    def handle(self):
        DaypartingSchedule.objects.all().delete()
        Spend.objects.all().delete()
        Campaign.objects.all().delete()
        Brand.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                "Purged all seeded brands, campaigns, spends, and schedules."
            )
        )


# Command for purging:
# python manage.py purge_seeded_data
