# Issue #309 Fix Summary

## Problem
Roads were not being imported when using `Terrain_Importer.terrain_and_road_import()`. The user was using a list format `[[x, y, z, width], ...]` but BeamNG expects a dictionary format `[{"x": x, "y": y, "width": width}, ...]`.

## Root Cause
The `terrain_and_road_import()` method was sending roads in the user's format directly to BeamNG without conversion. BeamNG's Lua side expects roads as dictionaries with `x`, `y`, and `width` keys, but was receiving nested lists instead.

## Solution
Added automatic format conversion in both `terrain_and_road_import()` and `peaks_and_road_import()` methods:

1. **Format Detection**: Detects if roads are in list format or dict format
2. **Automatic Conversion**: Converts list format `[x, y, z, width]` or `[x, y, width]` to dict format `{"x": x, "y": y, "width": width}`
3. **Validation**: Validates that dict format has required keys
4. **Logging**: Adds debug/info logging when conversion occurs
5. **Backward Compatibility**: Preserves existing dict format (no changes needed for existing code)

## Changes Made

### File: `src/beamngpy/tools/terrain_import.py`

1. **Enhanced `terrain_and_road_import()` method**:
   - Added format normalization logic
   - Added validation for dict format
   - Added logging for format conversion
   - Improved error messages with road/node indices

2. **Enhanced `peaks_and_road_import()` method**:
   - Same improvements as above

3. **Updated documentation**:
   - Added examples showing both formats
   - Clarified that z coordinate is ignored (terrain determines elevation)

## Testing

### Test Results
✅ User's list format `[[x, y, z, width], ...]` → correctly converts to `[{"x": x, "y": y, "width": width}, ...]`
✅ Dictionary format `[{"x": x, "y": y, "width": width}, ...]` → preserved as-is
✅ Mixed format (dict and list in same road) → works correctly
✅ Edge cases (3-element lists, 4-element lists) → handled correctly
✅ Invalid formats → proper error messages

### Before Fix
```python
# User's format sent directly to BeamNG
roads = [[[-900.0, 0.0, 28, 8], [-800.0, 0.0, 28, 8]]]
# Result: Roads don't appear (wrong format)
```

### After Fix
```python
# User's format automatically converted
roads = [[[-900.0, 0.0, 28, 8], [-800.0, 0.0, 28, 8]]]
# Internally converted to:
# [[{"x": -900.0, "y": 0.0, "width": 8.0}, {"x": -800.0, "y": 0.0, "width": 8.0}]]
# Result: Roads appear correctly!
```

## Usage Examples

### List Format (Now Supported)
```python
roads = [
    [
        [-900.0, 0.0, 28, 8],
        [-800.0, 0.0, 28, 8],
        [-700.0, 0.0, 28, 8],
    ],
    [
        [0.0, -900.0, 28, 8],
        [0.0, -800.0, 28, 8],
    ],
]

Terrain_Importer.terrain_and_road_import(
    bng=bng,
    png_path="heightmap.png",
    roads=roads,
    DOI=100.0,
    margin=4.0,
    zMax=400.0
)
```

### Dictionary Format (Still Works)
```python
roads = [
    [
        {"x": -800.0, "y": 100.0, "width": 7.0},
        {"x": -700.0, "y": 100.0, "width": 7.0},
    ],
]

Terrain_Importer.terrain_and_road_import(
    bng=bng,
    png_path="heightmap.png",
    roads=roads,
    DOI=100.0,
    margin=4.0,
    zMax=400.0
)
```

## Notes

- The `z` coordinate in list format `[x, y, z, width]` is ignored because the terrain heightmap determines the road elevation
- Both formats are now supported, but dictionary format is recommended for clarity
- Error messages now include road and node indices for easier debugging
- Format conversion is logged at DEBUG/INFO level for troubleshooting
