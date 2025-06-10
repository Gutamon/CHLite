import gradio as gr
import pandas as pd
import requests
import os
from data import progress_data

def upload_class_excel(file):
    global progress_data
    if not file:
        return "請選擇一個檔案", progress_data["classsheet"], gr.update(choices=progress_data["classsheet"]["name"].tolist()), gr.update(choices=progress_data["classsheet"]["name"].tolist())
    
    try:
        file_extension = os.path.splitext(file)[1].lower()
        if file_extension == '.csv':
            df = pd.read_csv(file, dtype=str, encoding='utf-8').fillna("")
        elif file_extension in ['.xls', '.xlsx']:
            df = pd.read_excel(file, engine='openpyxl', dtype=str).fillna("")
        else:
            return f"不支援的檔案格式：{file_extension}", progress_data["classsheet"], gr.update(choices=progress_data["classsheet"]["name"].tolist()), gr.update(choices=progress_data["classsheet"]["name"].tolist())
        
        required_columns = ["name", "semester", "day", "type", "point"]
        if not all(col in df.columns for col in required_columns):
            return f"檔案缺少必要欄位：{', '.join(set(required_columns) - set(df.columns))}", progress_data["classsheet"], gr.update(choices=progress_data["classsheet"]["name"].tolist()), gr.update(choices=progress_data["classsheet"]["name"].tolist())
        
        progress_data["classsheet"] = pd.concat([progress_data["classsheet"], df], ignore_index=True)
        return (
            "課程檔案上傳成功",
            progress_data["classsheet"],
            gr.update(choices=progress_data["classsheet"]["name"].tolist()),  # 更新 class_dropdown
            gr.update(choices=progress_data["classsheet"]["name"].tolist())   # 更新 course_dropdown
        )
    except Exception as e:
        return f"上傳失敗：{str(e)}", progress_data["classsheet"], gr.update(choices=progress_data["classsheet"]["name"].tolist()), gr.update(choices=progress_data["classsheet"]["name"].tolist())

def upload_class_image(file):
    global progress_data
    if not file:
        return "請選擇一張圖片", progress_data["classsheet"], gr.update(choices=progress_data["classsheet"]["name"].tolist()), gr.update(choices=progress_data["classsheet"]["name"].tolist())
    
    try:
        webhook_url = "https://hook.us2.make.com/nsfi68dd6e3k9srf4nz01budh22arsqx"
        with open(file, "rb") as f:
            files = {"file": f}
            response = requests.post(webhook_url, files=files)
            response.raise_for_status()
            data = response.json()
            
            required_keys = ["name", "semester", "day", "type", "point"]
            if not all(key in data for key in required_keys):
                return "圖片處理結果缺少必要欄位", progress_data["classsheet"], gr.update(choices=progress_data["classsheet"]["name"].tolist()), gr.update(choices=progress_data["classsheet"]["name"].tolist())
            
            new_classes = pd.DataFrame({
                "name": data["name"],
                "semester": data["semester"],
                "day": data["day"],
                "type": data["type"],
                "point": data["point"]
            })
            progress_data["classsheet"] = pd.concat([progress_data["classsheet"], new_classes], ignore_index=True)
            return (
                "課程圖片上傳成功",
                progress_data["classsheet"],
                gr.update(choices=progress_data["classsheet"]["name"].tolist()),  # 更新 class_dropdown
                gr.update(choices=progress_data["classsheet"]["name"].tolist())   # 更新 course_dropdown
            )
    except Exception as e:
        return f"圖片上傳失敗：{str(e)}", progress_data["classsheet"], gr.update(choices=progress_data["classsheet"]["name"].tolist()), gr.update(choices=progress_data["classsheet"]["name"].tolist())

def edit_class(class_name, new_name, new_semester, new_day, new_type, new_point):
    global progress_data
    if not class_name:
        return "請選擇一個課程", progress_data["classsheet"], gr.update(choices=progress_data["classsheet"]["name"].tolist())
    
    try:
        idx = progress_data["classsheet"].index[progress_data["classsheet"]["name"] == class_name].tolist()
        if not idx:
            return "課程不存在", progress_data["classsheet"], gr.update(choices=progress_data["classsheet"]["name"].tolist())
        
        idx = idx[0]
        progress_data["classsheet"].loc[idx, "name"] = new_name or progress_data["classsheet"].loc[idx, "name"]
        progress_data["classsheet"].loc[idx, "semester"] = new_semester or progress_data["classsheet"].loc[idx, "semester"]
        progress_data["classsheet"].loc[idx, "day"] = new_day or progress_data["classsheet"].loc[idx, "day"]
        progress_data["classsheet"].loc[idx, "type"] = new_type or progress_data["classsheet"].loc[idx, "type"]
        progress_data["classsheet"].loc[idx, "point"] = new_point or progress_data["classsheet"].loc[idx, "point"]
        return (
            f"課程 '{class_name}' 已更新",
            progress_data["classsheet"],
            gr.update(choices=progress_data["classsheet"]["name"].tolist())
        )
    except Exception as e:
        return f"更新失敗：{str(e)}", progress_data["classsheet"], gr.update(choices=progress_data["classsheet"]["name"].tolist())

def delete_class(class_name):
    global progress_data
    if not class_name:
        return "請選擇一個課程", progress_data["classsheet"], gr.update(choices=progress_data["classsheet"]["name"].tolist())
    
    try:
        progress_data["classsheet"] = progress_data["classsheet"][progress_data["classsheet"]["name"] != class_name]
        return (
            f"課程 '{class_name}' 已刪除",
            progress_data["classsheet"],
            gr.update(choices=progress_data["classsheet"]["name"].tolist())
        )
    except Exception as e:
        return f"刪除失敗：{str(e)}", progress_data["classsheet"], gr.update(choices=progress_data["classsheet"]["name"].tolist())