"""
Example: Demonstrating correct vs wrong road format for terrain_and_road_import.

This example shows:
1. The CORRECT format (dictionary) - this works
2. The WRONG format (list) - this doesn't work
3. How to convert from wrong to correct format

IMPORTANT: Use the CORRECT format (dictionary) until the automatic conversion is implemented.
"""

import json
from typing import List, Dict, Any


def show_correct_format() -> List[List[Dict[str, float]]]:
    """
    Shows the CORRECT format for roads that BeamNG expects.
    
    Returns:
        Roads in the correct dictionary format.
    """
    print("=" * 80)
    print("CORRECT FORMAT (Dictionary Format)")
    print("=" * 80)
    print("\n✅ This format WORKS with terrain_and_road_import()")
    print("\nFormat: Each node is a dictionary with 'x', 'y', 'width' keys")
    print("  roads = [")
    print("      [  # First road")
    print("          {\"x\": -800.0, \"y\": 100.0, \"width\": 7.0},")
    print("          {\"x\": -700.0, \"y\": 100.0, \"width\": 7.0},")
    print("      ],")
    print("      [  # Second road")
    print("          {\"x\": 100.0, \"y\": -800.0, \"width\": 7.0},")
    print("          {\"x\": 100.0, \"y\": -700.0, \"width\": 7.0},")
    print("      ]")
    print("  ]")
    
    # Example of correct format
    roads_correct = [
        [
            {"x": -800.0, "y": 100.0, "width": 7.0},
            {"x": -700.0, "y": 100.0, "width": 7.0},
            {"x": -600.0, "y": 100.0, "width": 7.0},
            {"x": -500.0, "y": 100.0, "width": 7.0},
        ],
        [
            {"x": 100.0, "y": -800.0, "width": 7.0},
            {"x": 100.0, "y": -700.0, "width": 7.0},
            {"x": 100.0, "y": -600.0, "width": 7.0},
            {"x": 100.0, "y": -500.0, "width": 7.0},
        ],
    ]
    
    print("\nExample (correct format):")
    print(json.dumps(roads_correct, indent=2))
    
    print("\n✅ Use this format - it works correctly!")
    print("   Each node: {\"x\": float, \"y\": float, \"width\": float}")
    print("   Note: 'z' coordinate is NOT needed (terrain determines elevation)")
    
    return roads_correct


