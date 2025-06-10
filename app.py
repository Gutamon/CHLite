import gradio as gr
import pandas as pd
import io
import os
import requests
import json
import tempfile
from datetime import datetime
from data import progress_data
from home import upload_progress, first_use
from assignment import add_assignment, edit_assignment, delete_assignment
from activity import upload_poster, add_activity, edit_activity, delete_activity
from classsheet import upload_class_excel, upload_class_image, edit_class, delete_class

# 初始化時載入預設進度檔（如果存在）
default_progress_file = "CHLite_Progress.xlsx"
if os.path.exists(default_progress_file):
    msg, span1_update, span2_update, course_choices, assignment_choices, activity_choices, class_choices, assignment_df, activity_df, class_df = upload_progress(default_progress_file)
    progress_data["classsheet"] = class_df
    progress_data["assignment"] = assignment_df
    progress_data["activity"] = activity_df
else:
    course_choices, assignment_choices, activity_choices, class_choices = [], [], [], []



with gr.Blocks() as demo:
    gr.Markdown("## CHLite, Your Course Helper is Lite")
    span1 = gr.Group(visible=True)
    span2 = gr.Group(visible=False)
    
    with span1:
        progress_file = gr.File(label="你的進度檔", file_types=[".csv", ".xls", ".xlsx"])
        with gr.Row():
            upload_progress_btn = gr.Button("上傳進度檔")
            first_use_btn = gr.Button("初次使用")
        home_msg = gr.Textbox(label="系統訊息", interactive=False)
    
    with span2:
        with gr.Row():
            assignment_display = gr.Dataframe(label="📌 作業清單", value=progress_data["assignment"])
            activity_display = gr.Dataframe(label="📌 活動清單", value=progress_data["activity"])
            
        with gr.Tabs():                      
            with gr.Tab("作業"):
                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### 新增作業")
                        title_input = gr.Textbox(label="作業標題")
                        course_dropdown = gr.Dropdown(label="課程選擇", choices=course_choices, allow_custom_value=True)
                        deadline_input = gr.Textbox(label="截止日（yyyy-mm-dd）")
                        priority_input = gr.Radio(choices=["⭐", "⭐⭐", "⭐⭐⭐"], label="重要度")
                        add_btn = gr.Button("新增作業")
                    with gr.Column(scale=1):
                        gr.Markdown("### 編輯/刪除作業")
                        assignment_dropdown = gr.Dropdown(label="選擇作業", choices=[], allow_custom_value=True)
                        edit_title_input = gr.Textbox(label="新作業標題")
                        edit_deadline_input = gr.Textbox(label="新截止日（yyyy-mm-dd）")
                        edit_priority_input = gr.Radio(choices=["⭐", "⭐⭐", "⭐⭐⭐"], label="新重要度")
                        with gr.Row():
                            edit_btn = gr.Button("編輯作業")
                            delete_btn = gr.Button("刪除作業")
                add_msg = gr.Textbox(label="操作訊息", interactive=False)
                
            with gr.Tab("活動"):
                gr.Markdown("### 新增活動")
                with gr.Row():
                    with gr.Column(scale=1):
                        file_input = gr.Image(label="上傳活動海報", type="filepath", height=300)
                        upload_poster_btn = gr.Button("上傳海報")
                    with gr.Column(scale=1):
                        act_title_input = gr.Textbox(label="活動標題", interactive=True)
                        act_location_input = gr.Textbox(label="地點", interactive=True)
                        act_date_input = gr.Textbox(label="日期（yyyy-mm-dd）", interactive=True)
                        act_time_input = gr.Textbox(label="時間", interactive=True)
                        submit_btn = gr.Button("新增活動")
                gr.Markdown("### 編輯/刪除活動")
                activity_dropdown = gr.Dropdown(label="選擇活動", choices=[], allow_custom_value=True)
                edit_act_title_input = gr.Textbox(label="新活動標題")
                edit_act_location_input = gr.Textbox(label="新地點")
                edit_act_date_input = gr.Textbox(label="新日期（yyyy-mm-dd）")
                edit_act_time_input = gr.Textbox(label="新時間")
                with gr.Row():
                    edit_activity_btn = gr.Button("編輯活動")
                    delete_activity_btn = gr.Button("刪除活動")
                result_output = gr.Textbox(label="回應結果")
                
            with gr.Tab("課表"):
                with gr.Row():
                    with gr.Column(scale=1):
                        class_display = gr.Dataframe(label="📌 課表紀錄", value=progress_data["classsheet"])
                    with gr.Column(scale=2):
                        with gr.Row():
                            with gr.Column(scale=1):
                                gr.Markdown("### 用Excel上傳課表")
                                course_file_csv = gr.File(label="上傳Excel", file_types=[".csv", ".xls", ".xlsx"])
                                upload_class_btn_excel = gr.Button("載入課程")
                            with gr.Column(scale=1):
                                gr.Markdown("### 用圖片上傳課表")
                                course_file_img = gr.File(label="上傳圖片", file_types=[".png", ".jpg", ".jpeg"])
                                upload_class_btn_img = gr.Button("載入課程")
                        upload_class_msg = gr.Textbox(label="偵測到的結果", interactive=False)
                
                gr.Markdown("### 編輯/刪除課程")
                class_dropdown = gr.Dropdown(label="選擇課程", choices=[], allow_custom_value=True)
                edit_class_name_input = gr.Textbox(label="新課程名稱")
                edit_class_semester_input = gr.Textbox(label="新課程學期(0-0)")
                edit_class_day_input = gr.Textbox(label="新課程日")
                edit_class_type_input = gr.Textbox(label="新課程類型(必、選)")
                edit_class_point_input = gr.Textbox(label="新課程學分")
                with gr.Row():
                    edit_class_btn = gr.Button("編輯課程")
                    delete_class_btn = gr.Button("刪除課程")
        
        download_btn = gr.DownloadButton(label="匯出記錄檔", value="CHLite_Progress.xlsx")
        
    # Helper function to update dropdown choices
    def update_dropdowns():
        course_choices = progress_data["classsheet"]["name"].tolist()
        assignment_choices = progress_data["assignment"]["title"].tolist()
        activity_choices = progress_data["activity"]["title"].tolist()
        return (
            gr.update(choices=course_choices),  # 更新 course_dropdown
            gr.update(choices=assignment_choices),  # 更新 assignment_dropdown
            gr.update(choices=activity_choices),  # 更新 activity_dropdown
            gr.update(choices=course_choices)  # 更新 class_dropdown
        )
    
    # Helper function to export progress file
    def export_progress():
        try:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                classsheet_clean = progress_data["classsheet"].fillna("").astype(str)
                assignment_clean = progress_data["assignment"].fillna("").astype(str)
                activity_clean = progress_data["activity"].fillna("").astype(str)
                
                classsheet_clean.to_excel(writer, sheet_name="classsheet", index=False)
                assignment_clean.to_excel(writer, sheet_name="assignment", index=False)
                activity_clean.to_excel(writer, sheet_name="activity", index=False)
            
            with open("test_output.xlsx", "wb") as f:
                f.write(output.getvalue())
            
            output.seek(0)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                tmp_file.write(output.read())
                tmp_file_path = tmp_file.name
            
            return (
                tmp_file_path,
                gr.update(visible=True),
                gr.update(visible=False)
            )
        except Exception as e:
            print(f"匯出失敗：{str(e)}")
            return None, gr.update(visible=True), gr.update(visible=False)
    
    # Event handlers
    # 更新 upload_class_btn_excel 的事件處理器
    upload_class_btn_excel.click(
        fn=upload_class_excel,
        inputs=course_file_csv,
        outputs=[upload_class_msg, class_display, class_dropdown, course_dropdown]
    )

    # 更新 upload_class_btn_img 的事件處理器
    upload_class_btn_img.click(
        fn=upload_class_image,
        inputs=course_file_img,
        outputs=[upload_class_msg, class_display, class_dropdown, course_dropdown]  # 添加 course_dropdown
    )
    
    upload_progress_btn.click(
        fn=upload_progress,
        inputs=progress_file,
        outputs=[home_msg, span1, span2, course_dropdown, assignment_dropdown, activity_dropdown, class_dropdown, assignment_display, activity_display, class_display]
    )
    first_use_btn.click(
        fn=first_use,
        outputs=[span1, span2, course_dropdown, assignment_dropdown, activity_dropdown, class_dropdown, assignment_display, activity_display, class_display]
    )
    add_btn.click(
        fn=add_assignment,
        inputs=[title_input, course_dropdown, deadline_input, priority_input],
        outputs=[add_msg, assignment_display, assignment_dropdown]
    )
    edit_btn.click(
        fn=edit_assignment,
        inputs=[assignment_dropdown, edit_title_input, edit_deadline_input, edit_priority_input],
        outputs=[add_msg, assignment_display, assignment_dropdown]
    )
    delete_btn.click(
        fn=delete_assignment,
        inputs=assignment_dropdown,
        outputs=[add_msg, assignment_display, assignment_dropdown]
    )
    upload_poster_btn.click(
        fn=upload_poster,
        inputs=file_input,
        outputs=[act_title_input, act_location_input, act_date_input, act_time_input, result_output]
    )
    submit_btn.click(
        fn=add_activity,
        inputs=[act_title_input, act_location_input, act_date_input, act_time_input],
        outputs=[result_output, activity_display, activity_dropdown]
    )
    edit_activity_btn.click(
        fn=edit_activity,
        inputs=[activity_dropdown, edit_act_title_input, edit_act_location_input, edit_act_date_input, edit_act_time_input],
        outputs=[result_output, activity_display, activity_dropdown]
    )
    delete_activity_btn.click(
        fn=delete_activity,
        inputs=activity_dropdown,
        outputs=[result_output, activity_display, activity_dropdown]
    )

    edit_class_btn.click(
        fn=edit_class,
        inputs=[class_dropdown, edit_class_name_input, edit_class_semester_input, edit_class_day_input, edit_class_type_input, edit_class_point_input],
        outputs=[upload_class_msg, class_display, class_dropdown]
    )
    delete_class_btn.click(
        fn=delete_class,
        inputs=class_dropdown,
        outputs=[upload_class_msg, class_display, class_dropdown]
    )
    download_btn.click(
        fn=export_progress,
        outputs=[download_btn, span1, span2]
    )

demo.launch()