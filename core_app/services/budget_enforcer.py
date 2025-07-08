from datetime import date
from typing import Optional
from core_app.models import Campaign, Spend
import logging


def check_and_pause_exceeding_campaigns() -> None:
    """
    Iterate over campaigns and pause any that exceed their daily or monthly budgets.
    """
    today = date.today()
    campaigns = Campaign.objects.filter(status=Campaign.Status.ACTIVE)

    logging.info(f"Checking campaigns for budget enforcement on {today}")

    if not campaigns:
        return

    for campaign in campaigns:
        spend = get_latest_spend(campaign_id=campaign.id, on_date=today)

        # Assuming only spend entry per day

        if spend is None:
            continue  # no spend entry for today

        over_daily = (
            campaign.daily_budget is not None
            and spend.daily_spend >= campaign.daily_budget
        )
        over_monthly = (
            campaign.monthly_budget is not None
            and spend.monthly_spend >= campaign.monthly_budget
        )

        if over_daily or over_monthly:
            campaign.status = Campaign.Status.PAUSED_BY_SYSTEM
            campaign.save(update_fields=["status"])


def get_latest_spend(campaign_id: str, on_date: date) -> Optional[Spend]:
    try:
        return Spend.objects.get(campaign_id=campaign_id, date=on_date)
    except Spend.DoesNotExist:
        return None