def show_wrong_format() -> List[List[List[float]]]:
    """
    Shows the WRONG format that users might try to use.
    
    Returns:
        Roads in the wrong list format.
    """
    print("\n" + "=" * 80)
    print("WRONG FORMAT (List Format)")
    print("=" * 80)
    print("\n❌ This format does NOT work with terrain_and_road_import()")
    print("\nFormat: Each node is a list [x, y, z, width]")
    print("  roads = [")
    print("      [  # First road")
    print("          [-900.0, 0.0, 28, 8],")
    print("          [-800.0, 0.0, 28, 8],")
    print("      ],")
    print("      [  # Second road")
    print("          [0.0, -900.0, 28, 8],")
    print("          [0.0, -800.0, 28, 8],")
    print("      ]")
    print("  ]")
    
    # Example of wrong format (from GitHub issue #309)
    roads_wrong = [
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
    
    print("\nExample (wrong format - from GitHub issue #309):")
    print(json.dumps(roads_wrong, indent=2))
    
    print("\n❌ Do NOT use this format - it will cause roads not to appear!")
    print("   Problem: BeamNG expects dictionary format, not list format")
    print("   Result: Roads are sent but don't appear in the scene")
    
    return roads_wrong


def convert_wrong_to_correct(roads_wrong: List[List[List[float]]]) -> List[List[Dict[str, float]]]:
    """
    Converts wrong format (list) to correct format (dictionary).
    
    This is a helper function to show users how to convert their format.
    In the future, this conversion will be done automatically.
    
    Args:
        roads_wrong: Roads in list format [[x, y, z, width], ...]
    
    Returns:
        Roads in dictionary format [{"x": x, "y": y, "width": width}, ...]
    """
    print("\n" + "=" * 80)
    print("CONVERSION: Wrong Format → Correct Format")
    print("=" * 80)
    print("\nThis shows how to convert from wrong format to correct format.")
    print("(In the future, this will be done automatically)")
    
    roads_correct = []
    for road_idx, road in enumerate(roads_wrong):
        converted_road = []
        for node_idx, node in enumerate(road):
            if len(node) >= 4:
                x, y, z, width = node[0], node[1], node[2], node[3]
                # Convert to dictionary format
                converted_node = {"x": float(x), "y": float(y), "width": float(width)}
                converted_road.append(converted_node)
                print(f"  Road {road_idx}, Node {node_idx}: [{x}, {y}, {z}, {width}] → {converted_node}")
                print(f"    (z={z} is ignored - terrain determines elevation)")
            elif len(node) >= 3:
                x, y, width = node[0], node[1], node[2]
                converted_node = {"x": float(x), "y": float(y), "width": float(width)}
                converted_road.append(converted_node)
                print(f"  Road {road_idx}, Node {node_idx}: [{x}, {y}, {width}] → {converted_node}")
        roads_correct.append(converted_road)
    
    print("\n✅ Converted format (now correct):")
    print(json.dumps(roads_correct, indent=2))
    
    return roads_correct


def demonstrate_formats():
    """
    Main demonstration function showing both formats.
    """
    print("\n" + "=" * 80)
    print("ROAD FORMAT DEMONSTRATION FOR terrain_and_road_import()")
    print("=" * 80)
    print("\nThis example shows the difference between correct and wrong formats.")
    print("Use the CORRECT format until automatic conversion is implemented.\n")
    
    # Show correct format
    roads_correct = show_correct_format()
    
    # Show wrong format
    roads_wrong = show_wrong_format()
    
    # Show conversion
    roads_converted = convert_wrong_to_correct(roads_wrong)
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("\n✅ CORRECT FORMAT (use this):")
    print("   roads = [[{\"x\": x, \"y\": y, \"width\": width}, ...], ...]")
    print("   - Each node is a dictionary")
    print("   - Keys: 'x', 'y', 'width'")
    print("   - Works correctly with terrain_and_road_import()")
    
    print("\n❌ WRONG FORMAT (do not use):")
    print("   roads = [[[x, y, z, width], ...], ...]")
    print("   - Each node is a list")
    print("   - Roads don't appear in scene")
    print("   - Will be fixed in future version")
    
    print("\n📝 HOW TO USE:")
    print("   1. Use the CORRECT format (dictionary) for now")
    print("   2. If you have list format, convert it using convert_wrong_to_correct()")
    print("   3. In the future, automatic conversion will be implemented")
    
    print("\n📖 See examples/terrain_and_road_import_example.py for a complete working example.")


def get_correct_format_example() -> List[List[Dict[str, float]]]:
    """
    Returns an example of the correct format that users can copy.
    
    Returns:
        Example roads in correct dictionary format.
    """
    return [
        [
            {"x": -800.0, "y": 100.0, "width": 7.0},
            {"x": -700.0, "y": 100.0, "width": 7.0},
            {"x": -600.0, "y": 100.0, "width": 7.0},
        ],
        [
            {"x": 100.0, "y": -800.0, "width": 7.0},
            {"x": 100.0, "y": -700.0, "width": 7.0},
            {"x": 100.0, "y": -600.0, "width": 7.0},
        ],
    ]


def get_wrong_format_example() -> List[List[List[float]]]:
    """
    Returns an example of the wrong format (for reference).
    
    Returns:
        Example roads in wrong list format (from GitHub issue #309).
    """
    return [
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


if __name__ == "__main__":
    demonstrate_formats()
