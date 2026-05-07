import pandas as pd

class Histo_service:
    def __init__(self,trip_repo):
        self.trip_repo= trip_repo
    
    def get_histo_data(self,time_granularity="week",day=None):
        data = self.trip_repo.get_histo_data(time_granularity,day)
        return  pd.DataFrame(data)
