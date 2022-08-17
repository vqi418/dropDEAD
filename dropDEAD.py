import os
import itertools
from internetarchive.session import ArchiveSession
from internetarchive.search import Search
from internetarchive import download
from internetarchive import get_item
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
import PySimpleGUI as sg

s = ArchiveSession()

sg.theme("DarkBlack")

LISTBOX_SELECT_MODE_MULTIPLE = "multi"

IDS = []
IDS2 = {}

cprint = sg.cprint

FULL_DATE_SEARCH = "neutral"
BANDID = ""
VENUE = ""
VENUE_1 = ""
VENUE_AVAIL = "ON"
DATE_AVAIL = "ON"
RECORDING = ""
REC_AVAIL = "ON"
TOPICS = ""
TOPICS_AVAIL = "ON"
CITY = ""
CITY_AVAIL = "ON"
SOURCE = ""
SOURCE_AVAIL = "ON"
COLLECTION = ""
COLLECTION_AVAIL = "ON"
# LINEAGE_AVAIL = "ON"
AUDIENCE = "OFF"
SOUNDBOARD = "OFF"
YEAR = ""
MONTH = ""
DAY = ""

DEAD_BASE64 = (
    b"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXM"
    b"AAAG0AAABtAFMIk34AAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcG"
    b"Uub3Jnm+48GgAAB31JREFUWIWNlnlwleUVxn/fcrfc3CUhO1lISIKQ"
    b"QCABoRZRkC1FXKjQcaS2QmunSu3IFGGmMrWLyjJWSgtjibS0WMCyS"
    b"xUCgjgDFgRalrAFaBrSQBbIvTd3v/db+sclcAlJbp6Z95/vnPc873"
    b"m+9z3nCPQfo6zwnSQYH4ZSAWQdJEAHgiZoUuCkC/4OHAGU/gQVEt"
    b"glM8wzwlsFYJ4FzjIQSwBDnFMY+B9wCfTPwHMMTApsUmE1cLYvAr"
    b"kP2ygH7JgAA34Ktqw+HE1AIVAH2gXgm+V8PmmCWP/mWvEImI6B/w"
    b"Wgvd8HSIIfOmDFqljGfUIH9oO+MQ3vjBnGlvWVZsFokicuXhUEx"
    b"hogZSLUXoDIXFBqu+8XeyD/0UBYubMf5ACngRoI48BUNEhzGoz"
    b"SQJ8v4jtziUeh2AxmGUamgXkbSDMTHWC0A5ZtBEdyP8ibgK3gz"
    b"SkXQj+bb20vKy82lJaPStqyL9QuS6qWZP6oDbZokK3By8mQ/F"
    b"eQp8THiL+ENidcqIHcoQmIrwJrBNziKFH//pykQMmQAmteYYl"
    b"TkmVuNjcqt1tutNVfaR3w2gqDLxSZ6YRhUmynG1jXDoFhwK37FEi"
    b"FDa9CRl/kbcDroM8SIXOaEHppjkF1OkxSJBqJ3Gq9qSjRKJlZufL15"
    b"rD06jKDPxSZlXqPHMAJTE6BpM3dFagshIOfgDPRu4zcUeAyUANR"
    b"MogsX2jylI0ot2Xm5Nl27/qy/ZVfh2VFne2Ewl7C1bigeQbwT+"
    b"FO9rXvwNTxCci70AH8XKSz4lmD+6npqXJ55ZgcQRTZue1Qx2vLA0Z"
    b"FsUiQ5QebDDZzbBUAmXciXAN2HAL/EwKQmQGXDvYje4BaUP+Sg2/JT"
    b"6zekVXlAzJy8iwAPo8b1+02r8cTDLW0+9SbrX6p/j9+8x+365K"
    b"mDddgZvL9r36VC9zDZQmemgnGROSdwDIRV9FsU/C9KSmGssoxuU"
    b"aj6a492eEk2eG05YGtyO/Vt2492lKzwxjRtMkOqOqh3pSZ4dh"
    b"kORW+/Rgk9UV+ALQ/5xJ6/QcSDhspiqq6z379VZMsS86SspE2q81+1"
    b"7e1+br/nd/VtW7aa0jT9e/a78neHYMtcPZZIQUaP4N8Wy9uO2MrI"
    b"NvxKwr8N4LNPoDIe4uTPZXjxg202Z0igKZpnDp+qv3lpe3BppZ8J"
    b"8yyg7GPtELA6kbBAR1HIaUvBSBWcj+AUNM4yf3KS6l6xcPfyDYY"
    b"YgShYIDt24+0Ln7fJ4XCQoogZHSAKAsgaLooQ0EyTODBAy2/LT9Q"
    b"i3tAAFgk4n18ntk1d0p+cvGw4amCELs10WiEhvqLofwcc7TmV0"
    b"kAt4IBj/Xw12Hp41pRQB8PjCfWubtDkPrqhgA0AgutdC55w+Ia+"
    b"0hFekZ27n33xWAwMrSiygzkRqMRDn/xr1tvryN4vSXPoOtPOxOIq"
    b"8sqqBo9dCXgCOjrBwnetxcYGTZiRL4lySp4PS7MFisG4z05dV2nse"
    b"Gaf+Waq96tB7Bq2jQrVCQQVwX0sJAG57fAsPh+rwM1wFoJfdpow"
    b"ZeSLEVMJkGoKNf1oaUD5IoxjzhEKSZpp8elbfzb8fZ3PoxawpFiI1"
    b"SboT+tzAWsr5NMUFEKVcVxJgXIAb6nI0xqxtTQoBk7BorBJ6cO1Ec"
    b"8PC5VFEWi0Qj1daej23f9m4/349NUoyrLbhVORFX1gBlOqGASIYu"
    b"eB6/LOlzZJADTp8Lm38Y6xQNYC0HtGaP7xecL5NKyivS7Kuk6ihJFU"
    b"1V0TaPlRpP6aW29f8UGMegP5plhhqOXkHewpQMuPScDnx8HNcD91U"
    b"gHlgv4i+aZO2dUD7LmDy61q4qCJMfurSAIGAxG/KFOavefanvr96HI"
    b"jVvpyfBkJmQnkD8IXNeBryRAs0BOElRW3HkrCvAGBBqHII8tl903Wz"
    b"qjDVevdkp6QEjLzDYBRCNhjh092bZg6eX2dVuxegPV6TDdAr2VtHgc"
    b"CkDLMlC+7Po56alweR+kJAHNQF2c+y5QnlloOffc7EdHWW12fB43u"
    b"3cfDi16X4tEojYLPG+I/ev+oBP4oA0CBUCoqzoEJDDdhjETwGgHiu+s"
    b"QmC1jGf+XLtYWPKQE0AyyJhNumIRO8STF8Oqrp8HHBJkJCBXgQ1"
    b"u8M4D/TzE9UcfvLsP5oyDhybHla1DoD/xuHwtr2hwmcfVwZ69de7"
    b"Ne/zaqYuKUVGGRGB0Kgyi50rSHf/wQeefQP2k60t8JYy6YfIv4HQ2ZH"
    b"ZNxOvA9ZtvWaxpGdmW/bWnvCs/dEnNbSYrzDckzrgLOrDXD/UnILgo"
    b"3tL92C0eqP4xdJwDrgCGLFyZ2WmpQb9fz8vQPS8+LV8QxaAXdkdjX"
    b"SIRFGBLJ5zbA/6pgBZv7W0OGeqEfZmQvmCJ+WR+ljRk+0Hl9EefisW"
    b"alpECE1NisifCDWCbG0JrIPBmTx59DUJ2I/xhaImknrlirIYiCzx"
    b"m75/srcAXHmhsg+ALwInePBNNYpPAuhSogjIRBltjz83ebWsYaAEa"
    b"w3DGD6GbEPolqNuIXYBe0Z85FCAVqAZrNQhVoGaAIIEmgKABfpDPQa"
    b"gWoruBhn7G5f8Fob1bA357AgAAAABJRU5ErkJggg=="
)

