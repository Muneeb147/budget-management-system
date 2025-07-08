from celery import shared_task
from core_app.services import budget_enforcer


@shared_task
def check_all_campaign_budgets() -> None:
    """
    Entry task to scan all campaigns and pause any that exceed budget.
    """
    budget_enforcer.check_and_pause_exceeding_campaigns()
