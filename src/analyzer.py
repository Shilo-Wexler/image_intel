def analyze(images_data: list[dict])->dict:
    total_images = len(images_data)
    images_with_gps = len([img for img in images_data if img.get("has_gps")])
    unique_cameras = list(set([img.get("camera_make") + " " + img.get("camera_model") for img in images_data if img.get("camera_make") and img.get("camera_model")]))
    dates = [img.get("datetime") for img in images_data if img.get("datetime")]
    if dates:
        date_range = {"start": min(dates) , "end": max(dates)} 
    else:
        date_range = {"start": None, "end": None}
    return {
        "total_images": total_images,
        "images_with_gps": images_with_gps,
        "unique_cameras": unique_cameras,
        "date_range": date_range,
        "insights": []
    }

