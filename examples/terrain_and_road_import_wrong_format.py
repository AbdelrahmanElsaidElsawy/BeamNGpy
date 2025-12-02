"""
Example: terrain_and_road_import with WRONG format (from GitHub issue #309).

This demonstrates what happens when using the wrong format (list format).
The roads will NOT appear in the scene.

This is the EXACT code from GitHub issue #309 that doesn't work.
"""

import time

from beamngpy import BeamNGpy, Scenario, Vehicle, set_up_simple_logging
from beamngpy.tools import Terrain_Importer


def main():
    set_up_simple_logging()

    # Initialize BeamNG.
    print("Initializing BeamNG...")
    beamng = BeamNGpy("localhost", 25252)
    beamng.open(launch=True)
    scenario = Scenario("tech_ground", "terrain_loader_example_roads_wrong")
    vehicle = Vehicle("ego_vehicle", model="etk800")
    scenario.add_vehicle(vehicle)

    # Start up BeamNG.
    print("Making scenario...")
    scenario.make(beamng)
    beamng.scenario.load(scenario)
    beamng.scenario.start()

    # Open the world editor - REQUIRED for terrain importer
    print("Opening the world editor...")
    print("NOTE: The world editor MUST be open when using the terrain importer.")
    Terrain_Importer.open_close_world_editor(beamng, True)
    time.sleep(5)  # Wait for world editor to open

    # ============================================================================
    # USER'S CODE FROM GITHUB ISSUE #309 (WRONG FORMAT)
    # ============================================================================
    print("\n" + "=" * 80)
    print("USER'S CODE FROM GITHUB ISSUE #309 (WRONG FORMAT)")
    print("=" * 80)
    print("\n⚠️  WARNING: This format does NOT work!")
    print("   Format: [[x, y, z, width], ...] (list format)")
    print("   Result: Roads will NOT appear in the scene")
    print()

    # This is the EXACT format from GitHub issue #309
    # Format: List of lists of lists
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

    print(f"Roads format: {type(roads)}")
    print(f"First road type: {type(roads[0])}")
    print(f"First node type: {type(roads[0][0])}")
    print(f"First node: {roads[0][0]}")
    print(f"\n❌ Problem: This is list format, but BeamNG expects dictionary format!")

    DOMAIN_OF_INFLUENCE = 100.0  # meters around roads affected by terraforming
    MARGIN = 4.0  # smoothing margin
    Z_MAX = 400.0  # max terrain height in meters

    # NOTE: You need to provide a valid heightmap PNG file path
    # Replace this with your actual heightmap path
    HEIGHTMAP_PATH = "path/to/your/heightmap.png"  # 16-bit greyscale PNG

    print("\n" + "-" * 80)
    print("ATTEMPTING TO IMPORT TERRAIN AND ROADS (WRONG FORMAT)")
    print("-" * 80)
    print("\n⚠️  This will fail - roads won't appear!")
    print("   The terrain will import, but roads will be missing.")
    print("\nTo actually run this, uncomment the code below and provide a valid heightmap:")

    # Uncomment to actually test (will fail - roads won't appear):
    # print("\nImporting terrain and roads with wrong format...")
    # Terrain_Importer.terrain_and_road_import(
    #     bng=beamng,
    #     png_path=str(HEIGHTMAP_PATH),
    #     roads=roads,  # Wrong format - roads won't appear!
    #     DOI=DOMAIN_OF_INFLUENCE,
    #     margin=MARGIN,
    #     zMax=Z_MAX
    # )
    # print("⚠️  Check the scene - roads should NOT be visible!")

    vehicle.teleport((0.0, 0.0, 250.0), cling=True)
    vehicle.switch()

    print("\n" + "=" * 80)
    print("RESULT")
    print("=" * 80)
    print("\n❌ With this format (list format):")
    print("   - Terrain imports correctly ✅")
    print("   - Roads message is sent to BeamNG ✅")
    print("   - BeamNG receives wrong format ❌")
    print("   - Roads don't appear in scene ❌")
    print("\n📝 SOLUTION:")
    print("   Use dictionary format instead!")
    print("   See: examples/terrain_and_road_import_correct_format.py")

    # Execute BeamNG until the user closes it.
    input("\nPress Enter to close...")
    beamng.disconnect()


if __name__ == "__main__":
    main()
