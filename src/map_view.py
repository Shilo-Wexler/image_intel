"""
map_view.py - יצירת מפה אינטראקטיבית
צוות 1, זוג B

ראו docs/api_contract.md לפורמט הקלט והפלט.

=== תיקונים ===
1. חישוב מרכז המפה - היה עובר על images_data (כולל תמונות בלי GPS) במקום gps_image, נופל עם None
2. הסרת CustomIcon שלא עובד (filename זה לא נתיב שהדפדפן מכיר)
3. הסרת m.save() - לפי API contract צריך להחזיר HTML string, לא לשמור קובץ
4. הסרת fake_data מגוף הקובץ - הועבר ל-if __name__
5. תיקון color_index - היה מתקדם על כל תמונה במקום רק על מכשיר חדש
6. הוספת מקרא מכשירים
"""

import folium
from datetime import datetime
import itertools


def sort_by_time(arr):
    def get_date(x):
        dt_str = x.get("datetime")
        if not dt_str:
            return datetime.min
        try:
            return datetime.strptime(dt_str, "%Y:%m:%d %H:%M:%S")
        except:
            return datetime.min

    return sorted(arr, key=get_date)


def create_map(images_data):
    """
    יוצר מפה אינטראקטיבית עם כל המיקומים.

    Args:
        images_data: רשימת מילונים מ-extract_all

    Returns:
        string של HTML (המפה)
    """
    gps_images = [img for img in images_data if img.get("has_gps") and img.get("latitude") and img.get("longitude")]

    if not gps_images:
        return "<div style='text-align:center; padding:50px; font-family:sans-serif;'>No GPS data available</div>"

    gps_images = sort_by_time(gps_images)

    colors = ['#E63946', '#457B9D', '#2A9D8F', '#F4A261', '#6D597A', '#7209B7']
    color_cycle = itertools.cycle(colors)
    device_colors = {}

    center_lat = sum(img["latitude"] for img in gps_images) / len(gps_images)
    center_lon = sum(img["longitude"] for img in gps_images) / len(gps_images)

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=10,
        tiles='OpenStreetMap',
        control_scale=True
    )

    for img in gps_images:
        device = f"{img.get('camera_make', '')} {img.get('camera_model', '')}"
        if device not in device_colors:
            device_colors[device] = next(color_cycle)

        current_color = device_colors[device]

        info_html = f"""
            <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; direction: rtl; text-align: right; min-width: 200px; padding: 5px;">
                <b style="color: {current_color}; font-size: 15px; border-bottom: 2px solid {current_color}; padding-bottom: 3px;">{img.get('filename', 'Unknown')}</b>
                <div style="margin-top: 10px; font-size: 13px; color: #333;">
                    <b>תאריך:</b> {img.get('datetime', 'N/A')}<br>
                    <b>מכשיר:</b> <span style="color: {current_color}; font-weight: bold;">{device}</span><br>
                    <hr style="border: 0; border-top: 1px solid #eee; margin: 8px 0;">
                    <small style="color: #666;">נתיב: {img.get('path', 'N/A')}</small>
                </div>
            </div>
        """

        folium.CircleMarker(
            location=[img["latitude"], img["longitude"]],
            radius=9,
            popup=folium.Popup(info_html, max_width=300),
            color='white',  # מסגרת לבנה שתבליט את הנקודה
            weight=2,
            fill=True,
            fill_color=current_color,
            fill_opacity=0.85
        ).add_to(m)

    return m._repr_html_()



if __name__ == "__main__":
    # תיקון: fake_data הועבר לכאן מגוף הקובץ - כדי שלא ירוץ בכל import
    fake_data = [
        {"filename": "test1.jpg", "latitude": 32.0853, "longitude": 34.7818,
         "has_gps": True, "camera_make": "Samsung", "camera_model": "Galaxy S23",
         "datetime": "2025-01-12 08:30:00"},
        {"filename": "test2.jpg", "latitude": 31.7683, "longitude": 35.2137,
         "has_gps": True, "camera_make": "Apple", "camera_model": "iPhone 15 Pro",
         "datetime": "2025-01-13 09:00:00"},
    ]
    html = create_map(fake_data)
    with open("test_map.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Map saved to test_map.html")



