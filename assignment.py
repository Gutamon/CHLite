import gradio as gr
import pandas as pd
from data import progress_data

def add_assignment(title, course, deadline, priority):
    global progress_data
    if not all([title, course, deadline, priority]):
        return "請填寫所有欄位", progress_data["assignment"], gr.update(choices=progress_data["assignment"]["title"].tolist())
    
    try:
        # Convert priority to numeric value
        priority_map = {"⭐": "1.00", "⭐⭐": "2.00", "⭐⭐⭐": "3.00"}
        new_assignment = pd.DataFrame([{
            "title": title,
            "class": course,
            "deadline": deadline,
            "level": priority_map[priority]
        }])
        progress_data["assignment"] = pd.concat([progress_data["assignment"], new_assignment], ignore_index=True)
        return (
            f"作業 '{title}' 已新增",
            progress_data["assignment"],
            gr.update(choices=progress_data["assignment"]["title"].tolist())
        )
    except Exception as e:
        return f"新增失敗：{str(e)}", progress_data["assignment"], gr.update(choices=progress_data["assignment"]["title"].tolist())

def edit_assignment(assignment_title, new_title, new_deadline, new_priority):
    global progress_data
    if not assignment_title:
        return "請選擇一個作業", progress_data["assignment"], gr.update(choices=progress_data["assignment"]["title"].tolist())
    
    try:
        priority_map = {"⭐": "1.00", "⭐⭐": "2.00", "⭐⭐⭐": "3.00"}
        idx = progress_data["assignment"].index[progress_data["assignment"]["title"] == assignment_title].tolist()
        if not idx:
            return "作業不存在", progress_data["assignment"], gr.update(choices=progress_data["assignment"]["title"].tolist())
        
        idx = idx[0]
        progress_data["assignment"].loc[idx, "title"] = new_title or progress_data["assignment"].loc[idx, "title"]
        progress_data["assignment"].loc[idx, "deadline"] = new_deadline or progress_data["assignment"].loc[idx, "deadline"]
        progress_data["assignment"].loc[idx, "level"] = priority_map[new_priority] if new_priority else progress_data["assignment"].loc[idx, "level"]
        return (
            f"作業 '{assignment_title}' 已更新",
            progress_data["assignment"],
            gr.update(choices=progress_data["assignment"]["title"].tolist())
        )
    except Exception as e:
        return f"更新失敗：{str(e)}", progress_data["assignment"], gr.update(choices=progress_data["assignment"]["title"].tolist())

def delete_assignment(assignment_title):
    global progress_data
    if not assignment_title:
        return "請選擇一個作業", progress_data["assignment"], gr.update(choices=progress_data["assignment"]["title"].tolist())
    
    try:
        progress_data["assignment"] = progress_data["assignment"][progress_data["assignment"]["title"] != assignment_title]
        return (
            f"作業 '{assignment_title}' 已刪除",
            progress_data["assignment"],
            gr.update(choices=progress_data["assignment"]["title"].tolist())
        )
    except Exception as e:
        return f"刪除失敗：{str(e)}", progress_data["assignment"], gr.update(choices=progress_data["assignment"]["title"].tolist())