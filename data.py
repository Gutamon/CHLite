# data.py
import pandas as pd

progress_data = {
    "classsheet": pd.DataFrame(columns=["name", "semester", "day", "type", "point"]),
    "assignment": pd.DataFrame(columns=["title", "class", "deadline", "level"]),
    "activity": pd.DataFrame(columns=["title", "location", "date", "time"])
}