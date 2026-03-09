import os
from src.extractor import extract_all
from src.analyzer import analyze
from src.map_view import create_map
from src.report import create_report


def run_test(target_folder="/Users/shilovaksler/Desktop/image_intel/images/"):
    print(f"--- Starting Test for folder: {target_folder} ---")

    if not os.path.exists(target_folder):
        print(f"Error: Folder '{target_folder}' not found.")
        return

    raw_data = extract_all(target_folder)
    print(f"Extracted data from {len(raw_data)} images.")

    if not raw_data:
        print("No data found. Exiting.")
        return

    analysis_results = analyze(raw_data)
    print("Analysis complete.")

    map_html = create_map(raw_data)
    print("Interactive map generated.")

    timeline_placeholder = "<div style='text-align:center; padding:20px; color:#64748b;'>ציר זמן ויזואלי - בקרוב</div>"

    final_report = create_report(
        images_data=raw_data,
        map_html=map_html,
        timeline_html=timeline_placeholder,
        analysis=analysis_results
    )

    output_file = "test_report.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_report)

    print(f"--- Success! Report saved to: {os.path.abspath(output_file)} ---")


if __name__ == "__main__":
    run_test()
