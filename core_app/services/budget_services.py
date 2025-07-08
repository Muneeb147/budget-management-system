import logging
import pytz
from datetime import date, datetime, timezone

from core_app.models import Campaign, Spend, Campaign, DaypartingSchedule

logger = logging.getLogger(__name__)


def check_and_pause_exceeding_campaigns() -> None:
    today = date.today()
    campaigns = Campaign.objects.filter(status=Campaign.Status.ACTIVE)

    for campaign in campaigns:
        try:
            spend = Spend.objects.get(campaign=campaign, date=today)
        except Spend.DoesNotExist:
            logger.info(f"No spend record for campaign {campaign.id} today.")
            continue

        over_daily = False
        over_monthly = False

        if campaign.daily_budget and spend.daily_spend >= campaign.daily_budget:
            over_daily = True
        elif (
            campaign.brand.daily_budget
            and spend.daily_spend >= campaign.brand.daily_budget
        ):
            over_daily = True

        if campaign.monthly_budget and spend.monthly_spend >= campaign.monthly_budget:
            over_monthly = True
        elif (
            campaign.brand.monthly_budget
            and spend.monthly_spend >= campaign.brand.monthly_budget
        ):
            over_monthly = True

        if over_daily or over_monthly:
            campaign.status = Campaign.Status.PAUSED_BY_SYSTEM
            campaign.save(update_fields=["status"])
            logger.warning(
                f"Campaign {campaign.id} paused due to {'daily' if over_daily else 'monthly'} budget limit."
            )


def reactivate_daily_campaigns() -> None:
    """Reactivate PAUSED_BY_SYSTEM campaigns if they're now under daily budget."""

    today = date.today()

    for campaign in Campaign.objects.filter(status=Campaign.Status.PAUSED_BY_SYSTEM):
        spend, _ = Spend.objects.get_or_create(campaign=campaign, date=today)

        limit = campaign.daily_budget or campaign.brand.daily_budget
        if limit and spend.daily_spend < limit:
            campaign.status = Campaign.Status.ACTIVE
            campaign.save(update_fields=["status"])
            logger.info(f"Campaign {campaign.id} reactivated under daily budget.")


def reactivate_monthly_campaigns() -> None:
    """Reactivate PAUSED_BY_SYSTEM campaigns if they're now under monthly budget."""

    today = date.today()

    for campaign in Campaign.objects.filter(status=Campaign.Status.PAUSED_BY_SYSTEM):
        spend, _ = Spend.objects.get_or_create(campaign=campaign, date=today)

        limit = campaign.monthly_budget or campaign.brand.monthly_budget
        if limit and spend.monthly_spend < limit:
            campaign.status = Campaign.Status.ACTIVE
            campaign.save(update_fields=["status"])
            logger.info(f"Campaign {campaign.id} reactivated under monthly budget.")


def enforce_dayparting_for_all_campaigns() -> None:
    """Enable or pause campaigns based on their allowed time schedules (dayparting)."""

    campaigns = Campaign.objects.filter(is_dayparting_enabled=True)

    for campaign in campaigns:
        now_utc = datetime.now(timezone.utc)

        today_weekday = now_utc.strftime("%a").upper()[:3]  # e.g., "MON" "TUE" etc..
        schedules: list[DaypartingSchedule] = campaign.dayparting_schedules.filter(
            day_of_week=today_weekday
        )

        should_be_active = False

        for schedule in schedules:
            now_local = now_utc

            if schedule.timezone != "UTC":
                tz = pytz.timezone(schedule.timezone)
                now_local = now_utc.astimezone(tz)

            now_local = now_local.time()

            # If any schedule allows, make it active
            if schedule.start_time <= now_local <= schedule.end_time:
                should_be_active = True
                break

        if should_be_active:
            if campaign.status == Campaign.Status.PAUSED_BY_SYSTEM:
                campaign.status = Campaign.Status.ACTIVE
                campaign.save(update_fields=["status"])
                logger.info(f"Campaign {campaign.id} reactivated by dayparting.")
        else:
            if campaign.status == Campaign.Status.ACTIVE:
                campaign.status = Campaign.Status.PAUSED_BY_SYSTEM
                campaign.save(update_fields=["status"])
                logger.info(f"Campaign {campaign.id} paused by dayparting.")
