"""
Format comparison example for Issue #309.

This script demonstrates the format conversion that happens automatically.
It shows what format is sent to BeamNG before and after the fix.
"""

import json
import sys
import os

# Add src to path to import beamngpy
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def demonstrate_format_conversion():
    """
    Demonstrates how the format conversion works.
    """
    print("=" * 80)
    print("ISSUE #309: Format Conversion Demonstration")
    print("=" * 80)

    # ============================================================================
    # User's original format (from GitHub issue #309)
    # ============================================================================
    print("\n1. USER'S ORIGINAL FORMAT (from GitHub issue #309)")
    print("-" * 80)
    
    roads_user_format = [
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

    print(f"Input format: List of lists of lists")
    print(f"  Type: {type(roads_user_format)}")
    print(f"  Structure: [[[x, y, z, width], ...], ...]")
    print(f"\nFirst road, first node: {roads_user_format[0][0]}")
    print(f"  Interpretation: x=-900.0, y=0.0, z=28, width=8")
    print(f"  Note: 'z' coordinate (28) will be ignored (terrain determines elevation)")

    # ============================================================================
    # What was sent BEFORE the fix (WRONG - roads don't appear)
    # ============================================================================
    print("\n" + "=" * 80)
    print("2. BEFORE FIX: What was sent to BeamNG (WRONG FORMAT)")
    print("=" * 80)
    
    message_before = {
        "type": "TerrainAndRoadImport",
        "pngPath": "heightmap.png",
        "roads": roads_user_format,  # Sent directly - WRONG!
        "DOI": 100.0,
        "margin": 4.0,
        "zMax": 400.0,
    }

    print("Message sent to BeamNG:")
    print(json.dumps(message_before, indent=2))
    print("\n❌ PROBLEM: Roads are nested lists, but BeamNG expects nested dictionaries!")
    print("   Result: Roads don't appear in the scene")

    # ============================================================================
    # Format conversion (what the fix does)
    # ============================================================================
    print("\n" + "=" * 80)
    print("3. FORMAT CONVERSION (what the fix does automatically)")
    print("=" * 80)

    # Simulate the normalization logic
    normalized_roads = []
    for road_idx, road in enumerate(roads_user_format):
        normalized_road = []
        for node_idx, node in enumerate(road):
            if isinstance(node, (list, tuple)) and len(node) >= 4:
                x, y, z, width = node[0], node[1], node[2], node[3]
                normalized_road.append({
                    "x": float(x),
                    "y": float(y),
                    "width": float(width)
                    # Note: z is ignored
                })
        normalized_roads.append(normalized_road)

    print("Conversion process:")
    print(f"  Input:  {roads_user_format[0][0]}  (list)")
    print(f"  Output: {normalized_roads[0][0]}  (dict)")
    print(f"\n  Key changes:")
    print(f"    - List [x, y, z, width] → Dict {{\"x\": x, \"y\": y, \"width\": width}}")
    print(f"    - z coordinate (28) is ignored")
    print(f"    - All values converted to float")

    # ============================================================================
    # What is sent AFTER the fix (CORRECT - roads appear)
    # ============================================================================
    print("\n" + "=" * 80)
    print("4. AFTER FIX: What is sent to BeamNG (CORRECT FORMAT)")
    print("=" * 80)

    message_after = {
        "type": "TerrainAndRoadImport",
        "pngPath": "heightmap.png",
        "roads": normalized_roads,  # Converted to dict format - CORRECT!
        "DOI": 100.0,
        "margin": 4.0,
        "zMax": 400.0,
    }

    print("Message sent to BeamNG:")
    print(json.dumps(message_after, indent=2))
    print("\n✅ SOLUTION: Roads are now nested dictionaries, matching BeamNG's expected format!")
    print("   Result: Roads appear correctly in the scene")

    # ============================================================================
    # Comparison
    # ============================================================================
    print("\n" + "=" * 80)
    print("5. SIDE-BY-SIDE COMPARISON")
    print("=" * 80)

    print("\nBEFORE FIX (roads don't appear):")
    print("  roads: [[[-900.0, 0.0, 28, 8], [-800.0, 0.0, 28, 8]], ...]")
    print("  Format: List of lists of lists")
    print("  BeamNG: ❌ Doesn't recognize this format")

    print("\nAFTER FIX (roads appear correctly):")
    print("  roads: [[{\"x\": -900.0, \"y\": 0.0, \"width\": 8.0}, ...], ...]")
    print("  Format: List of lists of dictionaries")
    print("  BeamNG: ✅ Recognizes and processes correctly")

    # ============================================================================
    # Dictionary format (still works)
    # ============================================================================
    print("\n" + "=" * 80)
    print("6. DICTIONARY FORMAT (from examples - still works)")
    print("=" * 80)

    roads_dict_format = [
        [
            {"x": -800.0, "y": 100.0, "width": 7.0},
            {"x": -700.0, "y": 100.0, "width": 7.0},
        ],
    ]

    print("Input format: Already in dictionary format")
    print(f"  First node: {roads_dict_format[0][0]}")
    print("\n✅ This format is preserved as-is (no conversion needed)")
    print("   It was always working and continues to work")

    # ============================================================================
    # Summary
    # ============================================================================
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("\n✅ List format [[x, y, z, width], ...] → Automatically converted")
    print("✅ Dictionary format [{\"x\": x, \"y\": y, \"width\": width}, ...] → Used as-is")
    print("✅ Both formats now work correctly")
    print("✅ The 'z' coordinate in list format is ignored (terrain determines elevation)")
    print("✅ Better error messages if format is invalid")
    print("\nThe fix ensures roads are always sent in the correct format!")


if __name__ == "__main__":
    demonstrate_format_conversion()
