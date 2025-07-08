import pytest
from decimal import Decimal
from datetime import date
from core_app.models import Brand, Campaign, Spend
from core_app.tasks import check_all_campaign_budgets, reactivate_daily_campaigns

@pytest.mark.django_db
def test_campaign_paused_when_daily_budget_exceeded():
    brand = Brand.objects.create(name="BrandA", daily_budget=Decimal("100"))
    campaign = Campaign.objects.create(
        brand=brand, name="Camp1", daily_budget=Decimal("100")
    )
    Spend.objects.create(
        campaign=campaign,
        date=date.today(),
        daily_spend=Decimal("150"),
        monthly_spend=Decimal("300")
    )

    check_all_campaign_budgets()
    campaign.refresh_from_db()
    assert campaign.status == Campaign.Status.PAUSED_BY_SYSTEM

@pytest.mark.django_db
def test_campaign_resumes_when_under_budget_at_day_end():
    brand = Brand.objects.create(name="BrandB", daily_budget=Decimal("200"))
    campaign = Campaign.objects.create(
        brand=brand, name="Camp2", daily_budget=Decimal("200"),
        status=Campaign.Status.PAUSED_BY_SYSTEM
    )
    Spend.objects.create(
        campaign=campaign,
        date=date.today(),
        daily_spend=Decimal("50"),
        monthly_spend=Decimal("100")
    )

    reactivate_daily_campaigns()
    campaign.refresh_from_db()
    assert campaign.status == Campaign.Status.ACTIVE

@pytest.mark.django_db
def test_no_spend_record_means_campaign_remains_active():
    brand = Brand.objects.create(name="BrandC", daily_budget=Decimal("100"))
    campaign = Campaign.objects.create(
        brand=brand, name="Camp3", daily_budget=Decimal("100")
    )

    check_all_campaign_budgets()
    campaign.refresh_from_db()
    assert campaign.status == Campaign.Status.ACTIVE