BND_COL1 = sg.Column(
    [
        [
            sg.Radio(
                "Grateful Dead",
                "RADIO1",
                text_color="#E7D541",
                circle_color="DarkRed",
                font=("Times New Roman", 12, "normal"),
                key="GratefulDead",
                pad=(3, 3),
            )
        ],
        [
            sg.Radio(
                "Little Feat",
                "RADIO1",
                text_color="#E7D541",
                circle_color="DarkRed",
                font=("Times New Roman", 12, "normal"),
                key="LittleFeat",
                pad=(3, 3),
            )
        ],
        [
            sg.Radio(
                "Dead and Company",
                "RADIO1",
                text_color="#E7D541",
                circle_color="DarkRed",
                font=("Times New Roman", 12, "normal"),
                key="DeadAndCompany",
                pad=(3, 3),
            )
        ],
        [
            sg.Radio(
                "Billy Strings",
                "RADIO1",
                text_color="#E7D541",
                circle_color="DarkRed",
                font=("Times New Roman", 12, "normal"),
                key="BillyStrings",
                pad=(3, 3),
            )
        ],
        [
            sg.Radio(
                "Tedeschi Trucks Band",
                "RADIO1",
                text_color="#E7D541",
                circle_color="DarkRed",
                font=("Times New Roman", 12, "normal"),
                key="TedeschiTrucksBand",
                pad=(3, 3),
            )
        ],
        [
            sg.Radio(
                "North Mississippi Allstars",
                "RADIO1",
                text_color="#E7D541",
                circle_color="DarkRed",
                font=("Times New Roman", 12, "normal"),
                key="NorthMississippiAllstars",
                pad=(3, 3),
            )
        ],
        [
            sg.Radio(
                "Phil Lesh and Friends",
                "RADIO1",
                text_color="#E7D541",
                circle_color="DarkRed",
                font=("Times New Roman", 12, "normal"),
                key="PhilLeshandFriends",
                pad=(3, 3),
            )
        ],
    ]
)

