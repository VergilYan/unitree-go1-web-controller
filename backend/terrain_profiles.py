"""
Terrain Profile System for GO1 Web Controller

This module stores terrain-specific movement profiles.
Each profile contains speed and yaw_rate settings optimized for different terrains.

Future Compatibility:
- Design allows easy addition of new terrain types
- Sensors can update terrain mode automatically in future versions
- For now: manual switching only
"""

class TerrainProfile:
    """
    Represents a terrain profile with speed and yaw_rate settings.
    """
    def __init__(self, name: str, speed_multiplier: float, yaw_rate_multiplier: float, description: str = ""):
        self.name = name
        self.speed_multiplier = speed_multiplier
        self.yaw_rate_multiplier = yaw_rate_multiplier
        self.description = description

    def __repr__(self):
        return f"TerrainProfile({self.name}, speed={self.speed_multiplier}, yaw_rate={self.yaw_rate_multiplier})"

    def to_dict(self):
        return {
            "name": self.name,
            "speed_multiplier": self.speed_multiplier,
            "yaw_rate_multiplier": self.yaw_rate_multiplier,
            "description": self.description
        }


TERRAIN_PROFILES = {
    "grass": TerrainProfile(
        name="Grass",
        speed_multiplier=0.4,
        yaw_rate_multiplier=0.25,
        description="Normal grass terrain, balanced speed and control"
    ),
    "gravel": TerrainProfile(
        name="Gravel",
        speed_multiplier=0.25,
        yaw_rate_multiplier=0.15,
        description="Loose gravel, reduced speed for stability"
    ),
    "cobblestone": TerrainProfile(
        name="Cobblestone",
        speed_multiplier=0.20,
        yaw_rate_multiplier=0.10,
        description="Uneven cobblestones, slow and careful"
    ),
    "slope": TerrainProfile(
        name="Slope",
        speed_multiplier=0.15,
        yaw_rate_multiplier=0.08,
        description="Incline/decline, very slow for safety"
    ),
    "stairs": TerrainProfile(
        name="Stairs",
        speed_multiplier=0.10,
        yaw_rate_multiplier=0.05,
        description="Stair climbing, minimum speed"
    ),
}


class TerrainManager:
    """
    Manages terrain profile selection and provides current profile settings.

    This class provides a simple interface for:
    - Getting current terrain profile
    - Setting terrain mode
    - Getting profile settings for movement commands
    """
    def __init__(self, default_terrain: str = "grass"):
        self.current_terrain = default_terrain
        self.current_profile = TERRAIN_PROFILES.get(default_terrain, TERRAIN_PROFILES["grass"])
        print(f"[Terrain] Initialized with default terrain: {self.current_terrain}")
        print(f"[Terrain] Active profile: speed={self.current_profile.speed_multiplier}, yaw_rate={self.current_profile.yaw_rate_multiplier}")

    def set_terrain(self, terrain_name: str) -> bool:
        """
        Set the current terrain mode.

        Args:
            terrain_name: Name of terrain (grass, gravel, cobblestone, slope, stairs)

        Returns:
            True if terrain was set successfully, False otherwise
        """
        terrain_lower = terrain_name.lower()
        if terrain_lower in TERRAIN_PROFILES:
            self.current_terrain = terrain_lower
            self.current_profile = TERRAIN_PROFILES[terrain_lower]
            print(f"[Terrain] Mode changed: {self.current_profile.name}")
            print(f"[Terrain] Active profile: speed={self.current_profile.speed_multiplier}, yaw_rate={self.current_profile.yaw_rate_multiplier}")
            return True
        else:
            print(f"[Terrain] ❌ Unknown terrain: {terrain_name}")
            print(f"[Terrain] Available terrains: {list(TERRAIN_PROFILES.keys())}")
            return False

    def get_current_profile(self) -> TerrainProfile:
        """
        Get the current terrain profile.

        Returns:
            Current TerrainProfile object
        """
        return self.current_profile

    def get_speed_multiplier(self) -> float:
        """
        Get speed multiplier for current terrain.

        Returns:
            Speed multiplier (0.0 to 1.0)
        """
        return self.current_profile.speed_multiplier

    def get_yaw_rate_multiplier(self) -> float:
        """
        Get yaw rate multiplier for current terrain.

        Returns:
            Yaw rate multiplier (0.0 to 1.0)
        """
        return self.current_profile.yaw_rate_multiplier

    def get_status(self) -> dict:
        """
        Get terrain system status.

        Returns:
            Dictionary with current terrain info
        """
        return {
            "current_terrain": self.current_terrain,
            "profile": self.current_profile.to_dict(),
            "available_terrains": list(TERRAIN_PROFILES.keys())
        }


if __name__ == "__main__":
    print("Terrain Profile System Test")
    print("=" * 50)

    tm = TerrainManager()

    for terrain_name in ["grass", "gravel", "cobblestone", "slope", "stairs"]:
        print(f"\nSwitching to: {terrain_name}")
        tm.set_terrain(terrain_name)
        print(f"  Speed multiplier: {tm.get_speed_multiplier()}")
        print(f"  Yaw rate multiplier: {tm.get_yaw_rate_multiplier()}")

    print("\n" + "=" * 50)
    print("All terrain profiles tested successfully!")
