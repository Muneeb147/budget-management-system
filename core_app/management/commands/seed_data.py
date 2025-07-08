from django.core.management.base import BaseCommand
from core_app.models import Brand, Campaign, Spend, DaypartingSchedule
from datetime import date, timedelta, time
from decimal import Decimal
import random


class Command(BaseCommand):
    help = "Seed sample data for brands, campaigns, spends, and schedules"

    def add_arguments(self, parser):

        parser.add_argument("--brands", type=int, default=1, help="Number of brands")
        parser.add_argument(
            "--campaigns",
            type=int,
            default=3,
            help="Number of campaigns to create (default: 3)",
        )
        parser.add_argument(
            "--daily-budget",
            type=Decimal,
            default=Decimal("100.00"),
            help="Daily budget per campaign (default: 100.00)",
        )
        parser.add_argument(
            "--monthly-budget",
            type=Decimal,
            default=Decimal("2500.00"),
            help="Monthly budget per campaign (default: 2500.00)",
        )
        parser.add_argument(
            "--spend-days",
            type=int,
            default=5,
            help="Number of past days to create Spend records for (default: 5)",
        )

    def handle(self, **options):
        brands = []
        campaigns_per_brand = options["campaigns"]
        for b in range(options["brands"]):
            brand = Brand.objects.create(
                name=f"Brand {b+1}",
                daily_budget=options["daily_budget"] * campaigns_per_brand,
                monthly_budget=options["monthly_budget"] * campaigns_per_brand,
            )
            brands.append(brand)

        for i in range(1, options["campaigns"] + 1):
            brand = brands[(i - 1) % len(brands)]
            campaign = Campaign.objects.create(
                brand=brand,
                name=f"Campaign {i}",
                status=Campaign.Status.ACTIVE,
                daily_budget=options["daily_budget"],
                monthly_budget=options["monthly_budget"],
                is_dayparting_enabled=(i % 2 == 0),
            )

            for d in range(options["spend_days"]):
                spend_date = date.today() - timedelta(days=d)
                Spend.objects.update_or_create(
                    campaign=campaign,
                    date=spend_date,
                    defaults={
                        "daily_spend": Decimal(
                            random.randint(20, int(options["daily_budget"]))
                        ),
                        "monthly_spend": Decimal(
                            random.randint(500, int(options["monthly_budget"]))
                        ),
                    },
                )

            if campaign.is_dayparting_enabled:
                for day in DaypartingSchedule.DayOfWeek.values:
                    DaypartingSchedule.objects.create(
                        campaign=campaign,
                        day_of_week=day,
                        start_time=time(9, 0),
                        end_time=time(17, 0),
                        timezone="UTC",
                    )

        self.stdout.write(
            self.style.SUCCESS("Seeded brands, campaigns, and schedules.")
        )
