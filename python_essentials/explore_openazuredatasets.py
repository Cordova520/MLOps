from azureml.opendatasets import PublicHolidays

from datetime import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta

today = datetime.today()
last_year = today - relativedelta(years=1)
holidays = PublicHolidays(start_date=last_year, end_date=today)
print(holidays)

holidays_df = holidays.to_pandas_dataframe()
print(holidays_df.head())

holidays_df.describe()