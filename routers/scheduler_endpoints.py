from models.basemodels import Finance_Data
from datetime import date, timedelta
from services import FinanceService
from fastapi import APIRouter

router = APIRouter(
    prefix='/scheduler'
)

@router.get('/report-generator')
async def report_generator():
    end = date(date.today().year, date.today().month, 1) - timedelta(1)
    start = date(end.year, end.month, 1)

    data = await FinanceService.finance_values(start, end)
    offers_sum = sum(data.offers)
    tithe_sum = sum(data.tithes)
    expense_sum = sum(data.expenses)

    entry = round(offers_sum + tithe_sum, 2)
    issues = round(expense_sum, 2)
    period_balance = round(entry - issues, 2)
    total_balance = round(sum(data.previous_balance) + period_balance, 2)

    send_finance_data = Finance_Data(
        entry=entry,
        issues=issues,
        start=start,
        end=end,
        period_balance=period_balance,
        total_balance=total_balance
    )
    send_finance = await FinanceService.finance_include(send_finance_data)