BND_COL2 = sg.Column(
    [
        [
            sg.Radio(
                "Joe Russos Almost Dead",
                "RADIO1",
                text_color="#E7D541",
                circle_color="DarkRed",
                font=("Times New Roman", 12, "normal"),
                key="JoeRussosAlmostDead",
                pad=(3, 3),
            )
        ],
        [
            sg.Radio(
                "Yonder Mountain String Band",
                "RADIO1",
                text_color="#E7D541",
                circle_color="DarkRed",
                font=("Times New Roman", 12, "normal"),
                key="YonderMountainStringBand",
                pad=(3, 3),
            )
        ],
        [
            sg.Radio(
                "Railroad Earth",
                "RADIO1",
                text_color="#E7D541",
                circle_color="DarkRed",
                font=("Times New Roman", 12, "normal"),
                key="RailroadEarth",
                pad=(3, 3),
            )
        ],
        [
            sg.Radio(
                "MaxCreek",
                "RADIO1",
                text_color="#E7D541",
                circle_color="DarkRed",
                font=("Times New Roman", 12, "normal"),
                key="MaxCreek",
                pad=(3, 3),
            )
        ],
        [
            sg.Radio(
                "Ratdog",
                "RADIO1",
                text_color="#E7D541",
                circle_color="DarkRed",
                font=("Times New Roman", 12, "normal"),
                key="Ratdog",
                pad=(3, 3),
            )
        ],
        [
            sg.Radio(
                "Dark Star Orchestra",
                "RADIO1",
                text_color="#E7D541",
                circle_color="DarkRed",
                font=("Times New Roman", 12, "normal"),
                key="DarkStarOrchestra",
                pad=(3, 3),
            )
        ],
        [
            sg.Radio(
                "Blues Traveler",
                "RADIO1",
                text_color="#E7D541",
                circle_color="DarkRed",
                font=("Times New Roman", 12, "normal"),
                key="BluesTraveler",
                pad=(3, 3),
            )
        ],
    ]
)

BND_COL3 = sg.Column(
    [
        [
            sg.Radio(
                "Furthur",
                "RADIO1",
                text_color="#E7D541",
                circle_color="DarkRed",
                font=("Times New Roman", 12, "normal"),
                key="Furthur",
                pad=(3, 3),
            )
        ],
        [
            sg.Radio(
                "Leftover Salmon",
                "RADIO1",
                text_color="#E7D541",
                circle_color="DarkRed",
                font=("Times New Roman", 12, "normal"),
                key="LeftoverSalmon",
                pad=(3, 3),
            )
        ],
        [
            sg.Radio(
                "Drive-By Truckers",
                "RADIO1",
                text_color="#E7D541",
                circle_color="DarkRed",
                font=("Times New Roman", 12, "normal"),
                key="Drive-ByTruckers",
                pad=(3, 3),
            )
        ],
        [
            sg.Radio(
                "Derek Trucks Band",
                "RADIO1",
                text_color="#E7D541",
                circle_color="DarkRed",
                font=("Times New Roman", 12, "normal"),
                key="DerekTrucksBand",
                pad=(3, 3),
            )
        ],
        [
            sg.Radio(
                "Bob Weir",
                "RADIO1",
                text_color="#E7D541",
                circle_color="DarkRed",
                font=("Times New Roman", 12, "normal"),
                key="BobWeir",
                pad=(3, 3),
            )
        ],
        [
            sg.Radio(
                "New Riders of the Purple Sage",
                "RADIO1",
                text_color="#E7D541",
                circle_color="DarkRed",
                font=("Times New Roman", 12, "normal"),
                key="NewRidersofthePurpleSage",
                pad=(3, 3),
            )
        ],
        [
            sg.Radio(
                "String Cheese Incident",
                "RADIO1",
                text_color="#E7D541",
                circle_color="DarkRed",
                font=("Times New Roman", 12, "normal"),
                key="StringCheeseIncident",
                pad=(3, 3),
            )
        ],
    ]
)

BND_FRM_LAYOUT = [[BND_COL1, BND_COL2, BND_COL3]]

COL1 = sg.Column(
    [
        [
            sg.Frame(
                "Bands",
                BND_FRM_LAYOUT,
                title_color="Red",
                background_color="#03020f",
                border_width=3,
            )
        ]
    ]
)

