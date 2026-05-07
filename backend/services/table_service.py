import pandas as pd
class Table_service:
    def __init__(self,trip_repo):
        self.trip_repo = trip_repo
    def get_table_data(self,time_granularity="week",day=None,hour=None):
        data = self.trip_repo.get_table_data(time_granularity,day,hour)
        return  pd.DataFrame(data)
