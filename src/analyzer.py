from datetime import datetime


def analyze(images_data: list[dict]) -> dict:
    if not images_data:
        return {
            "total_images": 0,
            "images_with_gps": 0,
            "unique_cameras": [],
            "date_range": {"start": None, "end": None},
            "insights": []
        }

    total_images = len(images_data)
    images_with_gps = len([img for img in images_data if img.get("has_gps")])

    cameras = set()
    for img in images_data:
        make = img.get("camera_make") or "Unknown"
        model = img.get("camera_model") or "Device"
        cameras.add(f"{make} {model}")
    unique_cameras = sorted(list(cameras))

    dates = []
    sorted_images = []
    for img in images_data:
        dt_str = img.get("datetime")
        if dt_str:
            try:
                dt_obj = datetime.strptime(dt_str, "%Y:%m:%d %H:%M:%S")
                dates.append(dt_obj)
                img_copy = img.copy()
                img_copy['dt_obj'] = dt_obj
                sorted_images.append(img_copy)
            except (ValueError, TypeError):
                continue

    sorted_images.sort(key=lambda x: x['dt_obj'])

    device_replacement_date = None
    if len(unique_cameras) > 1 and sorted_images:
        first_device = f"{sorted_images[0].get('camera_make')} {sorted_images[0].get('camera_model')}"
        for img in sorted_images:
            current_device = f"{img.get('camera_make')} {img.get('camera_model')}"
            if current_device != first_device:
                device_replacement_date = img['dt_obj'].strftime("%d/%m/%Y")
                break

    if dates:
        date_range = {
            "start": min(dates).strftime("%d/%m/%Y"),
            "end": max(dates).strftime("%d/%m/%Y")
        }
    else:
        date_range = {"start": None, "end": None}

    insights = []
    insights.append(f"זוהו {len(unique_cameras)} מכשירים שונים במאגר.")

    if device_replacement_date:
        insights.append(f"זוהתה החלפת מכשיר סביב תאריך {device_replacement_date}.")

    if total_images > 0 and (images_with_gps / total_images) > 0.9:
        insights.append("רמת כיסוי GPS גבוהה מאוד.")

    if len(unique_cameras) == 1:
        insights.append(f"כל התמונות צולמו במכשיר יחיד ({unique_cameras[0]}).")

    return {
        "total_images": total_images,
        "images_with_gps": images_with_gps,
        "unique_cameras": unique_cameras,
        "date_range": date_range,
        "top_insight": insights[1] if len(insights) > 1 else insights[0],
        "insights": insights
    }
