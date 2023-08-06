from enum import Enum
from fnmatch import fnmatch
from itertools import chain
from typing import Optional, Container, FrozenSet, Iterable, List, Dict, Any

from pydantic import BaseModel

__all__ = [
    "Feature",
    "FeatureProperties",
    "ManifestInfo",
    "Modpack",
    "ManifestIndex",
    "ModpackStatus",
    "PatternTestable",
    "RichManifest",
    "SimplePatternList",
    "SourceManifest",
    "TargetManifest",
    "FileTask",
]


class HashEqModel(BaseModel):
    def __eq__(self, other):
        return hash(self) == hash(other)


class BaseManifest(HashEqModel):
    name: str
    title: str
    version: str = "1.0"

    class Config:
        allow_mutation = False

    def __hash__(self):
        return hash((self.name, self.title, self.version))


class ManifestInfo(BaseManifest):
    location: str

    class Config:
        allow_mutation = False

    def __hash__(self):
        return hash((self.name, self.title, self.version, self.location))


class ManifestIndex(HashEqModel):
    minimumVersion: int = 3
    packages: List[ManifestInfo] = []

    class Config:
        allow_mutation = False

    def __hash__(self):
        return hash((self.minimumVersion, frozenset(self.packages)))


class SimplePatternList(HashEqModel):
    include: List[str] = []
    exclude: List[str] = []

    def __hash__(self):
        return hash(frozenset(self.include + self.exclude))

    class Config:
        allow_mutation = False


class FeatureProperties(HashEqModel):
    name: str
    description: str
    recommendation: str = "starred"
    selected: bool = False

    def __hash__(self):
        return hash((self.name, self.description, self.recommendation, self.selected))

    class Config:
        allow_mutation = False


class Feature(BaseModel):
    properties: FeatureProperties
    files: SimplePatternList
    userFiles: Optional[SimplePatternList] = SimplePatternList()

    class Config:
        allow_mutation = False


class FileTask(HashEqModel):
    type: str = "file"
    hash: str
    location: str
    to: str
    size: int
    userFile: bool
    when: Optional[Dict[Any, Any]] = None
    bundle: Optional[str] = None

    def __hash__(self):
        return hash((
            self.type,
            self.hash,
            self.location,
            self.to,
            self.size,
            self.userFile,
            self.when and (self.when['if'], frozenset(self.when['features']))
        ))

    class Config:
        allow_mutation = False
        ignore_extra = False


class RichManifest(BaseManifest):
    gameVersion: str
    launch: Dict[str, List[str]] = {"flags": []}
    librariesLocation: Optional[str] = None
    objectsLocation: str
    userFiles: SimplePatternList = SimplePatternList()

    class Config:
        allow_mutation = False


class SourceManifest(RichManifest):
    minimumVersion: int = 2
    features: List[Feature] = []
    bundles: List[str] = []

    @property
    def combined_user_files(self) -> Iterable[str]:
        return chain(self.userFiles.include, *(f.userFiles.include for f in self.features))

    class Config:
        allow_mutation = False
        ignore_extra = False


class TargetManifest(RichManifest):
    minimumVersion: int = 3
    features: List[FeatureProperties] = []
    tasks: List[FileTask] = []

    def __hash__(self):
        return hash((
            self.gameVersion,
            frozenset(self.launch['flags']),
            self.userFiles,
            self.minimumVersion,
            self.librariesLocation,
            self.objectsLocation,
            frozenset(self.features),
            frozenset(self.tasks),
        ))

    class Config:
        allow_mutation = False
        ignore_extra = False


class ModpackStatus(Enum):
    FRESH = "Fresh"
    OUTDATED = "Outdated"
    NOT_DEPLOYED = "Not deployed"
    ORPHANED = "Orphaned"
    BROKEN = "Broken"
    UNKNOWN = "Unknown"


class Modpack(BaseModel):
    name: str
    enabled: bool
    status: ModpackStatus
    source_manifest: Optional[SourceManifest] = None
    target_manifest: Optional[TargetManifest] = None

    class Config:
        allow_mutation = False
        ignore_extra = False


class PatternTestable(Container):
    __patterns: FrozenSet
    __slots__ = ('__patterns',)

    # noinspection PyProtocol
    def __contains__(self, item: str) -> bool:
        return any(fnmatch(item, pattern) for pattern in self.__patterns)

    def __init__(self, patterns: Iterable[str]):
        self.__patterns = frozenset(patterns)

    def __len__(self) -> int:
        return len(self.__patterns)
