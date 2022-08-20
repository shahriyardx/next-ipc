from dataclasses import dataclass

__version__ = "0.0.1b1"


@dataclass
class VersionInfo:
    major: int
    minor: int
    micro: int
    releaselevel: str
    serial: int


version_info = VersionInfo(0, 0, 1, "beta", 1)
