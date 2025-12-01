"""
Test script to reproduce Issue #309: Roads not imported when using Terrain_Importer.terrain_and_road_import()

This script tests the normalization logic step by step.
"""
import json

def normalize_roads(roads):
    """
    Normalize road format: convert list format [x, y, z, width] to dict format {"x": x, "y": y, "width": width}
    This is the logic from terrain_and_road_import()
    """
    normalized_roads = []
    for road in roads:
        normalized_road = []
        for node in road:
            if isinstance(node, dict):
                # Already in dict format, use as-is
                normalized_road.append(node)
            elif isinstance(node, (list, tuple)) and len(node) >= 3:
                # Convert from list format [x, y, z, width] or [x, y, width]
                if len(node) >= 4:
                    x, y, z, width = node[0], node[1], node[2], node[3]
                else:
                    x, y, width = node[0], node[1], node[2]
                    z = 0.0  # Default z if not provided
                normalized_road.append({"x": float(x), "y": float(y), "width": float(width)})
            else:
                raise ValueError(f"Invalid road node format: {node}. Expected dict with 'x', 'y', 'width' keys or list [x, y, z, width]")
        normalized_roads.append(normalized_road)
    return normalized_roads

def test_user_format():
    """
    Test with the exact format the user reported (list format)
    """
    print("=" * 80)
    print("TEST 1: Reproducing user's bug with list format")
    print("=" * 80)
    
    # User's exact format from the issue
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
    
    print(f"\nRoads format (user's format):")
    print(f"Type: {type(roads)}")
    print(f"Number of roads: {len(roads)}")
    print(f"First road type: {type(roads[0])}")
    print(f"First node type: {type(roads[0][0])}")
    print(f"First node: {roads[0][0]}")
    print(f"\nRoads data:")
    print(json.dumps(roads, indent=2))
    
    # Test the normalization function
    print("\n" + "=" * 80)
    print("Testing normalization function...")
    print("=" * 80)
    
    try:
        normalized_roads = normalize_roads(roads)
        
        print(f"\nNormalized roads:")
        print(f"Type: {type(normalized_roads)}")
        print(f"Number of roads: {len(normalized_roads)}")
        print(f"First road type: {type(normalized_roads[0])}")
        print(f"First node type: {type(normalized_roads[0][0])}")
        print(f"First node: {normalized_roads[0][0]}")
        print(f"\nNormalized roads data:")
        print(json.dumps(normalized_roads, indent=2))
        
        # Verify the format
        print("\n" + "=" * 80)
        print("Verifying normalized format...")
        print("=" * 80)
        
        for i, road in enumerate(normalized_roads):
            print(f"\nRoad {i}:")
            for j, node in enumerate(road):
                if not isinstance(node, dict):
                    print(f"  ❌ Node {j} is not a dict: {type(node)}")
                elif "x" not in node or "y" not in node or "width" not in node:
                    print(f"  ❌ Node {j} missing required keys: {node}")
                else:
                    print(f"  ✅ Node {j}: x={node['x']}, y={node['y']}, width={node['width']}")
        
        print("\n✅ Normalization successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error during normalization: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dict_format():
    """
    Test with the working dictionary format from examples
    """
    print("\n" + "=" * 80)
    print("TEST 2: Testing with dictionary format (from examples)")
    print("=" * 80)
    
    # Format from import_peaks_and_roads.py example
    roads = [
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
    
    print(f"\nRoads format (dictionary format):")
    print(f"Type: {type(roads)}")
    print(f"Number of roads: {len(roads)}")
    print(f"First road type: {type(roads[0])}")
    print(f"First node type: {type(roads[0][0])}")
    print(f"First node: {roads[0][0]}")
    
    # Test normalization
    try:
        normalized_roads = normalize_roads(roads)
        
        print(f"\nNormalized roads (should be same as input):")
        print(json.dumps(normalized_roads, indent=2))
        
        # Verify they're the same
        if normalized_roads == roads:
            print("\n✅ Dictionary format preserved correctly!")
        else:
            print("\n⚠️  Dictionary format changed (should be identical)")
            print("Original:", roads)
            print("Normalized:", normalized_roads)
        
        return True
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_edge_cases():
    """
    Test edge cases
    """
    print("\n" + "=" * 80)
    print("TEST 3: Testing edge cases")
    print("=" * 80)
    
    test_cases = [
        {
            "name": "3-element list [x, y, width]",
            "roads": [[[100.0, 200.0, 5.0]]],
            "should_work": True,
        },
        {
            "name": "4-element list [x, y, z, width]",
            "roads": [[[100.0, 200.0, 30.0, 5.0]]],
            "should_work": True,
        },
        {
            "name": "Mixed format (dict and list)",
            "roads": [[{"x": 100.0, "y": 200.0, "width": 5.0}, [300.0, 400.0, 6.0]]],
            "should_work": True,
        },
        {
            "name": "Invalid: 2-element list",
            "roads": [[[100.0, 200.0]]],
            "should_work": False,
        },
    ]
    
    results = []
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        roads = test_case['roads']
        try:
            normalized_roads = normalize_roads(roads)
            print(f"  ✅ Success: {normalized_roads}")
            results.append((test_case['name'], True, test_case['should_work']))
        except Exception as e:
            print(f"  ❌ Error: {e}")
            results.append((test_case['name'], False, test_case['should_work']))
    
    # Summary
    print("\n" + "=" * 80)
    print("Edge case test summary:")
    print("=" * 80)
    for name, worked, should_work in results:
        status = "✅" if worked == should_work else "❌"
        print(f"{status} {name}: worked={worked}, expected={should_work}")

def test_what_gets_sent():
    """
    Test what actually gets sent to BeamNG (simulate the message format)
    """
    print("\n" + "=" * 80)
    print("TEST 4: What gets sent to BeamNG")
    print("=" * 80)
    
    # User's format
    roads = [
        [
            [-900.0, 0.0, 28, 8],
            [-800.0, 0.0, 28, 8],
        ],
    ]
    
    print("\nOriginal format (user's input):")
    print(json.dumps(roads, indent=2))
    
    normalized_roads = normalize_roads(roads)
    
    print("\nNormalized format (what gets sent):")
    print(json.dumps(normalized_roads, indent=2))
    
    # Simulate the message that would be sent
    message = {
        "type": "TerrainAndRoadImport",
        "pngPath": "test.png",
        "roads": normalized_roads,
        "DOI": 100.0,
        "margin": 4.0,
        "zMax": 400.0,
    }
    
    print("\nComplete message that would be sent:")
    print(json.dumps(message, indent=2))
    
    # Compare with what the user's format would send (before fix)
    print("\n" + "=" * 80)
    print("BEFORE FIX: What would have been sent (user's format directly):")
    print("=" * 80)
    old_message = {
        "type": "TerrainAndRoadImport",
        "pngPath": "test.png",
        "roads": roads,  # User's format directly
        "DOI": 100.0,
        "margin": 4.0,
        "zMax": 400.0,
    }
    print(json.dumps(old_message, indent=2))
    
    print("\n" + "=" * 80)
    print("DIFFERENCE:")
    print("=" * 80)
    print("BEFORE: roads were sent as nested lists: [[[-900.0, 0.0, 28, 8], ...]]")
    print("AFTER:  roads are sent as nested dicts: [[{\"x\": -900.0, \"y\": 0.0, \"width\": 8}, ...]]")
    print("\nThis is likely why roads weren't appearing - BeamNG expects dict format!")

if __name__ == "__main__":
    print("Issue #309 Reproduction and Testing")
    print("=" * 80)
    
    test1 = test_user_format()
    test2 = test_dict_format()
    test_edge_cases()
    test_what_gets_sent()
    
    print("\n" + "=" * 80)
    print("All tests completed!")
    print("=" * 80)
    
    if test1 and test2:
        print("\n✅ All main tests passed!")
    else:
        print("\n❌ Some tests failed!")
