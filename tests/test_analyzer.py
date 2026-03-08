
import sys
import os

# השורה הזו מוסיפה את תיקיית הפרויקט לנתיב של פייתון
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# עכשיו פייתון יודע לחפש בתוך src
from src.analyzer import analyze 



def test_basic_analysis():
    fake_data = [
        {"camera_make": "Samsung", "camera_model": "S23", "has_gps": True, "datetime": "2025:01:12 08:30:00"},
        {"camera_make": "Samsung", "camera_model": "S23", "has_gps": False, "datetime": "2025:01:12 09:00:00"},
        {"camera_make": "Apple", "camera_model": "iPhone 15", "has_gps": True, "datetime": "2025:01:13 10:00:00"},
        {"camera_make": None, "camera_model": None, "has_gps": False, "datetime": None}
    ]

    results = analyze(fake_data)

    # כאן היה הכשל - שנה ל-4
    assert results["total_images"] == 4, f"Expected 4 images, got {results['total_images']}"
    assert results["images_with_gps"] == 2
    assert len(results["unique_cameras"]) == 2 # המכשיר הרביעי מסונן כי הוא None
    
    print("✅ All assertions passed with null values handling!")
    print(results)

test_basic_analysis()
