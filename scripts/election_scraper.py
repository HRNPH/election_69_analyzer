import requests
import time
import json
import os

# Configuration
# Note: Change timestamp part (2026-02-09-19-03-03-086) to fetch updated data
TIMESTAMP_VERSION = "2026-02-09-19-58-02-921"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://www.thaipbs.or.th/"
}

def fetch_json_data(endpoint_type, area_code):
    """
    Fetches JSON data for either 'mp' (constituency) or 'pl' (party-list).
    """
    if endpoint_type == "mp":
        url = f"https://election69-data.thaipbs.or.th/result-ect-unofficial-constituency/{TIMESTAMP_VERSION}/areas/AREA-{area_code}.json"
    else:  # pl(party-list)
        url = f"https://election69-data.thaipbs.or.th/result-ect-unofficial-party-list/{TIMESTAMP_VERSION}/areas/AREA-{area_code}.json"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        if response.status_code != 200:
            return None
            
        response.raise_for_status()
        data = response.json()
        return data.get("entries", [])
            
    except Exception as e:
        print(f"Error fetching {endpoint_type.upper()} for Area {area_code}: {e}")
        return "ERROR"

def save_to_json(data_type, area_code, entries):
    """
    Saves entries inside an object wrapper to data/{data_type}/{area_code}.json
    """
    directory = f"data/{data_type}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    filepath = os.path.join(directory, f"{area_code}.json")
    
    # WRAPPER: Wrap the list in a dictionary {}
    data_to_save = {
        "area_code": area_code,
        "entries": entries
    }
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Failed to save {data_type.upper()} for Area {area_code}: {e}")
        return False

def main():
    start_code = 1001
    max_code = 9999
    
    mp_success = 0
    pl_success = 0
    current_code = start_code
    
    while current_code <= max_code:
        # 1. Fetch MP Data (Primary check for valid area codes)
        mp_entries = fetch_json_data("mp", current_code)
        
        if mp_entries is None:
            # Skip logic: if response is 403(no more data in this province), go to next XX01 block
            next_block = ((current_code // 100) + 1) * 100 + 1
            print(f"  Area {current_code} is invalid. Skipping to block: {next_block}")
            current_code = next_block
            continue
            
        if mp_entries != "ERROR":
            if save_to_json("mp", current_code, mp_entries):
                mp_success += 1

        # 2. Fetch Party List (PL) Data
        pl_entries = fetch_json_data("pl", current_code)
        
        if pl_entries != "ERROR":
            if save_to_json("pl", current_code, pl_entries):
                pl_success += 1
                
        print(f"Saved MP & PL data for {current_code}")
        
        current_code += 1
        # Small delay between areas
        time.sleep(0.1)
    
    print("\n--- Download Complete ---")
    print(f"Total MP Files Saved: {mp_success}")
    print(f"Total PL Files Saved: {pl_success}")

if __name__ == "__main__":
    main()
