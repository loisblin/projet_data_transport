import pandas as pd

class Map_service:
    def __init__(self,trip_repo,city_repo):
        self.trip_repo = trip_repo
        self.city_repo = city_repo

    def get_trips_map_data(self,time_granularity="week",day=None,hour=None):
        
        data = self.trip_repo.get_trips_map_data(time_granularity,day,hour)
        df = pd.DataFrame(data)

        return df
    def get_cities_coords_dict(self):
        dict = self.city_repo.get_city_coords_dict()
        
        return dict