# Issue #309 Examples

This directory contains examples demonstrating the fix for Issue #309: "Roads not imported when using Terrain_Importer.terrain_and_road_import()".

## Examples Created

### 1. `issue_309_standalone_demo.py` ⭐ **RECOMMENDED**
**Standalone demonstration that doesn't require BeamNG to run.**

This is the best example to start with. It shows:
- The user's original format from GitHub issue #309
- How the format conversion works automatically
- Before/after comparison of what gets sent to BeamNG
- Error handling for invalid formats
- Complete working examples

**Run it:**
```bash
python3 examples/issue_309_standalone_demo.py
```

**Output:**
- Shows format conversion in action
- Demonstrates error handling
- Shows side-by-side comparison
- No BeamNG required!

---

### 2. `issue_309_format_comparison.py`
**Format comparison demonstration.**

Shows the exact format differences between before and after the fix.

**Run it:**
```bash
python3 examples/issue_309_format_comparison.py
```

**Output:**
- Detailed format analysis
- JSON comparison of messages sent to BeamNG
- Clear before/after visualization

---

### 3. `issue_309_terrain_and_road_import_example.py`
**Complete BeamNGpy example (requires BeamNG).**

Full working example that can be run with BeamNG. Shows:
- User's format working with `terrain_and_road_import()`
- Dictionary format still working
- Using `peaks_and_road_import()` with list format

**Run it:**
```bash
# Requires BeamNG to be installed and running
python3 examples/issue_309_terrain_and_road_import_example.py
```

**Note:** This example requires BeamNG to be installed and available.

---

### 4. `issue_309_demo.py`
**Complete demonstration with error handling (requires BeamNG).**

Shows the full workflow including error handling.

**Run it:**
```bash
# Requires BeamNG to be installed and running
python3 examples/issue_309_demo.py
```

---

## Quick Start

### For Understanding the Fix (No BeamNG Required)
```bash
python3 examples/issue_309_standalone_demo.py
```

### For Testing with BeamNG
```bash
# Make sure BeamNG is running first
python3 examples/issue_309_terrain_and_road_import_example.py
```

## The User's Original Code (Now Works!)

This is the exact code from GitHub issue #309 that now works:

```python
from beamngpy.tools import Terrain_Importer

# User's format (list format) - NOW WORKS!
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

Terrain_Importer.terrain_and_road_import(
    bng=bng,
    png_path=str(HEIGHTMAP_PATH),
    roads=roads,  # Automatically converted!
    DOI=100.0,
    margin=4.0,
    zMax=400.0
)
```

## What the Fix Does

1. **Automatic Format Conversion**
   - List format `[[x, y, z, width], ...]` → Dict format `[{"x": x, "y": y, "width": width}, ...]`
   - Happens automatically in `terrain_and_road_import()` and `peaks_and_road_import()`

2. **Backward Compatibility**
   - Dictionary format still works (no changes needed)
   - Existing code continues to work

3. **Better Error Messages**
   - Includes road and node indices
   - Clear messages for invalid formats

4. **Logging**
   - Shows when format conversion occurs
   - Helps with debugging

## Supported Formats

### ✅ List Format (Now Supported)
```python
roads = [
    [[-900.0, 0.0, 28, 8], [-800.0, 0.0, 28, 8]],  # [x, y, z, width]
    [[100.0, -900.0, 28, 8], [100.0, -800.0, 28, 8]],
]
```

### ✅ List Format (3 elements)
```python
roads = [
    [[-900.0, 0.0, 8], [-800.0, 0.0, 8]],  # [x, y, width]
]
```

### ✅ Dictionary Format (Still Works)
```python
roads = [
    [{"x": -800.0, "y": 100.0, "width": 7.0}, {"x": -700.0, "y": 100.0, "width": 7.0}],
]
```

## Notes

- The `z` coordinate in list format `[x, y, z, width]` is **ignored** (terrain heightmap determines elevation)
- Both formats are automatically converted to BeamNG's expected format
- Error messages include road and node indices for easier debugging
- Format conversion is logged at DEBUG/INFO level

## Related Files

- `ISSUE_309_STEP_BY_STEP.md` - Detailed step-by-step explanation
- `ISSUE_309_FIX_SUMMARY.md` - Summary of the fix
- `src/beamngpy/tools/terrain_import.py` - The actual fix implementation