COL2 = sg.Column(
    [
        [
            sg.Frame(
                "Date",
                [
                    [
                        sg.Column(
                            [
                                [
                                    sg.Text(
                                        "Please enter the Year, Month and Day of the Show:\n (to list all "
                                        "shows in a Year, enter the Year only)\n "
                                        "YYYY  -  MM  -  DD",
                                        text_color="#E7D541",
                                    )
                                ],
                                [
                                    sg.Text(
                                        "Yearly show listings are presented as filenames, \ndue to "
                                        "excessive processing time and "
                                        "the fact \nI do not know what I am doing.",
                                        font=("Times New Roman", 9, "italic"),
                                        text_color="#E7D541",
                                        pad=((95, 0), (5, 5)),
                                    )
                                ],
                                [
                                    sg.Input(
                                        s=(5, 2),
                                        text_color="#E7D541",
                                        tooltip="Year",
                                        border_width=3,
                                        enable_events=True,
                                        key="-YEAR-",
                                        pad=((125, 15), (5, 5)),
                                    ),
                                    sg.Input(
                                        s=(3, 2),
                                        text_color="#E7D541",
                                        tooltip="Month",
                                        border_width=3,
                                        enable_events=True,
                                        key="-MONTH-",
                                        pad=(15, 5),
                                    ),
                                    sg.Input(
                                        s=(3, 2),
                                        text_color="#E7D541",
                                        tooltip="Day",
                                        border_width=3,
                                        enable_events=True,
                                        key="-DAY-",
                                        pad=(15, 5),
                                    ),
                                ],
                            ]
                        )
                    ]
                ],
                title_color="Red",
                background_color="#03020f",
                border_width=3,
            )
        ],
        [
            sg.Button(
                "Search",
                border_width=3,
                button_color=("Red", "#2C2D2F"),
                font=("Times New Roman", 14, "bold"),
                bind_return_key=True,
                key="-SETDATE-",
            )
        ],
    ]
)

FR_COL1 = sg.Column(
    [
        [sg.Image(size=(0, 0))],
        [
            sg.Column(
                [
                    [
                        sg.Text(
                            "Select the show you would like to download:",
                            text_color="#E7D541",
                        )
                    ],
                    [
                        sg.Listbox(
                            IDS,
                            select_mode="multi",
                            enable_events=False,
                            size=(70, 10),
                            text_color="#E7D541",
                            background_color="#03020f",
                            highlight_background_color="Black",
                            highlight_text_color="Red",
                            key="-LISTBOX-",
                        )
                    ],
                    [
                        sg.Button(
                            "Download",
                            border_width=3,
                            button_color=("Red", "#2C2D2F"),
                            font=("Times New Roman", 14, "bold"),
                            key="-GET_SHOW-",
                        )
                    ],
                ]
            )
        ],
    ],
    key="-COL1-",
    visible=False,
)

FR_COL2 = sg.Column(
    [
        [sg.Image(size=(0, 0))],
        [
            sg.Column(
                [
                    [
                        sg.Frame(
                            "File Type and Location",
                            [
                                [
                                    sg.Column(
                                        [
                                            [
                                                sg.Text(
                                                    "Would you like to download Flac files or MP3?\n(GD "
                                                    "soundboard shows can only be downloaded in MP3, "
                                                    "\n by request of the band)",
                                                    text_color="#E7D541",
                                                )
                                            ],
                                            [
                                                sg.Radio(
                                                    "Flac",
                                                    "RADIO2",
                                                    circle_color="DarkRed",
                                                    font=(
                                                        "Times New Roman",
                                                        12,
                                                        "normal",
                                                    ),
                                                    key="-FLAC-",
                                                    pad=(120, 5),
                                                    background_color="#03020f",
                                                ),
                                                sg.Radio(
                                                    "MP3",
                                                    "RADIO2",
                                                    circle_color="DarkRed",
                                                    font=(
                                                        "Times New Roman",
                                                        12,
                                                        "normal",
                                                    ),
                                                    key="-MP3-",
                                                    pad=(5, 5),
                                                    background_color="#03020f",
                                                ),
                                            ],
                                            [
                                                sg.HorizontalSeparator(
                                                    color="DarkRed", pad=(5, 20)
                                                )
                                            ],
                                            [
                                                sg.Text(
                                                    "Please browse to the download directory:",
                                                    text_color="#E7D541",
                                                )
                                            ],
                                            [
                                                sg.In(
                                                    s=(40, 60),
                                                    text_color="#E7D541",
                                                    key="-FOLD-",
                                                ),
                                                sg.FolderBrowse(
                                                    button_text="Browse",
                                                    button_color=("Red", "#2C2D2F"),
                                                    font=(
                                                        "Times New Roman",
                                                        14,
                                                        "bold",
                                                    ),
                                                    key="-DIR-",
                                                ),
                                            ],
                                        ]
                                    )
                                ]
                            ],
                            title_color="Red",
                            background_color="#03020f",
                            border_width=3,
                        )
                    ]
                ]
            )
        ],
    ],
    key="-COL2-",
    visible=False,
)

FRAME1_LAYOUT = [[FR_COL1, FR_COL2]]

