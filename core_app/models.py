from __future__ import annotations
import uuid
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from django.db import models

if TYPE_CHECKING:
    from datetime import time


class Brand(models.Model):
    id: uuid.UUID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    name: str = models.CharField(max_length=255)

    # Assuming these numbers in usd ($)
    daily_budget: Optional[Decimal] = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    monthly_budget: Optional[Decimal] = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Campaign(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        PAUSED_BY_SYSTEM = "PAUSED_BY_SYSTEM", "Paused by System"
        PAUSED_BY_USER = "PAUSED_BY_USER", "Paused by User"

    id: uuid.UUID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    brand: Brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name="campaigns"
    )
    name: str = models.CharField(max_length=255)
    status: str = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE
    )

    daily_budget: Optional[Decimal] = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    monthly_budget: Optional[Decimal] = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )

    is_dayparting_enabled: bool = models.BooleanField(default=False)

    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Spend(models.Model):
    id: uuid.UUID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    campaign: Campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="spends"
    )
    date: models.DateField = models.DateField()

    daily_spend: Decimal = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_spend: Decimal = models.DecimalField(max_digits=12, decimal_places=2)

    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("campaign", "date")  # prevent duplicates

    def __str__(self) -> str:
        return f"{self.campaign.name} - {self.date}"


class DaypartingSchedule(models.Model):
    class DayOfWeek(models.TextChoices):
        MON = "MON", "Monday"
        TUE = "TUE", "Tuesday"
        WED = "WED", "Wednesday"
        THU = "THU", "Thursday"
        FRI = "FRI", "Friday"
        SAT = "SAT", "Saturday"
        SUN = "SUN", "Sunday"

    id: uuid.UUID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    campaign: Campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="dayparting_schedules"
    )

    day_of_week: str = models.CharField(max_length=3, choices=DayOfWeek.choices)
    start_time: time = models.TimeField()
    end_time: time = models.TimeField()
    timezone: str = models.CharField(
        max_length=64, default="UTC"
    )  # not needed (if all in UTC)

    def __str__(self) -> str:
        return f"{self.campaign.name} - {self.day_of_week}: {self.start_time}-{self.end_time}"
