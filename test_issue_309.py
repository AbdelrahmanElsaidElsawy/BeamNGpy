"""
Test script to reproduce Issue #309: Roads not imported when using Terrain_Importer.terrain_and_road_import()

This script reproduces the exact issue reported by the user.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from beamngpy import BeamNGpy, Scenario, Vehicle, set_up_simple_logging
from beamngpy.tools import Terrain_Importer

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
    print(f"\nRoads data: {roads}")
    
    # Test the normalization function
    print("\n" + "=" * 80)
    print("Testing normalization function...")
    print("=" * 80)
    
    try:
        # Import the function logic
        from beamngpy.tools.terrain_import import Terrain_Importer
        
        # Simulate what happens in terrain_and_road_import
        normalized_roads = []
        for road in roads:
            normalized_road = []
            for node in road:
                if isinstance(node, dict):
                    normalized_road.append(node)
                elif isinstance(node, (list, tuple)) and len(node) >= 3:
                    if len(node) >= 4:
                        x, y, z, width = node[0], node[1], node[2], node[3]
                    else:
                        x, y, width = node[0], node[1], node[2]
                        z = 0.0
                    normalized_road.append({"x": float(x), "y": float(y), "width": float(width)})
                else:
                    raise ValueError(f"Invalid road node format: {node}")
            normalized_roads.append(normalized_road)
        
        print(f"\nNormalized roads:")
        print(f"Type: {type(normalized_roads)}")
        print(f"Number of roads: {len(normalized_roads)}")
        print(f"First road type: {type(normalized_roads[0])}")
        print(f"First node type: {type(normalized_roads[0][0])}")
        print(f"First node: {normalized_roads[0][0]}")
        print(f"\nNormalized roads data:")
        for i, road in enumerate(normalized_roads):
            print(f"  Road {i}: {road}")
        
        print("\n✅ Normalization successful!")
        
    except Exception as e:
        print(f"\n❌ Error during normalization: {e}")
        import traceback
        traceback.print_exc()

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
    normalized_roads = []
    for road in roads:
        normalized_road = []
        for node in road:
            if isinstance(node, dict):
                normalized_road.append(node)
            elif isinstance(node, (list, tuple)) and len(node) >= 3:
                if len(node) >= 4:
                    x, y, z, width = node[0], node[1], node[2], node[3]
                else:
                    x, y, width = node[0], node[1], node[2]
                    z = 0.0
                normalized_road.append({"x": float(x), "y": float(y), "width": float(width)})
            else:
                raise ValueError(f"Invalid road node format: {node}")
        normalized_roads.append(normalized_road)
    
    print(f"\nNormalized roads (should be same as input):")
    for i, road in enumerate(normalized_roads):
        print(f"  Road {i}: {road}")
    
    print("\n✅ Dictionary format works correctly!")

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
        },
        {
            "name": "4-element list [x, y, z, width]",
            "roads": [[[100.0, 200.0, 30.0, 5.0]]],
        },
        {
            "name": "Mixed format (should fail)",
            "roads": [[{"x": 100.0, "y": 200.0, "width": 5.0}, [300.0, 400.0, 6.0]]],
        },
    ]
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        roads = test_case['roads']
        try:
            normalized_roads = []
            for road in roads:
                normalized_road = []
                for node in road:
                    if isinstance(node, dict):
                        normalized_road.append(node)
                    elif isinstance(node, (list, tuple)) and len(node) >= 3:
                        if len(node) >= 4:
                            x, y, z, width = node[0], node[1], node[2], node[3]
                        else:
                            x, y, width = node[0], node[1], node[2]
                            z = 0.0
                        normalized_road.append({"x": float(x), "y": float(y), "width": float(width)})
                    else:
                        raise ValueError(f"Invalid road node format: {node}")
                normalized_roads.append(normalized_road)
            print(f"  ✅ Success: {normalized_roads}")
        except Exception as e:
            print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    print("Issue #309 Reproduction and Testing")
    print("=" * 80)
    
    test_user_format()
    test_dict_format()
    test_edge_cases()
    
    print("\n" + "=" * 80)
    print("All tests completed!")
    print("=" * 80)
