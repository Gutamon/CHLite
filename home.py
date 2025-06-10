import gradio as gr
import pandas as pd
import io
from data import progress_data

def upload_progress(file):
    global progress_data
    if not file:
        return "請選擇一個檔案", gr.update(visible=True), gr.update(visible=False), [], [], [], [], pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    
    try:
        # Read Excel file with multiple sheets
        xls = pd.ExcelFile(file, engine='openpyxl')
        sheets = xls.sheet_names
        
        # Validate required sheets
        required_sheets = ["classsheet", "assignment", "activity"]
        if not all(sheet in sheets for sheet in required_sheets):
            return f"檔案缺少必要的工作表：{', '.join(set(required_sheets) - set(sheets))}", gr.update(visible=True), gr.update(visible=False), [], [], [], [], pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
        
        # Load data
        progress_data["classsheet"] = pd.read_excel(xls, sheet_name="classsheet", dtype=str).fillna("")
        progress_data["assignment"] = pd.read_excel(xls, sheet_name="assignment", dtype=str).fillna("")
        progress_data["activity"] = pd.read_excel(xls, sheet_name="activity", dtype=str).fillna("")
        
        # Validate classsheet columns
        required_columns = ["name", "semester", "day", "type", "point"]
        if not all(col in progress_data["classsheet"].columns for col in required_columns):
            return "classsheet 缺少必要欄位", gr.update(visible=True), gr.update(visible=False), [], [], [], [], pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
        
        # Update dropdowns and displays
        course_choices = progress_data["classsheet"]["name"].tolist()
        assignment_choices = progress_data["assignment"]["title"].tolist()
        activity_choices = progress_data["activity"]["title"].tolist()
        
        return (
            "進度檔上傳成功",
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(choices=course_choices),
            gr.update(choices=assignment_choices),
            gr.update(choices=activity_choices),
            gr.update(choices=course_choices),
            progress_data["assignment"],
            progress_data["activity"],
            progress_data["classsheet"]
        )
    except Exception as e:
        return f"上傳失敗：{str(e)}", gr.update(visible=True), gr.update(visible=False), [], [], [], [], pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

def first_use():
    global progress_data
    # Initialize empty dataframes
    progress_data["classsheet"] = pd.DataFrame(columns=["name", "semester", "day", "type", "point"])
    progress_data["assignment"] = pd.DataFrame(columns=["title", "class", "deadline", "level"])
    progress_data["activity"] = pd.DataFrame(columns=["title", "location", "date", "time"])
    
    return (
        gr.update(visible=False),
        gr.update(visible=True),
        gr.update(choices=[]),
        gr.update(choices=[]),
        gr.update(choices=[]),
        gr.update(choices=[]),
        progress_data["assignment"],
        progress_data["activity"],
        progress_data["classsheet"]
    )