BOX_LAYOUT = sg.Column(
    [
        [
            sg.Frame(
                "Shows",
                FRAME1_LAYOUT,
                title_color="Red",
                background_color="#03020f",
                border_width=3,
                key="-BOXFRAME-",
                visible=False,
            )
        ]
    ],
    key="-BOXCOL-",
    visible=False,
)

PRNT_WIN = sg.Column(
    [
        [sg.Image(size=(0, 0))],
        [
            sg.Frame(
                "Progress",
                [
                    [
                        sg.Column(
                            [
                                [
                                    sg.Multiline(
                                        key="-ML-",
                                        border_width=3,
                                        size=(100, 10),
                                        auto_size_text=True,
                                        autoscroll=True,
                                        background_color="#03020f",
                                        text_color="#E7D541",
                                        font=("Times New Roman", 14, "bold"),
                                        reroute_stdout=True,
                                        reroute_stderr=True,
                                        reroute_cprint=True,
                                        echo_stdout_stderr=True,
                                        write_only=True,
                                        auto_refresh=True,
                                    )
                                ]
                            ]
                        )
                    ]
                ],
                title_color="Red",
                background_color="#03020f",
                border_width=3,
            )
        ],
    ],
    key="-INFOBOX-",
    visible=False,
)

LAYOUT = [[COL1, COL2], [PRNT_WIN], [BOX_LAYOUT]]

WINDOW = sg.Window(
    "dropDEAD - Archive Downloader",
    LAYOUT,
    auto_size_text=True,
    relative_location=(0, -150),
    font=("Times New Roman", 14, "normal"),
    border_depth=4,
    text_justification="center",
    grab_anywhere=True,
    force_toplevel=False,
    keep_on_top=False,
    element_justification="center",
    icon=DEAD_BASE64,
)

sg.cprint_set_output_destination(WINDOW, "-ML-")


def _clean_(filename):
    return (
        str(filename)
        .replace("->", "")
        .replace(">", "")
        .replace("/", " - ")
        .replace("\\", " - ")
        .replace("*", "")
        .replace("!", "")
        .replace("'", "")
    )


def _strip_(doc_name):
    return str(doc_name).strip("'").strip("][")


