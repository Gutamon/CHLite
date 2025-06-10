import gradio as gr
import pandas as pd
import requests
from data import progress_data

def upload_poster(file):
    if not file:
        return "", "", "", "", "請選擇一張圖片"
    
    try:
        webhook_url = "https://hook.us2.make.com/uvm2in4ag93htg9xs01n255mlcyf8uu4"
        with open(file, "rb") as f:
            files = {"file": f}
            response = requests.post(webhook_url, files=files)
            response.raise_for_status()
            data = response.json()
            return (
                data.get("title", ""),
                data.get("location", ""),
                data.get("date", ""),
                data.get("time", ""),
                "海報上傳成功"
            )
    except Exception as e:
        return "", "", "", "", f"海報上傳失敗：{str(e)}"

def add_activity(title, location, date, time):
    global progress_data
    if not all([title, location, date, time]):
        return "請填寫所有欄位", progress_data["activity"], gr.update(choices=progress_data["activity"]["title"].tolist())
    
    try:
        new_activity = pd.DataFrame([{
            "title": title,
            "location": location,
            "date": date,
            "time": time
        }])
        progress_data["activity"] = pd.concat([progress_data["activity"], new_activity], ignore_index=True)
        return (
            f"活動 '{title}' 已新增",
            progress_data["activity"],
            gr.update(choices=progress_data["activity"]["title"].tolist())
        )
    except Exception as e:
        return f"新增失敗：{str(e)}", progress_data["activity"], gr.update(choices=progress_data["activity"]["title"].tolist())

def edit_activity(activity_title, new_title, new_location, new_date, new_time):
    global progress_data
    if not activity_title:
        return "請選擇一個活動", progress_data["activity"], gr.update(choices=progress_data["activity"]["title"].tolist())
    
    try:
        idx = progress_data["activity"].index[progress_data["activity"]["title"] == activity_title].tolist()
        if not idx:
            return "活動不存在", progress_data["activity"], gr.update(choices=progress_data["activity"]["title"].tolist())
        
        idx = idx[0]
        progress_data["activity"].loc[idx, "title"] = new_title or progress_data["activity"].loc[idx, "title"]
        progress_data["activity"].loc[idx, "location"] = new_location or progress_data["activity"].loc[idx, "location"]
        progress_data["activity"].loc[idx, "date"] = new_date or progress_data["activity"].loc[idx, "date"]
        progress_data["activity"].loc[idx, "time"] = new_time or progress_data["activity"].loc[idx, "time"]
        return (
            f"活動 '{activity_title}' 已更新",
            progress_data["activity"],
            gr.update(choices=progress_data["activity"]["title"].tolist())
        )
    except Exception as e:
        return f"更新失敗：{str(e)}", progress_data["activity"], gr.update(choices=progress_data["activity"]["title"].tolist())

def delete_activity(activity_title):
    global progress_data
    if not activity_title:
        return "請選擇一個活動", progress_data["activity"], gr.update(choices=progress_data["activity"]["title"].tolist())
    
    try:
        progress_data["activity"] = progress_data["activity"][progress_data["activity"]["title"] != activity_title]
        return (
            f"活動 '{activity_title}' 已刪除",
            progress_data["activity"],
            gr.update(choices=progress_data["activity"]["title"].tolist())
        )
    except Exception as e:
        return f"刪除失敗：{str(e)}", progress_data["activity"], gr.update(choices=progress_data["activity"]["title"].tolist())