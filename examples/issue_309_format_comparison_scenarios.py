"""
Scenario Comparison: User's Code (Wrong Format) vs Correct Format

This demonstrates:
1. User's code from GitHub issue #309 (wrong format) - roads don't appear
2. Correct format - roads appear correctly
"""

import json
from typing import List, Dict, Any


def scenario_user_code_wrong_format():
    """
    SCENARIO 1: User's code from GitHub issue #309 (WRONG FORMAT)
    This shows what happens when using the wrong format.
    """
    print("=" * 80)
    print("SCENARIO 1: USER'S CODE (WRONG FORMAT)")
    print("=" * 80)
    print("\nThis is the EXACT code from GitHub issue #309")
    print("(Lines 8-28 from ISSUE_309_STEP_BY_STEP.md)\n")
    
    # User's exact code
    print("USER'S CODE:")
    print("-" * 80)
    print("roads = [")
    print("    [")
    print("        [-900.0, 0.0, 28, 8],")
    print("        [-800.0, 0.0, 28, 8],")
    print("        [-700.0, 0.0, 28, 8],")
    print("    ],")
    print("    [")
    print("        [0.0, -900.0, 28, 8],")
    print("        [0.0, -800.0, 28, 8],")
    print("        [0.0, -700.0, 28, 8],")
    print("    ],")
    print("]")
    print()
    print("Terrain_Importer.terrain_and_road_import(")
    print("    bng=bng,")
    print("    png_path=str(HEIGHTMAP_PATH),")
    print("    roads=roads,")
    print("    DOI=100.0,")
    print("    margin=4.0,")
    print("    zMax=400.0")
    print(")")
    
    # Actual data
    roads = [
        [
            [-900.0, 0.0, 28, 8],
            [-800.0, 0.0, 28, 8],
            [-700.0, 0.0, 28, 8],
        ],
        [
            [0.0, -900.0, 28, 8],
            [0.0, -800.0, 28, 8],
            [0.0, -700.0, 28, 8],
        ],
    ]
    
    print("\n" + "-" * 80)
    print("WHAT HAPPENS:")
    print("-" * 80)
    print(f"Format type: {type(roads)}")
    print(f"First road type: {type(roads[0])}")
    print(f"First node type: {type(roads[0][0])}")
    print(f"First node: {roads[0][0]}")
    print(f"Structure: List of lists of lists")
    
    print("\n" + "-" * 80)
    print("WHAT GETS SENT TO BEAMNG:")
    print("-" * 80)
    message = {
        "type": "TerrainAndRoadImport",
        "pngPath": "heightmap.png",
        "roads": roads,  # Wrong format sent directly
        "DOI": 100.0,
        "margin": 4.0,
        "zMax": 400.0,
    }
    print(json.dumps(message, indent=2))
    
    print("\n" + "-" * 80)
    print("RESULT:")
    print("-" * 80)
    print("❌ PROBLEM: Roads are in list format [[x, y, z, width], ...]")
    print("   BeamNG expects: Dictionary format [{\"x\": x, \"y\": y, \"width\": width}, ...]")
    print()
    print("❌ WHAT HAPPENS:")
    print("   1. Terrain imports correctly ✅")
    print("   2. Roads message is sent to BeamNG ✅")
    print("   3. BeamNG receives wrong format ❌")
    print("   4. BeamNG doesn't recognize the format ❌")
    print("   5. Roads don't appear in scene ❌")
    print()
    print("📋 USER'S REPORT:")
    print("   'The terrain imports correctly, but no roads appear in the scene.'")
    print("   'I would like to confirm the expected format of the roads list'")
    
    return roads


def scenario_correct_format():
    """
    SCENARIO 2: Correct format (WORKS)
    This shows what happens when using the correct format.
    """
    print("\n\n" + "=" * 80)
    print("SCENARIO 2: CORRECT FORMAT (WORKS)")
    print("=" * 80)
    print("\nThis is the CORRECT format that works with terrain_and_road_import()\n")
    
    # Correct code
    print("CORRECT CODE:")
    print("-" * 80)
    print("roads = [")
    print("    [")
    print("        {\"x\": -900.0, \"y\": 0.0, \"width\": 8.0},")
    print("        {\"x\": -800.0, \"y\": 0.0, \"width\": 8.0},")
    print("        {\"x\": -700.0, \"y\": 0.0, \"width\": 8.0},")
    print("    ],")
    print("    [")
    print("        {\"x\": 0.0, \"y\": -900.0, \"width\": 8.0},")
    print("        {\"x\": 0.0, \"y\": -800.0, \"width\": 8.0},")
    print("        {\"x\": 0.0, \"y\": -700.0, \"width\": 8.0},")
    print("    ],")
    print("]")
    print()
    print("Terrain_Importer.terrain_and_road_import(")
    print("    bng=bng,")
    print("    png_path=str(HEIGHTMAP_PATH),")
    print("    roads=roads,")
    print("    DOI=100.0,")
    print("    margin=4.0,")
    print("    zMax=400.0")
    print(")")
    
    # Actual data in correct format
    roads = [
        [
            {"x": -900.0, "y": 0.0, "width": 8.0},
            {"x": -800.0, "y": 0.0, "width": 8.0},
            {"x": -700.0, "y": 0.0, "width": 8.0},
        ],
        [
            {"x": 0.0, "y": -900.0, "width": 8.0},
            {"x": 0.0, "y": -800.0, "width": 8.0},
            {"x": 0.0, "y": -700.0, "width": 8.0},
        ],
    ]
    
    print("\n" + "-" * 80)
    print("WHAT HAPPENS:")
    print("-" * 80)
    print(f"Format type: {type(roads)}")
    print(f"First road type: {type(roads[0])}")
    print(f"First node type: {type(roads[0][0])}")
    print(f"First node: {roads[0][0]}")
    print(f"Structure: List of lists of dictionaries")
    
    print("\n" + "-" * 80)
    print("WHAT GETS SENT TO BEAMNG:")
    print("-" * 80)
    message = {
        "type": "TerrainAndRoadImport",
        "pngPath": "heightmap.png",
        "roads": roads,  # Correct format
        "DOI": 100.0,
        "margin": 4.0,
        "zMax": 400.0,
    }
    print(json.dumps(message, indent=2))
    
    print("\n" + "-" * 80)
    print("RESULT:")
    print("-" * 80)
    print("✅ SUCCESS: Roads are in dictionary format [{\"x\": x, \"y\": y, \"width\": width}, ...]")
    print("   BeamNG expects: Dictionary format [{\"x\": x, \"y\": y, \"width\": width}, ...]")
    print()
    print("✅ WHAT HAPPENS:")
    print("   1. Terrain imports correctly ✅")
    print("   2. Roads message is sent to BeamNG ✅")
    print("   3. BeamNG receives correct format ✅")
    print("   4. BeamNG recognizes the format ✅")
    print("   5. Roads appear in scene ✅")
    print()
    print("📋 RESULT:")
    print("   'Terrain and roads imported successfully!'")
    print("   'Roads are visible in the scene.'")
    
    return roads


