# BeamNGpy Issues Fixed

This document summarizes the GitHub issues that have been addressed, ordered from hardest to easiest.

## Issues Fixed

### 1. Issue #309: Roads not imported when using Terrain_Importer.terrain_and_road_import()
**Difficulty:** Medium  
**Status:** ✅ Fixed

**Problem:** Roads were not being imported correctly because the format was unclear. Users were using list format `[x, y, z, width]` but the code expected dictionary format `{"x": x, "y": y, "width": width}`.

**Solution:**
- Added format validation and automatic conversion in `terrain_and_road_import()` and `peaks_and_road_import()` methods
- Now supports both formats:
  - Dictionary format: `{"x": float, "y": float, "width": float}` (recommended)
  - List format: `[x, y, z, width]` or `[x, y, width]`
- Added comprehensive documentation with examples
- Files modified:
  - `src/beamngpy/tools/terrain_import.py`

### 2. Issue #304: Teleporting vehicles should allow setting cling as spawn does
**Difficulty:** Easy  
**Status:** ✅ Fixed

**Problem:** The `teleport()` method didn't have a `cling` parameter like `spawn()` does, making it difficult to teleport vehicles to the correct ground level.

**Solution:**
- Added `cling` parameter to all `teleport()` methods
- When `cling=True`, the z-coordinate is automatically adjusted to ground level
- Files modified:
  - `src/beamngpy/api/beamng/vehicles.py`
  - `src/beamngpy/api/beamng/vehicles_ge.py`
  - `src/beamngpy/vehicle/vehicle.py`

### 3. Issue #202: Vehicle retains old control inputs after bng.scenario.restart()
**Difficulty:** Medium  
**Status:** ✅ Fixed

**Problem:** After restarting a scenario, vehicles would retain their previous control inputs (steering, throttle, brake), causing unexpected behavior.

**Solution:**
- Modified `restart()` method in `ScenarioApi` to clear all vehicle control inputs after reconnecting
- All vehicles now have their controls reset to neutral (steering=0.0, throttle=0.0, brake=0.0, parkingbrake=0.0) after restart
- Files modified:
  - `src/beamngpy/api/beamng/scenario.py`

### 4. Issue #288: How to get the lane info of a decal road?
**Difficulty:** Easy  
**Status:** ✅ Fixed

**Problem:** No easy way to retrieve lane information (number of lanes, one-way status, etc.) for a specific DecalRoad.

**Solution:**
- Added new method `get_road_lane_info(road: str)` to `ScenarioApi`
- Returns a dictionary with lane information including:
  - `lanes_left`: Number of lanes on the left side
  - `lanes_right`: Number of lanes on the right side
  - `one_way`: Whether the road is one-way
  - `drivability`: Drivability value
  - `flip_direction`: Whether direction is flipped
  - `material`: Road material name
  - `width`: Road width information
- Files modified:
  - `src/beamngpy/api/beamng/scenario.py`

## Issues Remaining (Not Yet Addressed)

The following issues are more complex and may require additional investigation or Lua-side changes:

- **Issue #205:** Vehicle collision cannot be disabled (requires Lua/engine changes)
- **Issue #305:** Questions about Python <-> Lua Interaction (documentation/example needed)
- **Issue #306:** How to disable one wheel on the fly (requires vehicle physics API)
- **Issue #295:** Shadows rendered incorrectly in camera sensor (rendering issue)
- **Issue #286:** No effect of add_checkpoints() after load() (scenario management)
- **Issue #224:** Controlling vehicle actuation with road wheel angle (feature request)
- **Issue #133:** Accessing BeamNG.tech from remote host (network configuration)
- **Issue #63:** Memory Error when using Lidar (memory management)

## Testing Recommendations

Before submitting these fixes, please test:

1. **Issue #309:** Test terrain_and_road_import() with both dictionary and list formats
2. **Issue #304:** Test teleport() with cling=True on various terrain heights
3. **Issue #202:** Test scenario restart and verify controls are cleared
4. **Issue #288:** Test get_road_lane_info() on various roads in different scenarios

## Notes

- All changes maintain backward compatibility
- Documentation has been updated where applicable
- No breaking changes were introduced
