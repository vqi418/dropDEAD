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

BANDID = ""
VENUE = ""
VENUE_1 = ""

ids = []
ids2 = {}

cprint = sg.cprint

D_SWITCH = "neutral"
VENUE_AVAIL = "ON"
SUBJECT_AVAIL = "ON"
TOPICS = ""

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

bnd_col1 = sg.Column(
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

bnd_col2 = sg.Column(
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

bnd_col3 = sg.Column(
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

bnd_frm_layout = [[bnd_col1, bnd_col2, bnd_col3]]

col1 = sg.Column(
    [
        [
            sg.Frame(
                "Bands",
                bnd_frm_layout,
                title_color="Red",
                background_color="#03020f",
                border_width=3,
            )
        ]
    ]
)

col2 = sg.Column(
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

fr_col1 = sg.Column(
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
                            ids,
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

fr_col2 = sg.Column(
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

frame1_layout = [[fr_col1, fr_col2]]

box_layout = sg.Column(
    [
        [
            sg.Frame(
                "Shows",
                frame1_layout,
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

prnt_win = sg.Column(
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

layout = [[col1, col2], [prnt_win], [box_layout]]

window = sg.Window(
    "dropDEAD - Archive Downloader",
    layout,
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

sg.cprint_set_output_destination(window, "-ML-")

# def get_key(val):
#     for key, value in chosen.items():
#         if val == value:
#             return key


def clean(filename):
    return (
        str(filename)
        .replace("->", "")
        .replace(">", "")
        .replace("/", " - ")
        .replace("*", "")
        .replace("!", "")
        .replace("'", "")
    )


def strip(doc_name):
    return str(doc_name).strip("'").strip("][")


while True:

    event, values = window.read()
    print(event, values)
    chosen = values
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    if (
        event == "-YEAR-"
        and values["-YEAR-"]
        and values["-YEAR-"][-1] not in "0123456789"
    ):
        window["-YEAR-"].update(values["-YEAR-"][:-1])
    if event == "-YEAR-" and len(values["-YEAR-"]) > 4:
        window["-YEAR-"].update(values["-YEAR-"][:-1])
    if (
        event == "-MONTH-"
        and values["-MONTH-"]
        and values["-MONTH-"][-1] not in "0123456789"
    ):
        window["-MONTH-"].update(values["-MONTH-"][:-1])
    if event == "-MONTH-" and len(values["-MONTH-"]) > 2:
        window["-MONTH-"].update(values["-MONTH-"][:-1])
    if event == "-DAY-" and values["-DAY-"] and values["-DAY-"][-1] not in "0123456789":
        window["-DAY-"].update(values["-DAY-"][:-1])
    if event == "-DAY-" and len(values["-DAY-"]) > 2:
        window["-DAY-"].update(values["-DAY-"][:-1])
    if event == "-SETDATE-":
        xids = []
        ids = []
        ids2 = {}
        window["-YEAR-"].Update("")
        window["-MONTH-"].Update("")
        window["-DAY-"].Update("")
        window["-LISTBOX-"].Update("")
        window["-FOLD-"].Update("")
        window["-INFOBOX-"].hide_row()
        window["-INFOBOX-"].Update(visible=False)
        window["-BOXCOL-"].unhide_row()
        window["-BOXCOL-"].Update(visible=True)
        window["-COL1-"].unhide_row()
        window["-COL1-"].Update(visible=True)
        window["-COL2-"].unhide_row()
        window["-COL2-"].Update(visible=True)
        window["-BOXFRAME-"].Update(visible=True)
        band_range = dict(itertools.islice(chosen.items(), 0, 20, 1))
        for key, value in band_range.items():
            if True is value:
                BANDID = key
        year = chosen.get("-YEAR-")
        month = chosen.get("-MONTH-")
        day = chosen.get("-DAY-")
        showdate = year + "-" + month + "-" + day
        query1 = "collection:" + BANDID
        query2 = " title:" + showdate
        search = Search(s, (query1 + query2))
        for result in search:
            xids.append(result["identifier"])
        for i in xids:
            if month != "":
                item = get_item(i)
                date = item.item_metadata["metadata"]["date"]
                try:
                    VENUE_1 = item.item_metadata["metadata"]["venue"]
                except KeyError:
                    VENUE_AVAIL = "OFF"
                finally:
                    try:
                        TOPICS = item.item_metadata["metadata"]["subject"]
                    except KeyError:
                        SUBJECT_AVAIL = "OFF"
                    else:
                        TOPICS = str(TOPICS)
                        TOPICS = clean(TOPICS)
                    finally:
                        if VENUE_AVAIL == "ON" and SUBJECT_AVAIL == "ON":
                            show = date + "-" + VENUE_1 + " - " + TOPICS
                        elif VENUE_AVAIL == "OFF" and SUBJECT_AVAIL == "ON":
                            show = date + " - " + TOPICS
                        elif VENUE_AVAIL == "ON" and SUBJECT_AVAIL == "OFF":
                            show = date + "-" + VENUE_1
                        else:
                            show = date
                ids.append(show)
                ids2[show] = i
                D_SWITCH = "ON"
            else:
                ids.append(i)
                D_SWITCH = "OFF"
        window["-LISTBOX-"].Update(ids)
    if event == "-GET_SHOW-":
        window["-ML-"].Update("")
        window["-BOXFRAME-"].Update(visible=False)
        window["-BOXCOL-"].Update(visible=False)
        window["-BOXCOL-"].hide_row()
        window["-COL1-"].Update(visible=False)
        window["-COL2-"].Update(visible=False)
        window["-COL1-"].hide_row()
        window["-COL2-"].hide_row()
        window["-INFOBOX-"].unhide_row()
        window["-INFOBOX-"].Update(visible=True)

        down_info = values
        dforms = (
            ["Text", "Flac", "24bit Flac", "Item Tile", "JPEG", "JPEG Thumb"]
            if down_info.get("-FLAC-") is True
            else ["Text", "VBR MP3", "Item Tile", "JPEG", "JPEG Thumb"]
        )
        SHOW_ID1 = down_info.get("-LISTBOX-")
        SHOW_ID2 = strip(SHOW_ID1)
        if ids2 is {}:
            SHOW_ID = clean(SHOW_ID2)
        else:
            SHOW_ID3 = clean(SHOW_ID2)
            SHOW_ID = ids2[SHOW_ID3]
        localdir = down_info.get("-DIR-")
        item = get_item(SHOW_ID)
        metadata = item.item_metadata
        creator = metadata["metadata"]["creator"]
        date = metadata["metadata"]["date"]
        try:
            VENUE = metadata["metadata"]["venue"]
        except KeyError:
            album = date + " - " + creator
        else:
            album = date + " - " + VENUE
        localdir = localdir.rstrip("//")
        download(
            SHOW_ID,
            formats=dforms,
            verbose=True,
            ignore_existing=True,
            destdir=localdir,
            retries=3,
        )
        source_dir = localdir + "/" + SHOW_ID

        MBID = ""

        for name in os.listdir(source_dir):
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
                path = os.path.join(source_dir, name)
                audio = FLAC(path)
                for file_data in metadata["files"]:
                    if file_data["name"] == name:
                        data_name = file_data["name"]
                        f1track = file_data["track"]
                        ftrack = int(f1track)
                        tracknumber = f"{ftrack:02d}"
                        song_name = file_data["title"]
                        track_title = tracknumber + " " + clean(song_name) + ".flac"
                        audio["title"] = song_name
                        audio["artist"] = creator
                        audio["album"] = album
                        audio["tracknumber"] = tracknumber
                        audio["date"] = date
                        audio["albumartist"] = creator
                        audio["albumartistsort"] = creator
                        audio["artistsort"] = creator
                        audio["musicbrainz_artistid"] = MBID
                        audio["originaldate"] = date
                        audio.save()
                        os.rename(
                            source_dir + "/" + data_name, source_dir + "/" + track_title
                        )
                    elif name.endswith(".mp3"):
                        path = os.path.join(source_dir, name)
                        audio = EasyID3(path)
                        for f_data in metadata["files"]:
                            if f_data["name"] == name:
                                data_name = f_data["name"]
                                f1track = f_data["track"]
                                ftrack = int(f1track)
                                tracknumber = f"{ftrack:02d}"
                                song_name = f_data["title"]
                                track_title = (
                                    tracknumber + " " + clean(song_name) + ".mp3"
                                )
                                audio["title"] = song_name
                                audio["artist"] = creator
                                audio["album"] = album
                                audio["tracknumber"] = tracknumber
                                audio["date"] = date
                                audio["albumartist"] = creator
                                audio["albumartistsort"] = creator
                                audio["artistsort"] = creator
                                audio["musicbrainz_artistid"] = MBID
                                audio["originaldate"] = date
                                audio.save()
                                os.rename(
                                    source_dir + "/" + data_name,
                                    source_dir + "/" + track_title,
                                )
    cprint("Hey its me, DAVE, I got the stuff!", c="Black", b="Red", key="-ML-")

window.close()
