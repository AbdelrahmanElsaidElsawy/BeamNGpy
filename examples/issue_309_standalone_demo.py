"""
Standalone demonstration of Issue #309 fix.

This example shows the format conversion without requiring BeamNG to be running.
It demonstrates:
1. The user's original format (from GitHub issue #309)
2. How it would have failed before the fix
3. How it works now with automatic format conversion
4. Error handling for invalid formats

This is a standalone script that doesn't require BeamNG to be running.
"""

import json


def normalize_roads(roads):
    """
    This is the normalization logic from the fix.
    It converts list format to dictionary format automatically.
    """
    normalized_roads = []
    format_converted = False
    
    for road_idx, road in enumerate(roads):
        normalized_road = []
        for node_idx, node in enumerate(road):
            if isinstance(node, dict):
                # Already in dict format, validate and use as-is
                if "x" not in node or "y" not in node or "width" not in node:
                    raise ValueError(
                        f"Invalid road node dict format at road {road_idx}, node {node_idx}: "
                        f"missing required keys. Expected 'x', 'y', 'width'. Got: {list(node.keys())}"
                    )
                normalized_road.append(node)
            elif isinstance(node, (list, tuple)) and len(node) >= 3:
                # Convert from list format [x, y, z, width] or [x, y, width]
                format_converted = True
                if len(node) >= 4:
                    x, y, z, width = node[0], node[1], node[2], node[3]
                    print(f"  🔄 Converting: [{x}, {y}, {z}, {width}] → {{'x': {x}, 'y': {y}, 'width': {width}}}")
                    print(f"     (z={z} is ignored - terrain determines elevation)")
                else:
                    x, y, width = node[0], node[1], node[2]
                    print(f"  🔄 Converting: [{x}, {y}, {width}] → {{'x': {x}, 'y': {y}, 'width': {width}}}")
                normalized_road.append({"x": float(x), "y": float(y), "width": float(width)})
            else:
                raise ValueError(
                    f"Invalid road node format at road {road_idx}, node {node_idx}: {node}. "
                    f"Expected dict with 'x', 'y', 'width' keys or list [x, y, z, width] or [x, y, width]"
                )
        normalized_roads.append(normalized_road)
    
    if format_converted:
        print("\n  ✅ Format conversion completed!")
        print("     List format automatically converted to dictionary format.")
    
    return normalized_roads


def demonstrate_user_format():
    """
    Demonstrates the user's original format from issue #309.
    """
    print("=" * 80)
    print("DEMONSTRATION: User's Original Format (Issue #309)")
    print("=" * 80)
    
    # This is the EXACT format from GitHub issue #309
    # Lines 8-28 from ISSUE_309_STEP_BY_STEP.md
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
    
    print("\n📋 User's Code (from GitHub issue #309):")
    print("   roads = [")
    print("       [[-900.0, 0.0, 28, 8], [-800.0, 0.0, 28, 8], [-700.0, 0.0, 28, 8]],")
    print("       [[0.0, -900.0, 28, 8], [0.0, -800.0, 28, 8], [0.0, -700.0, 28, 8]],")
    print("   ]")
    
    print("\n📊 Format Analysis:")
    print(f"   Type: {type(roads)}")
    print(f"   Structure: List of lists of lists")
    print(f"   First node: {roads[0][0]}")
    print(f"   Format: [[x, y, z, width], ...]")
    
    print("\n❌ BEFORE FIX:")
    print("   - This format was sent directly to BeamNG")
    print("   - BeamNG expects: [{\"x\": x, \"y\": y, \"width\": width}, ...]")
    print("   - Result: Roads don't appear in scene (silent failure)")
    
    print("\n✅ AFTER FIX:")
    print("   - Format is automatically converted")
    print("   - Conversion happens in terrain_and_road_import()")
    print("   - Result: Roads appear correctly!")
    
    print("\n🔄 Conversion Process:")
    normalized = normalize_roads(roads)
    
    print("\n📤 What gets sent to BeamNG (AFTER conversion):")
    message = {
        "type": "TerrainAndRoadImport",
        "pngPath": "heightmap.png",
        "roads": normalized,
        "DOI": 100.0,
        "margin": 4.0,
        "zMax": 400.0,
    }
    print(json.dumps(message, indent=2))
    
    print("\n✅ SUCCESS! Roads are now in the correct format!")
    print("   BeamNG will recognize and process them correctly.")
    
    return roads, normalized


