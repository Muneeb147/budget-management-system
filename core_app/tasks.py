from celery import shared_task
from core_app.services import budget_services


@shared_task
def check_all_campaign_budgets() -> None:
    """
    Entry task to scan all campaigns and pause any that exceed budget.
    """
    budget_services.check_and_pause_exceeding_campaigns()


@shared_task
def reactivate_daily_campaigns() -> None:
    """
    Reactivate campaigns that were paused due to daily budget limits
    if they are now under the daily budget.
    """
    budget_services.reactivate_daily_campaigns()


@shared_task
def reactivate_monthly_campaigns() -> None:
    """
    Reactivate campaigns that were paused due to monthly budget limits
    if they are now under the monthly budget.
    """
    budget_services.reactivate_monthly_campaigns()


@shared_task
def enforce_dayparting_for_all_campaigns() -> None:
    """
    Enforce dayparting for all campaigns that have it enabled.
    This task should be scheduled to run at the start of each day.
    """
    budget_services.enforce_dayparting_for_all_campaigns()
