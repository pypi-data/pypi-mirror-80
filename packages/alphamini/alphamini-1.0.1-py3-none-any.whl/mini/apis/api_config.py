import enum


@enum.unique
class LanType(enum.Enum):
    """
    语言类型

    国家的缩写

    """
    CN = 0
    EN = 1
    TW = 2
    FR = 3
    DE = 4
    EL = 5
    JA = 6
    KO = 7
    RU = 8
    CS = 9
    DA = 10
    NL = 11
    FI = 12
    BN = 13
    AF = 14
    EU = 15
    BG = 16
    BE = 17
    EO = 18
    ID = 19
    IT = 20
    GA = 21
    KY = 22
    LA = 23
    LO = 24
    MS = 25
    NO = 26
    FA = 27
    PT = 28
    SR = 29
    SO = 30
    UZ = 31
    ZU = 32
    YO = 33
    VI = 34
    TH = 35
    TG = 36
    SK = 37
    AR = 38
    MN = 39
    MY = 40
    TL = 41


@enum.unique
class ServicePlatform(enum.Enum):
    """
    服务平台

    BAIDU : 百度

    TENCENT : 腾讯

    GOOGLE : 谷歌

    """
    BAIDU = 0
    TENCENT = 1
    GOOGLE = 2