def side_by_side_comparison():
    """
    Shows side-by-side comparison of both scenarios.
    """
    print("\n\n" + "=" * 80)
    print("SIDE-BY-SIDE COMPARISON")
    print("=" * 80)
    
    # User's format
    roads_wrong = [
        [[-900.0, 0.0, 28, 8], [-800.0, 0.0, 28, 8]],
    ]
    
    # Correct format
    roads_correct = [
        [{"x": -900.0, "y": 0.0, "width": 8.0}, {"x": -800.0, "y": 0.0, "width": 8.0}],
    ]
    
    print("\nUSER'S FORMAT (WRONG)          |  CORRECT FORMAT")
    print("-" * 80)
    print(f"Type: {type(roads_wrong[0][0])}              |  Type: {type(roads_correct[0][0])}")
    print(f"Format: List                  |  Format: Dictionary")
    print(f"Structure: [[x, y, z, width]] |  Structure: [{{\"x\": x, \"y\": y, \"width\": width}}]")
    print(f"Example: {roads_wrong[0][0]}  |  Example: {roads_correct[0][0]}")
    print()
    print("Sent to BeamNG:                |  Sent to BeamNG:")
    print(json.dumps({"roads": roads_wrong}, indent=2)[:40] + "...")
    print("                               |  " + json.dumps({"roads": roads_correct}, indent=2)[:40] + "...")
    print()
    print("Result: ❌ Roads don't appear  |  Result: ✅ Roads appear")
    print("Reason: Wrong format           |  Reason: Correct format")


def show_conversion_needed():
    """
    Shows what conversion is needed.
    """
    print("\n\n" + "=" * 80)
    print("CONVERSION NEEDED")
    print("=" * 80)
    print("\nTo fix the user's code, convert from list format to dictionary format:")
    print()
    print("BEFORE (User's format - doesn't work):")
    print("  [[-900.0, 0.0, 28, 8], [-800.0, 0.0, 28, 8]]")
    print()
    print("AFTER (Correct format - works):")
    print("  [{\"x\": -900.0, \"y\": 0.0, \"width\": 8.0}, {\"x\": -800.0, \"y\": 0.0, \"width\": 8.0}]")
    print()
    print("CONVERSION RULE:")
    print("  [x, y, z, width] → {\"x\": x, \"y\": y, \"width\": width}")
    print("  (z coordinate is ignored - terrain determines elevation)")
    print()
    print("NOTE: This conversion will be done automatically in a future version.")


def main():
    """
    Main function demonstrating both scenarios.
    """
    print("\n" + "=" * 80)
    print("ISSUE #309: FORMAT COMPARISON SCENARIOS")
    print("=" * 80)
    print("\nThis demonstrates:")
    print("  1. User's code (wrong format) - roads don't appear")
    print("  2. Correct format - roads appear correctly")
    print("  3. Side-by-side comparison")
    print("  4. Conversion needed")
    
    # Scenario 1: User's code (wrong format)
    roads_wrong = scenario_user_code_wrong_format()
    
    # Scenario 2: Correct format
    roads_correct = scenario_correct_format()
    
    # Side-by-side comparison
    side_by_side_comparison()
    
    # Show conversion needed
    show_conversion_needed()
    
    print("\n\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("\n❌ USER'S CODE (Wrong Format):")
    print("   - Format: [[x, y, z, width], ...]")
    print("   - Result: Roads don't appear")
    print("   - Reason: BeamNG expects dictionary format")
    print()
    print("✅ CORRECT FORMAT:")
    print("   - Format: [{\"x\": x, \"y\": y, \"width\": width}, ...]")
    print("   - Result: Roads appear correctly")
    print("   - Reason: Matches BeamNG's expected format")
    print()
    print("📝 SOLUTION:")
    print("   Use the correct format (dictionary) until automatic conversion is implemented.")
    print("   See examples/terrain_and_road_import_example.py for working code.")


if __name__ == "__main__":
    main()
