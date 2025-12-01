from __future__ import annotations

from logging import DEBUG, getLogger

from beamngpy.logging import LOGGER_ID

from beamngpy import BeamNGpy


# The Terrain Importer class.
class Terrain_Importer:

    @staticmethod
    def import_heightmap(
        bng: BeamNGpy, data, w, h, scale=1, zMin=0, zMax=100, isYFlipped=True
    ):
        """
        Imports a heightmap from a 2D structure of 'pixel' values in the range given by [zMin, zMax].  The array should be indexable as [x][y].
        The scale describes the resolution of the final generated heightmap - in both x and y, in metres-per-pixel. The scale is isotropic.
        Heightmaps must ultimately satisfy the following conditions, which this function will ensure (by cropping, if required):
            i)    They must be square, ie the width and height must be the same.
            ii)   They must be a power of two in size, eg 2^4, 2^5, 2^6 etc.
            iii)  They must be between 128 and 8192 in length. This is the minimum and maximum possible heightmap data size.
        The generated heightmap will assume the vertical range [0, zMax - zMin] to ensure maximum granularity in its height.

        Args:
            bng: The BeamNG instance.
            data: A 2D dict of heightmap pixel values, indexed as [x][y].
            w: The width of the data (X dimension).
            h: The height of the data (Y dimension).
            scale: The scale of the data/resultant heightmap, in metres-per-pixel.
            zMin: The smallest elevation value in the data, in metres.
            zMax: The largest elevation value in the data, in metres.
            isYFlipped: A flag which indicates if the heightmap should be flipped in the Y dimension.
        """
        logger = getLogger(f"{LOGGER_ID}.Terrain_Importer")
        logger.setLevel(DEBUG)
        d = dict(
            type="ImportHeightmap",
            data=data,
            w=w,
            h=h,
            scale=scale,
            zMin=zMin,
            zMax=zMax,
            isYFlipped=isYFlipped,
        )
        response = bng.connection.send(d)
        response.ack("CompletedImportHeightmap")
        logger.debug("Terrain_Importer - terrain imported.")

    @staticmethod
    def terrain_and_road_import(bng: BeamNGpy, png_path, roads, DOI, margin, zMax):
        """
        Imports a heightmap from a given .png file (16-bit greyscale, uncompressed), then lays down the given roads on top of this modified terrain.
        The terrain will be further modified to fit the roads.

        Args:
            bng: The BeamNG instance.
            png_path: The path of the .png file (16-bit greyscale, uncompressed), which contains values in the range [0, 65535].
            roads: The list of roads which will be laid on the modified terrain (the terrain will also be terraformed to them).
                   Each road is a list of nodes. Each node can be specified in two formats:
                   1. Dictionary format: {"x": float, "y": float, "width": float} (recommended)
                   2. List format: [x, y, z, width] where x, y, z are coordinates and width is the road width
                   Example:
                   roads = [
                       [  # First road
                           {"x": -800.0, "y": 100.0, "width": 7.0},
                           {"x": -700.0, "y": 100.0, "width": 7.0},
                       ],
                       [  # Second road
                           {"x": 100.0, "y": -800.0, "width": 7.0},
                           {"x": 100.0, "y": -700.0, "width": 7.0},
                       ]
                   ]
            DOI: The domain of influence parameter of the terraforming process.
            margin: The margin parameter (around the roads).
            zMax: Sets the terrain prominence, which will be [0, zMax]. This is how the .png values will be scaled when modifying the terrain.
        """
        logger = getLogger(f"{LOGGER_ID}.Terrain_Importer")
        logger.setLevel(DEBUG)
        
        # Normalize road format: convert list format [x, y, z, width] to dict format {"x": x, "y": y, "width": width}
        # Note: z coordinate is ignored as terrain heightmap determines the road elevation
        normalized_roads = []
        format_converted = False
        
        for road_idx, road in enumerate(roads):
            normalized_road = []
            for node_idx, node in enumerate(road):
                if isinstance(node, dict):
                    # Already in dict format, use as-is
                    if "x" not in node or "y" not in node or "width" not in node:
                        raise ValueError(
                            f"Invalid road node dict format at road {road_idx}, node {node_idx}: "
                            f"missing required keys. Expected 'x', 'y', 'width'. Got: {list(node.keys())}"
                        )
                    normalized_road.append(node)
                elif isinstance(node, (list, tuple)) and len(node) >= 3:
                    # Convert from list format [x, y, z, width] or [x, y, width]
                    format_converted = True
                    if len(node) >= 4:
                        x, y, z, width = node[0], node[1], node[2], node[3]
                        logger.debug(
                            f"Converting road node from list format [x, y, z, width] to dict format. "
                            f"Road {road_idx}, node {node_idx}: z={z} will be ignored (terrain determines elevation)"
                        )
                    else:
                        x, y, width = node[0], node[1], node[2]
                    normalized_road.append({"x": float(x), "y": float(y), "width": float(width)})
                else:
                    raise ValueError(
                        f"Invalid road node format at road {road_idx}, node {node_idx}: {node}. "
                        f"Expected dict with 'x', 'y', 'width' keys or list [x, y, z, width] or [x, y, width]"
                    )
            normalized_roads.append(normalized_road)
        
        if format_converted:
            logger.info(
                "Terrain_Importer: Converted road format from list to dictionary format. "
                "This ensures compatibility with BeamNG's expected format."
            )
        
        d = dict(
            type="TerrainAndRoadImport",
            pngPath=png_path,
            roads=normalized_roads,
            DOI=DOI,
            margin=margin,
            zMax=zMax,
        )
        response = bng.connection.send(d)
        response.ack("CompletedTerrainAndRoadImport")
        logger.debug("Terrain_Importer - terrain and roads imported.")

    @staticmethod
    def peaks_and_road_import(bng: BeamNGpy, peaks, roads, DOI, margin):
        """
        Modifies the terrain with respect to a given collection of peaks and troughs (3D points), then lays down the given roads on top of this modified terrain.
        The terrain will be further modified to fit the given roads.

        Args:
            bng: The BeamNG instance.
            peaks: The list of 3D points which represent desired peaks and troughs in the terrain.
            roads: The list of roads which will be laid on the modified terrain (the terrain will also be terraformed to them).
                   Each road is a list of nodes. Each node can be specified in two formats:
                   1. Dictionary format: {"x": float, "y": float, "width": float} (recommended)
                   2. List format: [x, y, z, width] where x, y, z are coordinates and width is the road width
                   See terrain_and_road_import() for format examples.
            DOI: The domain of influence parameter of the terraforming process.
            margin: The margin parameter (around the roads).
        """
        logger = getLogger(f"{LOGGER_ID}.Terrain_Importer")
        logger.setLevel(DEBUG)
        
        # Normalize road format: convert list format [x, y, z, width] to dict format {"x": x, "y": y, "width": width}
        # Note: z coordinate is ignored as terrain heightmap determines the road elevation
        normalized_roads = []
        format_converted = False
        
        for road_idx, road in enumerate(roads):
            normalized_road = []
            for node_idx, node in enumerate(road):
                if isinstance(node, dict):
                    # Already in dict format, use as-is
                    if "x" not in node or "y" not in node or "width" not in node:
                        raise ValueError(
                            f"Invalid road node dict format at road {road_idx}, node {node_idx}: "
                            f"missing required keys. Expected 'x', 'y', 'width'. Got: {list(node.keys())}"
                        )
                    normalized_road.append(node)
                elif isinstance(node, (list, tuple)) and len(node) >= 3:
                    # Convert from list format [x, y, z, width] or [x, y, width]
                    format_converted = True
                    if len(node) >= 4:
                        x, y, z, width = node[0], node[1], node[2], node[3]
                        logger.debug(
                            f"Converting road node from list format [x, y, z, width] to dict format. "
                            f"Road {road_idx}, node {node_idx}: z={z} will be ignored (terrain determines elevation)"
                        )
                    else:
                        x, y, width = node[0], node[1], node[2]
                    normalized_road.append({"x": float(x), "y": float(y), "width": float(width)})
                else:
                    raise ValueError(
                        f"Invalid road node format at road {road_idx}, node {node_idx}: {node}. "
                        f"Expected dict with 'x', 'y', 'width' keys or list [x, y, z, width] or [x, y, width]"
                    )
            normalized_roads.append(normalized_road)
        
        if format_converted:
            logger.info(
                "Terrain_Importer: Converted road format from list to dictionary format. "
                "This ensures compatibility with BeamNG's expected format."
            )
        
        d = dict(
            type="PeaksAndRoadImport", peaks=peaks, roads=normalized_roads, DOI=DOI, margin=margin
        )
        response = bng.connection.send(d)
        response.ack("CompletedPeaksAndRoadImport")
        logger.debug("Terrain_Importer - peaks and roads imported.")

    @staticmethod
    def reset(bng: BeamNGpy):
        """
        Resets the terrain and roads which were created by the importing methods in this class (terrain+roads and peaks+roads).

        Args:
            bng: The BeamNG instance.
        """
        logger = getLogger(f"{LOGGER_ID}.Terrain_Importer")
        logger.setLevel(DEBUG)
        d = dict(type="ResetTerrain", data={})
        response = bng.connection.send(d)
        response.ack("CompletedResetTerrain")
        logger.debug("Terrain_Importer - reset.")

    @staticmethod
    def open_close_world_editor(bng: BeamNGpy, is_open):
        """
        Toggles the world editor open/closed.

        Args:
            bng: The BeamNG instance.
            is_open: A flag which indicates if the world editor should be switched to open (True) or closed (False).
        """
        logger = getLogger(f"{LOGGER_ID}.Terrain_Importer")
        logger.setLevel(DEBUG)
        d = dict(type="OpenCloseWorldEditor", isOpen=is_open)
        response = bng.connection.send(d)
        response.ack("CompletedOpenCloseWorldEditor")
        logger.debug("Terrain_Importer - open/close world editor.")
