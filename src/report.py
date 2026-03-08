def create_report(images_data: list[dict], map_html: str,
                  timeline_html: str, analysis: dict) -> str:
    table_rows = ""
    for img in images_data:
        status_tag = '<span class="tag-gps">GPS</span>' if img['has_gps'] else '<span class="tag-no">NO GPS</span>'
        table_rows += f"""
            <tr>
                <td class="file-name">{img['filename']}</td>
                <td class="date-col">{img['datetime']}</td>
                <td class="status-col">{status_tag}</td>
            </tr>
        """

    full_html = f"""
    <!DOCTYPE html>
    <html lang="he" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

            body {{ 
                margin: 0; padding: 40px; 
                font-family: 'Inter', sans-serif; 
                background-color: #f8fafc; color: #0f172a;
                line-height: 1.6;
            }}

            .container {{ max-width: 1100px; margin: auto; }}

            /* Header Section */
            header {{ 
                display: flex; justify-content: space-between; align-items: center;
                margin-bottom: 48px; 
            }}

            h1 {{ font-weight: 700; font-size: 30px; margin: 0; color: #1e293b; letter-spacing: -0.5px; }}
            .badge {{ background: #e2e8f0; color: #475569; padding: 4px 12px; border-radius: 99px; font-size: 12px; font-weight: 500; }}

            /* Stats Cards */
            .stats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-bottom: 48px; }}
            .card {{ 
                background: white; border: 1px solid #e2e8f0; border-radius: 12px; 
                padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); 
            }}
            .card-label {{ font-size: 13px; font-weight: 500; color: #64748b; margin-bottom: 8px; }}
            .card-value {{ font-size: 28px; font-weight: 700; color: #0f172a; }}

            /* Visual Content Section */
            .section-title {{ font-size: 16px; font-weight: 600; margin-bottom: 16px; color: #334155; }}
            .visual-frame {{ 
                background: white; border: 1px solid #e2e8f0; border-radius: 12px;
                height: 500px; margin-bottom: 48px; overflow: hidden;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            }}

            /* Modern Table */
            .table-container {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; }}
            table {{ width: 100%; border-collapse: collapse; text-align: right; }}
            th {{ background: #f8fafc; padding: 16px; font-size: 12px; font-weight: 600; color: #64748b; border-bottom: 1px solid #e2e8f0; }}
            td {{ padding: 16px; border-bottom: 1px solid #f1f5f9; font-size: 14px; }}
            .file-name {{ font-weight: 500; color: #1e293b; }}
            .date-col {{ color: #64748b; }}

            /* Tags */
            .tag-gps {{ background: #dcfce7; color: #166534; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; }}
            .tag-no {{ background: #f1f5f9; color: #475569; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>סקירת נתונים ויזואלית</h1>
                <span class="badge">V 4.2.0 - ACTIVE</span>
            </header>

            <div class="stats-grid">
                <div class="card">
                    <div class="card-label">סה"כ קבצים</div>
                    <div class="card-value">{len(images_data)}</div>
                </div>
                <div class="card">
                    <div class="card-label">נקודות GPS</div>
                    <div class="card-value" style="color: #2563eb;">{analysis.get('gps_count', '0')}</div>
                </div>
                <div class="card">
                    <div class="card-label">סטטוס סריקה</div>
                    <div class="card-value" style="color: #059669;">הושלם</div>
                </div>
            </div>

            <div class="section-title">פריסה גיאוגרפית</div>
            <div class="visual-frame">
                {map_html}
            </div>

            <div class="section-title">ציר זמן</div>
            <div class="visual-frame" style="height: auto; padding: 20px;">
                {timeline_html}
            </div>

            <div class="section-title">פירוט קבצים מלא</div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>מזהה קובץ</th>
                            <th>חותם זמן</th>
                            <th>נתוני מיקום</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    """
    return full_html
