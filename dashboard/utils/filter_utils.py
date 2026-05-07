import pandas as pd 

def filter_by_city(df,selected_city):
    "filter a data by city "
    if selected_city is None:
        return df
    return df[df["departure_city"] == selected_city]
def fusion_same_trip(df):
    df = df.copy()

    df["route"] = df.apply(
        lambda x: tuple(sorted([x["departure_city"], x["arrival_city"]])),
        axis=1
    )

    df = (
        df.groupby("route")
        .agg({
            "Number_of_trips": "sum",
            "Average_price": "mean",
            "Average_delay": "mean"
        })
        .reset_index()
    )

    df[["departure_city", "arrival_city"]] = pd.DataFrame(df["route"].tolist(), index=df.index)
    df = df.drop(columns="route")

    return df

def fusion_same_date(df):
    df = df.copy()
    df = (
        df.groupby("period")
        .agg({
            "average_price": "mean",
            "average_delay": "mean"
        })
        .reset_index()
    )
    return df


def prepare_map_dataframe(df,selected_city):
    if selected_city is not None :
        df= filter_by_city(df,selected_city)
    else:
        df = fusion_same_trip(df)
    return df 

def prepare_histo_dataframe(df,selected_city):
    if selected_city is not None :
        df = filter_by_city(df,selected_city)
    
    else:
        df=fusion_same_date(df)
    return df 