while True:

    event, values = WINDOW.read()
    print(event, values)
    CHOSEN = values
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    if (
        event == "-YEAR-"
        and values["-YEAR-"]
        and values["-YEAR-"][-1] not in "0123456789"
    ):
        WINDOW["-YEAR-"].update(values["-YEAR-"][:-1])
    if event == "-YEAR-" and len(values["-YEAR-"]) > 4:
        WINDOW["-YEAR-"].update(values["-YEAR-"][:-1])
    if (
        event == "-MONTH-"
        and values["-MONTH-"]
        and values["-MONTH-"][-1] not in "0123456789"
    ):
        WINDOW["-MONTH-"].update(values["-MONTH-"][:-1])
    if event == "-MONTH-" and len(values["-MONTH-"]) > 2:
        WINDOW["-MONTH-"].update(values["-MONTH-"][:-1])
    if event == "-DAY-" and values["-DAY-"] and values["-DAY-"][-1] not in "0123456789":
        WINDOW["-DAY-"].update(values["-DAY-"][:-1])
    if event == "-DAY-" and len(values["-DAY-"]) > 2:
        WINDOW["-DAY-"].update(values["-DAY-"][:-1])
    if event == "-SETDATE-":
        XIDS = []
        IDS = []
        IDS2 = {}
        WINDOW["-YEAR-"].Update("")
        WINDOW["-MONTH-"].Update("")
        WINDOW["-DAY-"].Update("")
        WINDOW["-LISTBOX-"].Update("")
        WINDOW["-FOLD-"].Update("")
        WINDOW["-INFOBOX-"].hide_row()
        WINDOW["-INFOBOX-"].Update(visible=False)
        WINDOW["-BOXCOL-"].unhide_row()
        WINDOW["-BOXCOL-"].Update(visible=True)
        WINDOW["-COL1-"].unhide_row()
        WINDOW["-COL1-"].Update(visible=True)
        WINDOW["-COL2-"].unhide_row()
        WINDOW["-COL2-"].Update(visible=True)
        WINDOW["-BOXFRAME-"].Update(visible=True)
        BAND_RANGE = dict(itertools.islice(CHOSEN.items(), 0, 20, 1))
        for key, value in BAND_RANGE.items():
            if True is value:
                BANDID = key
        YEAR = CHOSEN.get("-YEAR-")
        MONTH = CHOSEN.get("-MONTH-")
        DAY = CHOSEN.get("-DAY-")
        SHOWDATE = YEAR + "-" + MONTH + "-" + DAY
        QUERY1 = "collection:" + BANDID
        QUERY2 = " title:" + SHOWDATE
        SEARCH = Search(s, (QUERY1 + QUERY2))
        for result in SEARCH:
            XIDS.append(result["identifier"])
        # for i in XIDS:
        #     if MONTH != "":
        #         ITEM = get_item(i)
        #         DATE = ITEM.item_metadata["metadata"]["date"]
        #         try:
        #             VENUE_1 = ITEM.item_metadata["metadata"]["venue"]
        #         except KeyError:
        #             VENUE_AVAIL = "OFF"
        #         finally:
        #             try:
        #                 TOPICS = ITEM.item_metadata["metadata"]["subject"]
        #             except KeyError:
        #                 SUBJECT_AVAIL = "OFF"
        #             else:
        #                 TOPICS = str(TOPICS)
        #                 TOPICS = _clean_(TOPICS)
        #             finally:
        #                 if VENUE_AVAIL == "ON" and SUBJECT_AVAIL == "ON":
        #                     SHOW = DATE + "-" + VENUE_1 + " - " + TOPICS
        #                 elif VENUE_AVAIL == "OFF" and SUBJECT_AVAIL == "ON":
        #                     SHOW = DATE + " - " + TOPICS
        #                 elif VENUE_AVAIL == "ON" and SUBJECT_AVAIL == "OFF":
        #                     SHOW = DATE + "-" + VENUE_1
        #                 else:
        #                     SHOW = DATE
        for i in XIDS:
            if MONTH != "":
                AUDIENCE = "OFF"
                SOUNDBOARD = "OFF"
                ITEM = get_item(i)
                try:
                    DATE = ITEM.item_metadata["metadata"]["date"]
                except KeyError:
                    DATE = YEAR + "-" + MONTH + "-" + DAY
                    DATE_AVAIL = "OFF"
                try:
                    VENUE_1 = ITEM.item_metadata["metadata"]["venue"]
                except KeyError:
                    VENUE_AVAIL = "OFF"
                else:
                    VENUE_1 = str(VENUE_1)
                    VENUE_1 = _clean_(VENUE_1)
                try:
                    TOPICS = ITEM.item_metadata["metadata"]["subject"]
                except KeyError:
                    TOPICS_AVAIL = "OFF"
                else:
                    TOPICS = str(TOPICS)
                    TOPICS = _clean_(TOPICS)
                    if "audience" in TOPICS.lower():
                        AUDIENCE = "ON"
                        TOPICS = TOPICS.replace("Audience;", "")
                try:
                    CITY = ITEM.item_metadata["metadata"]["coverage"]
                except KeyError:
                    CITY_AVAIL = "OFF"
                else:
                    CITY = str(CITY)
                    CITY = _clean_(CITY)
                try:
                    SOURCE = ITEM.item_metadata["metadata"]["source"]
                except KeyError:
                    SOURCE_AVAIL = "OFF"
                else:
                    SOURCE = str(SOURCE)
                    SOURCE = _clean_(SOURCE)
                    if "sbd" or "soundboard" in SOURCE.lower():
                        SOUNDBOARD = "ON"
                try:
                    COLLECTION = ITEM.item_metadata["metadata"]["collection"]
                except KeyError:
                    COLLECTION_AVAIL = "OFF"
                else:
                    COLLECTION = str(COLLECTION)
                    COLLECTION = _clean_(COLLECTION)
                    if "stream_only" in COLLECTION.lower():
                        SOUNDBOARD = "ON"
                # try:
                #     LINEAGE = ITEM.item_metadata["metadata"]["lineage"]
                # except KeyError:
                #     LINEAGE_AVAIL = "OFF"
                # else:
                #     LINEAGE = str(LINEAGE)
                #     LINEAGE = _clean_(LINEAGE)
                # try:
                #     TITLE = ITEM.item_metadata["metadata"]["title"]
                # except KeyError:
                #     TITLE_AVAIL = "OFF"
                # else:
                #     TITLE = str(TITLE)
                #     TITLE = _clean_(TITLE)
                finally:
                    if SOUNDBOARD == "ON":
                        RECORDING = "Soundboard"
                        TOPICS = TOPICS.replace("Soundboard;", "")
                    if AUDIENCE == "ON":
                        RECORDING = "Audience"
                    if SOUNDBOARD == "OFF" and AUDIENCE == "OFF":
                        RECORDING = "-"
                    if (
                        VENUE_AVAIL == "ON"
                        and CITY_AVAIL == "ON"
                        and TOPICS_AVAIL == "ON"
                    ):
                        SHOW = (
                            DATE
                            + "-"
                            + VENUE_1
                            + ", "
                            + CITY
                            + " "
                            + "["
                            + RECORDING
                            + "]"
                            + " - "
                            + TOPICS
                        )
                    elif (
                        VENUE_AVAIL == "OFF"
                        and CITY_AVAIL == "ON"
                        and TOPICS_AVAIL == "ON"
                    ):
                        SHOW = (
                            DATE
                            + ", "
                            + CITY
                            + " "
                            + "["
                            + RECORDING
                            + "]"
                            + " - "
                            + TOPICS
                        )
                    elif (
                        VENUE_AVAIL == "ON"
                        and CITY_AVAIL == "OFF"
                        and TOPICS_AVAIL == "ON"
                    ):
                        SHOW = (
                            DATE
                            + "-"
                            + VENUE_1
                            + " "
                            + "["
                            + RECORDING
                            + "]"
                            + " - "
                            + TOPICS
                        )
                    elif (
                        VENUE_AVAIL == "ON"
                        and CITY_AVAIL == "ON"
                        and TOPICS_AVAIL == "OFF"
                    ):
                        SHOW = (
                            DATE
                            + "-"
                            + VENUE_1
                            + ", "
                            + CITY
                            + " "
                            + "["
                            + RECORDING
                            + "]"
                        )
                    elif (
                        VENUE_AVAIL == "OFF"
                        and CITY_AVAIL == "OFF"
                        and TOPICS_AVAIL == "ON"
                    ):
                        SHOW = DATE + " " + "[" + RECORDING + "]" + " - " + TOPICS
                    elif (
                        VENUE_AVAIL == "ON"
                        and CITY_AVAIL == "OFF"
                        and TOPICS_AVAIL == "OFF"
                    ):
                        SHOW = DATE + "-" + VENUE_1 + " " + "[" + RECORDING + "]"
                    else:
                        try:
                            SHOW = DATE + " " + "[" + RECORDING + "]"
                        except NameError:
                            REC_AVAIL = "OFF"
                            try:
                                SHOW = ITEM.item_metadata["metadata"]["title"]
                            except KeyError:
                                SHOW = ITEM
                    IDS.append(SHOW)
                    IDS2[SHOW] = i
                    FULL_DATE_SEARCH = "ON"
            else:
                IDS.append(i)
                FULL_DATE_SEARCH = "OFF"
        WINDOW["-LISTBOX-"].Update(IDS)
    if event == "-GET_SHOW-":
        WINDOW["-ML-"].Update("")
        WINDOW["-BOXFRAME-"].Update(visible=False)
        WINDOW["-BOXCOL-"].Update(visible=False)
        WINDOW["-BOXCOL-"].hide_row()
        WINDOW["-COL1-"].Update(visible=False)
        WINDOW["-COL2-"].Update(visible=False)
        WINDOW["-COL1-"].hide_row()
        WINDOW["-COL2-"].hide_row()
        WINDOW["-INFOBOX-"].unhide_row()
        WINDOW["-INFOBOX-"].Update(visible=True)

        DOWN_INFO = values
        DFORMS = (
            ["Text", "Flac", "24bit Flac", "Item Tile", "JPEG", "JPEG Thumb"]
            if DOWN_INFO.get("-FLAC-") is True
            else ["Text", "VBR MP3", "Item Tile", "JPEG", "JPEG Thumb"]
        )
        SHOW_ID1 = DOWN_INFO.get("-LISTBOX-")
        SHOW_ID2 = _strip_(SHOW_ID1)
        if IDS2 == {}:
            SHOW_ID = _clean_(SHOW_ID2)
        else:
            SHOW_ID3 = _clean_(SHOW_ID2)
            SHOW_ID = IDS2[SHOW_ID3]
        LOCALDIR = DOWN_INFO.get("-DIR-")
        ITEM = get_item(SHOW_ID)
        METADATA = ITEM.item_metadata
        CREATOR = METADATA["metadata"]["creator"]
        try:
            DATE = METADATA["metadata"]["date"]
        except KeyError:
            DATE = YEAR + "-" + MONTH + "-" + DAY
        try:
            VENUE = METADATA["metadata"]["venue"]
        except KeyError:
            ALBUM = DATE + " - " + CREATOR
        else:
            ALBUM = DATE + " - " + VENUE
        LOCALDIR = LOCALDIR.rstrip("//")
        download(
            SHOW_ID,
            formats=DFORMS,
            verbose=True,
            ignore_existing=True,
            destdir=LOCALDIR,
            retries=3,
        )
        SOURCE_DIR = LOCALDIR + "/" + SHOW_ID

        MBID = ""

        for name in os.listdir(SOURCE_DIR):
            if BANDID == "GratefulDead":
                MBID = "6faa7ca7-0d99-4a5e-bfa6-1fd5037520c6"
            elif BANDID == "LittleFeat":
                MBID = "9b106beb-12b5-4525-8025-42e295a2b90a"
            elif BANDID == "DeadAndCompany":
                MBID = "94f8947c-2d9c-4519-bcf9-6d11a24ad006"
            elif BANDID == "BillyStrings":
                MBID = "640db492-34c4-47df-be14-96e2cd4b9fe4"
            elif BANDID == "TedeschiTrucksBand":
                MBID = "e33e1ccf-a3b9-4449-a66a-0091e8f55a60"
            elif BANDID == "NorthMississippiAllstars":
                MBID = "62fa3eb2-1b73-4029-ba35-16ab66d29d02"
            elif BANDID == "PhilLeshandFriends":
                MBID = "ffb7c323-5113-4bb0-a5f7-5b657eec4083"
            elif BANDID == "JoeRussosAlmostDead":
                MBID = "84a69823-3d4f-4ede-b43f-17f85513181a"
            elif BANDID == "YonderMountainStringBand":
                MBID = "76fda896-7c2a-4e5e-a45b-d40acfb2080c"
            elif BANDID == "RailroadEarth":
                MBID = "b2e2abfa-fb1e-4be0-b500-56c4584f41cd"
            elif BANDID == "MaxCreek":
                MBID = "75f27492-3018-4b1e-aa04-60c31059a5c5"
            elif BANDID == "Ratdog":
                MBID = "73c5a9bc-3e0d-45e6-a981-ba67435e1f58"
            elif BANDID == "DarkStarOrchestra":
                MBID = "e477d9c0-1f35-40f7-ad1a-b915d2523b84"
            elif BANDID == "BluesTraveler":
                MBID = "6b28ecf0-94e6-48bb-aa2a-5ede325b675b"
            elif BANDID == "Furthur":
                MBID = "39e07389-bbc0-4629-9ceb-dbd0d13b85fe"
            elif BANDID == "LeftoverSalmon":
                MBID = "3020be1d-3c41-4e42-911b-ca5e96489300"
            elif BANDID == "Drive-ByTruckers":
                MBID = "8eae1e0a-1696-4532-9e3c-0a072217ef4c"
            elif BANDID == "DerekTrucksBand":
                MBID = "bb110dbc-8daa-407f-a04b-f569e7a5ee7e"
            elif BANDID == "BobWeir":
                MBID = "c8a63580-9e6b-4852-bf93-c09760035e76"
            elif BANDID == "NewRidersofthePurpleSage":
                MBID = "64c8fe79-1f93-483f-aace-b6a6e379e7d2"
            elif BANDID == "StringCheeseIncident":
                MBID = "cff95140-6d57-498a-8834-10eb72865b29"
            else:
                cprint(
                    "Woooooah, hold on, gimmie time to think!!!! Something "
                    "has gone terribly wrong",
                    c="Red",
                    b="Black",
                    key="-ML-",
                )
            if name.endswith(".flac"):
                PATH = os.path.join(SOURCE_DIR, name)
                audio = FLAC(PATH)
                for file_data in METADATA["files"]:
                    if file_data["name"] == name:
                        DATA_NAME = file_data["name"]
                        F1TRACK = file_data["track"]
                        FTRACK = int(F1TRACK)
                        TRACKNUMBER = f"{FTRACK:02d}"
                        SONG_NAME = file_data["title"]
                        TRACK_TITLE = TRACKNUMBER + " " + _clean_(SONG_NAME) + ".flac"
                        audio["title"] = SONG_NAME
                        audio["artist"] = CREATOR
                        audio["album"] = ALBUM
                        audio["tracknumber"] = TRACKNUMBER
                        audio["date"] = DATE
                        audio["albumartist"] = CREATOR
                        audio["albumartistsort"] = CREATOR
                        audio["artistsort"] = CREATOR
                        audio["musicbrainz_artistid"] = MBID
                        audio["originaldate"] = DATE
                        audio.save()
                        os.rename(
                            SOURCE_DIR + "/" + DATA_NAME, SOURCE_DIR + "/" + TRACK_TITLE
                        )
                    elif name.endswith(".mp3"):
                        PATH = os.path.join(SOURCE_DIR, name)
                        audio = EasyID3(PATH)
                        for F_DATA in METADATA["files"]:
                            if F_DATA["name"] == name:
                                DATA_NAME = F_DATA["name"]
                                F1TRACK = F_DATA["track"]
                                FTRACK = int(F1TRACK)
                                TRACKNUMBER = f"{FTRACK:02d}"
                                SONG_NAME = F_DATA["title"]
                                TRACK_TITLE = (
                                    TRACKNUMBER + " " + _clean_(SONG_NAME) + ".mp3"
                                )
                                audio["title"] = SONG_NAME
                                audio["artist"] = CREATOR
                                audio["album"] = ALBUM
                                audio["tracknumber"] = TRACKNUMBER
                                audio["date"] = DATE
                                audio["albumartist"] = CREATOR
                                audio["albumartistsort"] = CREATOR
                                audio["artistsort"] = CREATOR
                                audio["musicbrainz_artistid"] = MBID
                                audio["originaldate"] = DATE
                                audio.save()
                                os.rename(
                                    SOURCE_DIR + "/" + DATA_NAME,
                                    SOURCE_DIR + "/" + TRACK_TITLE,
                                )
    cprint("Hey its me, DAVE, I got the stuff!", c="Black", b="Red", key="-ML-")

WINDOW.close()
