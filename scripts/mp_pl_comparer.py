import os
import json
from datetime import datetime, timezone

def compare_mp_and_pl(export_json=False):
    """
    Compares the winning MP candidate number with the top 8 Party List party numbers.
    If export_json is True, also exports results to docs/data/results.json.
    """
    mp_dir = "data/mp"
    pl_dir = "data/pl"
    
    if not os.path.exists(mp_dir) or not os.path.exists(pl_dir):
        print("Error: data/mp or data/pl directory not found.")
        return

    mp_files = sorted([f for f in os.listdir(mp_dir) if f.endswith(".json")])
    
    print(f"{'Area':<6} | {'MP Num':<6} | {'MP Party':<10} | {'Status':<30}")
    print("-" * 50)

    all_matches = []
    all_rows = []

    for filename in mp_files:
        area_code = filename.replace(".json", "")
        mp_path = os.path.join(mp_dir, filename)
        pl_path = os.path.join(pl_dir, filename)
        
        if not os.path.exists(pl_path):
            continue

        try:
            # 1. Get MP winning info
            with open(mp_path, "r", encoding="utf-8") as f:
                mp_data = json.load(f)
            
            mp_entries = mp_data.get("entries", [])
            if not mp_entries:
                continue
                
            top_mp = mp_entries[0]
            winning_candidate = top_mp.get("candidateCode", "")
            mp_party = top_mp.get("partyCode", "Unknown") # Get party of the MP
            
            # Extraction logic: CANDIDATE-MP-100105 -> 05
            prefix = f"CANDIDATE-MP-{area_code}"
            mp_number = winning_candidate[len(prefix):] if winning_candidate.startswith(prefix) else None
            
            if not mp_number:
                continue

            # 2. Get Top 7 Party List data
            with open(pl_path, "r", encoding="utf-8") as f:
                pl_data = json.load(f)
                
            pl_entries = pl_data.get("entries", [])[:7] # Get rank 1 to 7
            
            matches = []
            for pl_entry in pl_entries:
                pl_party_code = pl_entry.get("partyCode", "")
                last_2 = pl_party_code[-2:]
                
                # Logic: Skip if party number is "6" or "9"
                # "6" is United Thai Nation Party
                # "9" is Pheu Thai Party
                if last_2 in ["06", "09"]:
                    continue
                
                # Compare
                if last_2 == mp_number:
                    match_info = {
                        "area": area_code,
                        "mp_number": mp_number,
                        "mp_party": mp_party,
                        "pl_rank": pl_entry.get('rank'),
                        "pl_party_code": pl_party_code
                    }
                    matches.append(f"Rank {match_info['pl_rank']} (Party List {last_2})")
                    all_matches.append(match_info)

            # 3. Output Row
            if matches:
                status = "MATCH: " + ", ".join(matches)
            else:
                status = "No Match"

            all_rows.append({
                "area": area_code,
                "mp_number": mp_number,
                "mp_party": mp_party,
                "matched": len(matches) > 0,
                "status": status
            })
                
            print(f"{area_code:<6} | {mp_number:<6} | {mp_party:<10} | {status}")

        except Exception as e:
            print(f"Error processing {area_code}: {e}")

    # Final Summary (Counting and Sorting)
    print("\n" + "="*40)
    print(f"{'SUMMARY BY PARTY (DESC)':^40}")
    print("="*40)
    
    party_counts = {}
    if not all_matches:
        print("No matches discovered.")
    else:
        # Count matches per party
        for m in all_matches:
            p = m['mp_party']
            party_counts[p] = party_counts.get(p, 0) + 1
            
        # Sort desc
        sorted_parties = sorted(party_counts.items(), key=lambda item: item[1], reverse=True)
        
        print(f"{'Party Code':<20} | {'Match Count':<10}")
        print("-" * 40)
        for party, count in sorted_parties:
            print(f"{party:<20} | {count:<10}")
    print("="*40)

    # Export JSON results
    if export_json:
        export_results(all_rows, all_matches, party_counts)

def export_results(all_rows, all_matches, party_counts):
    """
    Exports analysis results as JSON to docs/data/results.json
    """
    output_dir = "docs/data"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now(timezone.utc).isoformat()
    
    total_areas = len(all_rows)
    matched_areas = sum(1 for r in all_rows if r["matched"])
    
    # Build summary by party (sorted desc)
    sorted_parties = sorted(party_counts.items(), key=lambda item: item[1], reverse=True)
    summary = [{"party_code": p, "match_count": c} for p, c in sorted_parties]
    
    results = {
        "timestamp": timestamp,
        "total_areas": total_areas,
        "matched_areas": matched_areas,
        "match_rate": round(matched_areas / total_areas * 100, 2) if total_areas > 0 else 0,
        "summary_by_party": summary,
        "matches": all_matches,
        "details": all_rows
    }
    
    results_path = os.path.join(output_dir, "results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\nResults exported to {results_path}")

    # Append to history
    history_path = os.path.join(output_dir, "history.json")
    history = []
    if os.path.exists(history_path):
        try:
            with open(history_path, "r", encoding="utf-8") as f:
                history = json.load(f)
        except (json.JSONDecodeError, Exception):
            history = []
    
    history.append({
        "timestamp": timestamp,
        "total_areas": total_areas,
        "matched_areas": matched_areas,
        "match_rate": results["match_rate"],
        "summary_by_party": summary
    })
    
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    
    print(f"History updated at {history_path}")

if __name__ == "__main__":
    import sys
    print("--- MP winning number vs Top 8 Party List comparison ---")
    print("Logic: Ignores Party 06 and 09")
    export = "--export" in sys.argv
    compare_mp_and_pl(export_json=export)
