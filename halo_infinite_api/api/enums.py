
import enum


class AuthenticationMethod(int, enum.Enum):
    SpartanToken = 1
    ClearanceToken = 2
    XSTSv3XboxAudience = 3
    

class ProfileSetting(str, enum.Enum):
    GameDisplayName = "GameDisplayName"
    AppDisplayName = "AppDisplayName"
    AppDisplayPicRaw = "AppDisplayPicRaw"
    GameDisplayPicRaw = "GameDisplayPicRaw"
    PublicGamerpic = "PublicGamerpic"
    ShowUserAsAvatar = "ShowUserAsAvatar"
    Gamerscore = "Gamerscore"
    Gamertag = "Gamertag"
    ModernGamertag = "ModernGamertag"
    ModernGamertagSuffix = "ModernGamertagSuffix"
    UniqueModernGamertag = "UniqueModernGamertag"
    AccountTier = "AccountTier"
    TenureLevel = "TenureLevel"
    XboxOneRep = "XboxOneRep"
    PreferredColor = "PreferredColor"
    Location = "Location"
    Bio = "Bio"
    Watermarks = "Watermarks"
    RealName = "RealName"
    RealNameOverride = "RealNameOverride"
    IsQuarantined = "IsQuarantined"


class ResultOrder(int, enum.Enum):
    Desc = 1
    Asc = 2


class AssetKind(int, enum.Enum):
    Film = 1
    Map = 2
    Playlist = 3
    Prefab = 4
    TestAsset = 5
    UgcGameVariant = 6
    MapModePair = 7
    Project = 8
    Manifest = 9
    EngineGameVariant = 10


class SearchProperty(int, enum.Enum):
    Name = 1
    Likes = 2
    Bookmarks = 3
    PlaysRecent = 4
    NumberOfObjects = 5
    DateCreatedUtc = 6
    DateModifiedUtc = 7
    DatePublishedUtc = 8
    PlaysAllTime = 9
    ParentAssetCount = 10
    AverageRating = 11
    NumberOfRatings = 12


class MatchType(int, enum.Enum):
    All = 1
    Matchmaking = 2
    Custom = 3
    Local = 4


class Outcome(int, enum.Enum):
    Tie = 1
    Win = 2
    Loss = 3
    DidNotFinish = 4


class LifecycleMode(int, enum.Enum):
    Custom = 1
    Matchmade = 3


class GameVariantCategory(int, enum.Enum):
    MultiplayerSlayer = 6
    MultiplayerAttrition = 7
    MultiplayerElimination = 8
    MultiplayerFiesta = 9
    MultiplayerStrongholds = 11
    MultiplayerBastion = 12
    MultiplayerTotalControl = 14
    MultiplayerCtf = 15
    MultiplayerAssault = 16
    MultiplayerExtraction = 17
    MultiplayerOddball = 18
    MultiplayerStockpile = 19
    MultiplayerJuggernaut = 20
    MultiplayerEscort = 23
    MultiplayerGunGame = 24
    MultiplayerGrifball = 25
    TestEngine = 32
    MultiplayerLandGrab = 39


class PlaylistExperience(int, enum.Enum):
    Arena = 2
    BigTeamBattle = 3
    Featured = 5


class PlayerType(int, enum.Enum):
    Human = 1
    Bot = 2


class BotDifficulty(int, enum.Enum):
    # TODO these are guesses
    NA = 0
    Recruit = 1
    Marine = 2
    ODST = 3
    Spartan = 4

