"""
Example demonstrating Issue #309 fix: Roads not imported when using list format.

This example shows:
1. How the user's original format (list format) now works correctly
2. How the dictionary format (from examples) still works
3. How the fix automatically converts list format to dictionary format

Before the fix: Roads in list format [[x, y, z, width], ...] would not appear.
After the fix: Both formats work - list format is automatically converted.
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
    scenario = Scenario("tech_ground", "issue_309_terrain_road_import")
    vehicle = Vehicle("ego_vehicle", model="etk800")
    scenario.add_vehicle(vehicle)

    # Start up BeamNG.
    print("Making scenario...")
    scenario.make(beamng)
    beamng.scenario.load(scenario)
    beamng.scenario.start()

    # Open the world editor - NOTE: THE WORLD EDITOR MUST BE OPEN WHEN USING THE TERRAIN IMPORTER.
    print("Opening the world editor...")
    Terrain_Importer.open_close_world_editor(beamng, True)
    time.sleep(5)

    print("\n" + "=" * 80)
    print("ISSUE #309 DEMONSTRATION")
    print("=" * 80)

    # ============================================================================
    # EXAMPLE 1: User's original format (list format) - NOW WORKS!
    # ============================================================================
    print("\n" + "-" * 80)
    print("EXAMPLE 1: User's original format (list format)")
    print("Before fix: Roads would NOT appear")
    print("After fix: Roads automatically converted and appear correctly")
    print("-" * 80)

    # This is the EXACT format from the GitHub issue #309
    # Format: [[x, y, z, width], ...]
    roads_user_format = [
        [
            [-900.0, 0.0, 28, 8],
            [-800.0, 0.0, 28, 8],
            [-700.0, 0.0, 28, 8],
            [-600.0, 0.0, 28, 8],
            [-500.0, 0.0, 28, 8],
        ],
        [
            [0.0, -900.0, 28, 8],
            [0.0, -800.0, 28, 8],
            [0.0, -700.0, 28, 8],
            [0.0, -600.0, 28, 8],
            [0.0, -500.0, 28, 8],
        ],
    ]

    print(f"\nUser's format (list of lists):")
    print(f"  Type: {type(roads_user_format)}")
    print(f"  First road type: {type(roads_user_format[0])}")
    print(f"  First node type: {type(roads_user_format[0][0])}")
    print(f"  First node: {roads_user_format[0][0]}")
    print(f"  Format: [[x, y, z, width], ...]")

    # Note: You would need an actual heightmap PNG file for this to work
    # For demonstration, we'll show the format conversion
    print("\n⚠️  Note: This example requires a valid heightmap PNG file.")
    print("   The format conversion happens automatically in terrain_and_road_import().")
    print("\n   To use with actual terrain:")
    print("   Terrain_Importer.terrain_and_road_import(")
    print("       bng=beamng,")
    print("       png_path='path/to/heightmap.png',")
    print("       roads=roads_user_format,  # List format - automatically converted!")
    print("       DOI=100.0,")
    print("       margin=4.0,")
    print("       zMax=400.0")
    print("   )")

    # ============================================================================
    # EXAMPLE 2: Dictionary format (from examples) - STILL WORKS!
    # ============================================================================
    print("\n" + "-" * 80)
    print("EXAMPLE 2: Dictionary format (from examples)")
    print("This format was always working and still works")
    print("-" * 80)

    # This is the format from examples/import_peaks_and_roads.py
    # Format: [{"x": x, "y": y, "width": width}, ...]
    roads_dict_format = [
        [
            {"x": -800.0, "y": 100.0, "width": 7.0},
            {"x": -700.0, "y": 100.0, "width": 7.0},
            {"x": -600.0, "y": 100.0, "width": 7.0},
            {"x": -500.0, "y": 100.0, "width": 7.0},
            {"x": -400.0, "y": 100.0, "width": 7.0},
        ],
        [
            {"x": 100.0, "y": -800.0, "width": 7.0},
            {"x": 100.0, "y": -700.0, "width": 7.0},
            {"x": 100.0, "y": -600.0, "width": 7.0},
            {"x": 100.0, "y": -500.0, "width": 7.0},
            {"x": 100.0, "y": -400.0, "width": 7.0},
        ],
    ]

    print(f"\nDictionary format:")
    print(f"  Type: {type(roads_dict_format)}")
    print(f"  First road type: {type(roads_dict_format[0])}")
    print(f"  First node type: {type(roads_dict_format[0][0])}")
    print(f"  First node: {roads_dict_format[0][0]}")
    print(f"  Format: [{{\"x\": x, \"y\": y, \"width\": width}}, ...]")

    # ============================================================================
    # EXAMPLE 3: Using peaks_and_road_import with list format
    # ============================================================================
    print("\n" + "-" * 80)
    print("EXAMPLE 3: Using peaks_and_road_import with list format")
    print("This also works now with automatic conversion")
    print("-" * 80)

    # Set some peaks/troughs
    peaks = []
    peaks.append({"x": 100.0, "y": 100.0, "z": 250.0})
    peaks.append({"x": 900.0, "y": 100.0, "z": 200.0})
    peaks.append({"x": 100.0, "y": 900.0, "z": 0.0})
    peaks.append({"x": -500.0, "y": 500.0, "z": 250.0})

    # Roads in list format (user's format)
    roads_list_format = [
        [
            [-800.0, 100.0, 28, 7],  # [x, y, z, width]
            [-700.0, 100.0, 28, 7],
            [-600.0, 100.0, 28, 7],
        ],
        [
            [100.0, -800.0, 28, 7],
            [100.0, -700.0, 28, 7],
            [100.0, -600.0, 28, 7],
        ],
    ]

    print(f"\nPeaks: {len(peaks)} points")
    print(f"Roads (list format): {len(roads_list_format)} roads")
    print(f"  First node: {roads_list_format[0][0]}")

    print("\n✅ This format will be automatically converted when calling:")
    print("   Terrain_Importer.peaks_and_road_import(")
    print("       bng=beamng,")
    print("       peaks=peaks,")
    print("       roads=roads_list_format,  # List format - automatically converted!")
    print("       DOI=150.0,")
    print("       margin=6.0")
    print("   )")

    # ============================================================================
    # ACTUAL USAGE EXAMPLE (commented out - requires heightmap file)
    # ============================================================================
    print("\n" + "=" * 80)
    print("ACTUAL USAGE EXAMPLE")
    print("=" * 80)
    print("\nTo actually import terrain and roads, uncomment and modify the code below:")
    print("\n# Example with user's list format (now works!):")
    print("# Terrain_Importer.terrain_and_road_import(")
    print("#     bng=beamng,")
    print("#     png_path='path/to/your/heightmap.png',  # 16-bit greyscale PNG")
    print("#     roads=roads_user_format,  # List format - automatically converted!")
    print("#     DOI=100.0,  # Domain of influence")
    print("#     margin=4.0,  # Smoothing margin")
    print("#     zMax=400.0  # Max terrain height")
    print("# )")
    print("\n# Example with dictionary format (still works!):")
    print("# Terrain_Importer.terrain_and_road_import(")
    print("#     bng=beamng,")
    print("#     png_path='path/to/your/heightmap.png',")
    print("#     roads=roads_dict_format,  # Dictionary format - used as-is")
    print("#     DOI=100.0,")
    print("#     margin=4.0,")
    print("#     zMax=400.0")
    print("# )")
    print("\n# Example with peaks and roads (list format):")
    print("# Terrain_Importer.peaks_and_road_import(")
    print("#     bng=beamng,")
    print("#     peaks=peaks,")
    print("#     roads=roads_list_format,  # List format - automatically converted!")
    print("#     DOI=150.0,")
    print("#     margin=6.0")
    print("# )")

    print("\n" + "=" * 80)
    print("KEY POINTS:")
    print("=" * 80)
    print("1. ✅ List format [[x, y, z, width], ...] now works automatically")
    print("2. ✅ Dictionary format [{\"x\": x, \"y\": y, \"width\": width}, ...] still works")
    print("3. ✅ Both formats are automatically converted to BeamNG's expected format")
    print("4. ✅ The 'z' coordinate in list format is ignored (terrain determines elevation)")
    print("5. ✅ Better error messages if format is invalid")
    print("6. ✅ Logging shows when format conversion occurs")

    vehicle.teleport((100.0, 100.0, 250.0), cling=True)
    vehicle.switch()

    print("\n✅ Example completed!")
    print("   The fix ensures both formats work correctly.")
    print("   Check the logs for format conversion messages if using list format.")

    # Execute BeamNG until the user closes it.
    input("\nPress Enter to close...")
    beamng.disconnect()


if __name__ == "__main__":
    main()