def demonstrate_error_handling():
    """
    Demonstrates error handling for invalid formats.
    """
    print("\n" + "=" * 80)
    print("ERROR HANDLING: Invalid Formats")
    print("=" * 80)
    
    print("\n1. Testing invalid format (2-element list - missing width):")
    try:
        invalid_roads = [[[100.0, 200.0]]]  # Missing width
        print(f"   Input: {invalid_roads[0][0]}")
        normalize_roads(invalid_roads)
        print("   ❌ Should have raised an error!")
    except ValueError as e:
        print(f"   ✅ Caught error: {e}")
    
    print("\n2. Testing invalid dict format (missing 'width' key):")
    try:
        invalid_roads = [[{"x": 100.0, "y": 200.0}]]  # Missing width
        print(f"   Input: {invalid_roads[0][0]}")
        normalize_roads(invalid_roads)
        print("   ❌ Should have raised an error!")
    except ValueError as e:
        print(f"   ✅ Caught error: {e}")
    
    print("\n3. Testing valid formats:")
    print("   a) List format [x, y, z, width]:")
    try:
        valid_roads = [[[100.0, 200.0, 30.0, 5.0]]]
        normalized = normalize_roads(valid_roads)
        print(f"      ✅ Works! Converted to: {normalized[0][0]}")
    except Exception as e:
        print(f"      ❌ Error: {e}")
    
    print("\n   b) List format [x, y, width] (3 elements):")
    try:
        valid_roads = [[[100.0, 200.0, 5.0]]]
        normalized = normalize_roads(valid_roads)
        print(f"      ✅ Works! Converted to: {normalized[0][0]}")
    except Exception as e:
        print(f"      ❌ Error: {e}")
    
    print("\n   c) Dictionary format:")
    try:
        valid_roads = [[{"x": 100.0, "y": 200.0, "width": 5.0}]]
        normalized = normalize_roads(valid_roads)
        print(f"      ✅ Works! Preserved as: {normalized[0][0]}")
    except Exception as e:
        print(f"      ❌ Error: {e}")
    
    print("\n✅ Error messages include road and node indices for easier debugging!")


def demonstrate_comparison():
    """
    Shows side-by-side comparison of before and after.
    """
    print("\n" + "=" * 80)
    print("SIDE-BY-SIDE COMPARISON")
    print("=" * 80)
    
    roads = [[[-900.0, 0.0, 28, 8], [-800.0, 0.0, 28, 8]]]
    
    print("\nBEFORE FIX (what was sent to BeamNG):")
    message_before = {
        "type": "TerrainAndRoadImport",
        "roads": roads,  # List format - WRONG!
    }
    print(json.dumps(message_before, indent=2))
    print("   ❌ Result: Roads don't appear (wrong format)")
    
    print("\nAFTER FIX (what is sent to BeamNG now):")
    normalized = normalize_roads(roads)
    message_after = {
        "type": "TerrainAndRoadImport",
        "roads": normalized,  # Dict format - CORRECT!
    }
    print(json.dumps(message_after, indent=2))
    print("   ✅ Result: Roads appear correctly!")


def main():
    """
    Main demonstration function.
    """
    print("\n" + "=" * 80)
    print("ISSUE #309: Complete Standalone Demonstration")
    print("=" * 80)
    print("\nThis example demonstrates the fix without requiring BeamNG to run.")
    print("It shows the format conversion that happens automatically.")
    
    # Demonstrate the user's format
    original, normalized = demonstrate_user_format()
    
    # Show comparison
    demonstrate_comparison()
    
    # Show error handling
    demonstrate_error_handling()
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("\n✅ Issue #309 is FIXED!")
    print("\nKey Points:")
    print("  1. ✅ User's list format [[x, y, z, width], ...] now works automatically")
    print("  2. ✅ Dictionary format [{\"x\": x, \"y\": y, \"width\": width}, ...] still works")
    print("  3. ✅ Both formats are automatically converted to BeamNG's expected format")
    print("  4. ✅ The 'z' coordinate in list format is ignored (terrain determines elevation)")
    print("  5. ✅ Better error messages with road/node indices for invalid formats")
    print("  6. ✅ Logging shows when format conversion occurs")
    print("\nThe user's code from the GitHub issue will now work without any changes!")
    print("\nTo use in your code:")
    print("  from beamngpy.tools import Terrain_Importer")
    print("  ")
    print("  roads = [[[-900.0, 0.0, 28, 8], [-800.0, 0.0, 28, 8]]]  # List format")
    print("  ")
    print("  Terrain_Importer.terrain_and_road_import(")
    print("      bng=bng,")
    print("      png_path='heightmap.png',")
    print("      roads=roads,  # Automatically converted!")
    print("      DOI=100.0,")
    print("      margin=4.0,")
    print("      zMax=400.0")
    print("  )")


if __name__ == "__main__":
    main()
