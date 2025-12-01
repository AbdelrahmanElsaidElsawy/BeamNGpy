"""
Example: Importing terrain and roads using Terrain_Importer.

This example demonstrates how to import a heightmap terrain together with roads.
It shows the correct format for roads that BeamNG expects.

IMPORTANT: Roads must be in dictionary format with 'x', 'y', and 'width' keys.
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
    scenario = Scenario("tech_ground", "terrain_and_road_import_example")
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
    # TERRAIN AND ROAD IMPORT
    # ============================================================================
    print("\n" + "=" * 80)
    print("TERRAIN AND ROAD IMPORT")
    print("=" * 80)

    # IMPORTANT: Roads must be in dictionary format!
    # Each road is a list of nodes, where each node is a dictionary with:
    #   - "x": x-coordinate (float)
    #   - "y": y-coordinate (float)
    #   - "width": road width in meters (float)
    #
    # The z-coordinate is NOT needed - the terrain heightmap determines elevation.
    #
    # Format: [
    #     [  # First road
    #         {"x": x1, "y": y1, "width": w1},
    #         {"x": x2, "y": y2, "width": w2},
    #         ...
    #     ],
    #     [  # Second road
    #         {"x": x1, "y": y1, "width": w1},
    #         ...
    #     ],
    # ]

    # Example: Two roads crossing each other
    roads = [
        # First road: horizontal road
        [
            {"x": -800.0, "y": 0.0, "width": 8.0},
            {"x": -700.0, "y": 0.0, "width": 8.0},
            {"x": -600.0, "y": 0.0, "width": 8.0},
            {"x": -500.0, "y": 0.0, "width": 8.0},
            {"x": -400.0, "y": 0.0, "width": 8.0},
            {"x": -300.0, "y": 0.0, "width": 8.0},
            {"x": -200.0, "y": 0.0, "width": 8.0},
            {"x": -100.0, "y": 0.0, "width": 8.0},
            {"x": 0.0, "y": 0.0, "width": 8.0},
            {"x": 100.0, "y": 0.0, "width": 8.0},
            {"x": 200.0, "y": 0.0, "width": 8.0},
            {"x": 300.0, "y": 0.0, "width": 8.0},
            {"x": 400.0, "y": 0.0, "width": 8.0},
            {"x": 500.0, "y": 0.0, "width": 8.0},
            {"x": 600.0, "y": 0.0, "width": 8.0},
            {"x": 700.0, "y": 0.0, "width": 8.0},
            {"x": 800.0, "y": 0.0, "width": 8.0},
        ],
        # Second road: vertical road
        [
            {"x": 0.0, "y": -800.0, "width": 8.0},
            {"x": 0.0, "y": -700.0, "width": 8.0},
            {"x": 0.0, "y": -600.0, "width": 8.0},
            {"x": 0.0, "y": -500.0, "width": 8.0},
            {"x": 0.0, "y": -400.0, "width": 8.0},
            {"x": 0.0, "y": -300.0, "width": 8.0},
            {"x": 0.0, "y": -200.0, "width": 8.0},
            {"x": 0.0, "y": -100.0, "width": 8.0},
            {"x": 0.0, "y": 0.0, "width": 8.0},  # Intersection point
            {"x": 0.0, "y": 100.0, "width": 8.0},
            {"x": 0.0, "y": 200.0, "width": 8.0},
            {"x": 0.0, "y": 300.0, "width": 8.0},
            {"x": 0.0, "y": 400.0, "width": 8.0},
            {"x": 0.0, "y": 500.0, "width": 8.0},
            {"x": 0.0, "y": 600.0, "width": 8.0},
            {"x": 0.0, "y": 700.0, "width": 8.0},
            {"x": 0.0, "y": 800.0, "width": 8.0},
        ],
    ]

    print(f"\nPrepared {len(roads)} roads:")
    print(f"  Road 1: {len(roads[0])} nodes (horizontal)")
    print(f"  Road 2: {len(roads[1])} nodes (vertical)")
    print(f"  First node example: {roads[0][0]}")

    # Parameters for terrain import
    HEIGHTMAP_PATH = "path/to/your/heightmap.png"  # Replace with your heightmap path
    DOMAIN_OF_INFLUENCE = 100.0  # meters around roads affected by terraforming
    MARGIN = 4.0  # smoothing margin
    Z_MAX = 400.0  # max terrain height in meters

    print("\n" + "-" * 80)
    print("IMPORTANT: Road Format Requirements")
    print("-" * 80)
    print("Roads must be in dictionary format:")
    print('  [{"x": float, "y": float, "width": float}, ...]')
    print("\nNOT list format:")
    print("  [[x, y, z, width], ...]  ❌ This will NOT work!")
    print("\nThe 'z' coordinate is NOT needed - terrain heightmap determines elevation.")

    print("\n" + "-" * 80)
    print("To import terrain and roads:")
    print("-" * 80)
    print("1. Prepare a 16-bit greyscale PNG heightmap")
    print("2. Format roads as shown above (dictionary format)")
    print("3. Call Terrain_Importer.terrain_and_road_import()")
    print("\nExample code:")
    print("  Terrain_Importer.terrain_and_road_import(")
    print("      bng=beamng,")
    print("      png_path='path/to/heightmap.png',")
    print("      roads=roads,  # Dictionary format!")
    print("      DOI=100.0,")
    print("      margin=4.0,")
    print("      zMax=400.0")
    print("  )")

    # Uncomment the following lines to actually import terrain and roads:
    # print("\nImporting terrain and roads...")
    # Terrain_Importer.terrain_and_road_import(
    #     bng=beamng,
    #     png_path=HEIGHTMAP_PATH,
    #     roads=roads,
    #     DOI=DOMAIN_OF_INFLUENCE,
    #     margin=MARGIN,
    #     zMax=Z_MAX
    # )
    # print("✅ Terrain and roads imported successfully!")

    vehicle.teleport((0.0, 0.0, 250.0), cling=True)
    vehicle.switch()

    print("\n" + "=" * 80)
    print("Example completed!")
    print("=" * 80)
    print("\nRemember:")
    print("  ✅ Use dictionary format: [{\"x\": x, \"y\": y, \"width\": width}, ...]")
    print("  ❌ Do NOT use list format: [[x, y, z, width], ...]")
    print("\nSee the documentation for more details.")

    # Execute BeamNG until the user closes it.
    input("\nPress Enter to close...")
    beamng.disconnect()


if __name__ == "__main__":
    main()
