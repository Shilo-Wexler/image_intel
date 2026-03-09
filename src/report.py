def create_report(images_data: list[dict], map_html: str,
                  timeline_html: str, analysis: dict) -> str:
    insights_html = ""
    for insight in analysis.get('insights', []):
        insights_html += f'<div style="font-size: 14px; margin-bottom: 8px; color: #475569;">• {insight}</div>'

    table_rows = ""
    for img in images_data:
        status_tag = '<span class="tag-gps">GPS</span>' if img.get('has_gps') else '<span class="tag-no">NO GPS</span>'

        table_rows += f"""
            <tr>
                <td class="file-name">
                    <details>
                        <summary style="cursor: pointer; outline: none; color: #2563eb; font-weight: 500;">{img['filename']}</summary>
                        <div style="font-size: 12px; color: #64748b; background: #f8fafc; padding: 10px; border-radius: 6px; margin-top: 5px; border: 1px solid #e2e8f0;">
                            <b>מכשיר:</b> {img.get('camera_make', '')} {img.get('camera_model', '')}<br>
                            <b>נתיב:</b> {img.get('path', 'N/A')}
                        </div>
                    </details>
                </td>
                <td class="date-col">{img.get('datetime', 'N/A')}</td>
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
            body {{ margin: 0; padding: 40px; font-family: 'Inter', sans-serif; background-color: #f8fafc; color: #0f172a; direction: rtl; }}
            .container {{ max-width: 1100px; margin: auto; }}
            header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; }}
            h1 {{ font-weight: 700; font-size: 28px; margin: 0; color: #1e293b; }}

            .stats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 40px; }}
            .card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
            .card-label {{ font-size: 12px; font-weight: 600; color: #64748b; text-transform: uppercase; margin-bottom: 8px; }}
            .card-value {{ font-size: 24px; font-weight: 700; color: #0f172a; }}

            .section-title {{ font-size: 16px; font-weight: 600; margin-bottom: 16px; color: #334155; border-right: 4px solid #2563eb; padding-right: 12px; }}

            /* תיקון קריטי להצגת המפה */
            .visual-frame {{ 
                background: white; 
                border: 1px solid #e2e8f0; 
                border-radius: 12px; 
                height: 500px; 
                margin-bottom: 40px; 
                position: relative;
                overflow: hidden;
            }}

            /* מוודא שה-iframe של folium ימלא את כל המסגרת */
            .visual-frame iframe {{
                width: 100% !important;
                height: 100% !important;
                border: none !important;
            }}

            .table-container {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; }}
            table {{ width: 100%; border-collapse: collapse; text-align: right; }}
            th {{ background: #f8fafc; padding: 14px; font-size: 12px; font-weight: 600; color: #64748b; border-bottom: 1px solid #e2e8f0; }}
            td {{ padding: 14px; border-bottom: 1px solid #f1f5f9; font-size: 14px; }}

            .tag-gps {{ background: #dcfce7; color: #166534; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; }}
            .tag-no {{ background: #f1f5f9; color: #475569; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>דו"ח מודיעין תמונות</h1>
                <div style="text-align: left;">
                    <div style="font-size: 12px; color: #64748b;">טווח פעילות:</div>
                    <div style="font-size: 14px; font-weight: 600;">{analysis.get('date_range', {}).get('start', 'N/A')} - {analysis.get('date_range', {}).get('end', 'N/A')}</div>
                </div>
            </header>

            <div class="stats-grid">
                <div class="card">
                    <div class="card-label">סה"כ קבצים</div>
                    <div class="card-value">{analysis.get('total_images', 0)}</div>
                </div>
                <div class="card">
                    <div class="card-label">קבצים עם מיקום</div>
                    <div class="card-value" style="color: #2563eb;">{analysis.get('images_with_gps', 0)}</div>
                </div>
                <div class="card">
                    <div class="card-label">סטטוס ניתוח</div>
                    <div style="font-size: 14px; font-weight: 600; color: #059669; margin-top: 5px;">{analysis.get('top_insight', 'הושלם')}</div>
                </div>
            </div>

            <div class="section-title">תובנות מפתח</div>
            <div class="card" style="margin-bottom: 40px;">
                {insights_html if insights_html else "לא זוהו חריגות משמעותיות."}
            </div>

            <div class="section-title">פריסה גיאוגרפית</div>
            <div class="visual-frame">
                {map_html}
            </div>

            <div class="section-title">פירוט נכסים מלא</div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>שם קובץ (לחץ למידע נוסף)</th>
                            <th>זמן צילום</th>
                            <th>סטטוס GPS</th>
                        </tr>
                    </thead>
                    <tbody>{table_rows}</tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    """
    return full_html
