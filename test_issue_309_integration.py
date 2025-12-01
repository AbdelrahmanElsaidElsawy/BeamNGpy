"""
Integration test for Issue #309 - Simulates the actual message sending
"""
import json
import sys
import os

# Add a mock connection class to simulate what happens
class MockConnection:
    def __init__(self):
        self.sent_messages = []
    
    def send(self, data):
        self.sent_messages.append(data)
        return MockResponse()
    
    def get_last_message(self):
        return self.sent_messages[-1] if self.sent_messages else None

class MockResponse:
    def ack(self, expected_type):
        pass

class MockBeamNG:
    def __init__(self):
        self.connection = MockConnection()

def test_terrain_and_road_import():
    """
    Test the actual terrain_and_road_import function with user's format
    """
    print("=" * 80)
    print("INTEGRATION TEST: terrain_and_road_import with user's format")
    print("=" * 80)
    
    # Import the function
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    from beamngpy.tools.terrain_import import Terrain_Importer
    
    # Create mock BeamNG instance
    bng = MockBeamNG()
    
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
    
    print("\n1. User's input format:")
    print(f"   Type: {type(roads)}")
    print(f"   First node: {roads[0][0]}")
    print(f"   Format: List of lists of lists")
    
    # Call the function
    try:
        Terrain_Importer.terrain_and_road_import(
            bng=bng,
            png_path="test_heightmap.png",
            roads=roads,
            DOI=100.0,
            margin=4.0,
            zMax=400.0
        )
        
        # Check what was sent
        message = bng.connection.get_last_message()
        
        print("\n2. Message sent to BeamNG:")
        print(f"   Type: {message['type']}")
        print(f"   Roads type: {type(message['roads'])}")
        print(f"   Number of roads: {len(message['roads'])}")
        print(f"   First road type: {type(message['roads'][0])}")
        print(f"   First node type: {type(message['roads'][0][0])}")
        print(f"   First node: {message['roads'][0][0]}")
        
        print("\n3. Complete message (formatted):")
        print(json.dumps(message, indent=2))
        
        # Verify format
        print("\n4. Verification:")
        all_correct = True
        for road_idx, road in enumerate(message['roads']):
            for node_idx, node in enumerate(road):
                if not isinstance(node, dict):
                    print(f"   ❌ Road {road_idx}, node {node_idx}: Not a dict! Got {type(node)}")
                    all_correct = False
                elif "x" not in node or "y" not in node or "width" not in node:
                    print(f"   ❌ Road {road_idx}, node {node_idx}: Missing keys! Got {list(node.keys())}")
                    all_correct = False
                else:
                    print(f"   ✅ Road {road_idx}, node {node_idx}: x={node['x']}, y={node['y']}, width={node['width']}")
        
        if all_correct:
            print("\n✅ SUCCESS: All roads are in correct format!")
            print("   The roads should now appear in BeamNG.")
        else:
            print("\n❌ FAILURE: Some roads are in incorrect format!")
        
        return all_correct
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_before_fix_simulation():
    """
    Simulate what would have happened BEFORE the fix
    """
    print("\n" + "=" * 80)
    print("SIMULATION: What would have been sent BEFORE the fix")
    print("=" * 80)
    
    roads = [
        [
            [-900.0, 0.0, 28, 8],
            [-800.0, 0.0, 28, 8],
        ],
    ]
    
    # Simulate old code (no normalization)
    old_message = {
        "type": "TerrainAndRoadImport",
        "pngPath": "test.png",
        "roads": roads,  # Sent directly without conversion
        "DOI": 100.0,
        "margin": 4.0,
        "zMax": 400.0,
    }
    
    print("\nBEFORE FIX - Message format:")
    print(json.dumps(old_message, indent=2))
    print("\n❌ Problem: Roads are nested lists, BeamNG expects nested dicts!")
    print("   This is why roads didn't appear.")

def test_after_fix_simulation():
    """
    Show what happens AFTER the fix
    """
    print("\n" + "=" * 80)
    print("SIMULATION: What is sent AFTER the fix")
    print("=" * 80)
    
    roads = [
        [
            [-900.0, 0.0, 28, 8],
            [-800.0, 0.0, 28, 8],
        ],
    ]
    
    # Normalize (what the fix does)
    normalized_roads = []
    for road in roads:
        normalized_road = []
        for node in road:
            if isinstance(node, (list, tuple)) and len(node) >= 4:
                x, y, z, width = node[0], node[1], node[2], node[3]
                normalized_road.append({"x": float(x), "y": float(y), "width": float(width)})
        normalized_roads.append(normalized_road)
    
    new_message = {
        "type": "TerrainAndRoadImport",
        "pngPath": "test.png",
        "roads": normalized_roads,  # Converted to dict format
        "DOI": 100.0,
        "margin": 4.0,
        "zMax": 400.0,
    }
    
    print("\nAFTER FIX - Message format:")
    print(json.dumps(new_message, indent=2))
    print("\n✅ Solution: Roads are now nested dicts, matching BeamNG's expected format!")
    print("   Roads should now appear correctly.")

if __name__ == "__main__":
    print("Issue #309 Integration Test")
    print("=" * 80)
    
    test_before_fix_simulation()
    test_after_fix_simulation()
    
    success = test_terrain_and_road_import()
    
    print("\n" + "=" * 80)
    if success:
        print("✅ ALL TESTS PASSED - Fix is working correctly!")
    else:
        print("❌ TESTS FAILED - Fix needs adjustment")
    print("=" * 80)
