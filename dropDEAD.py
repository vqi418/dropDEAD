import os
from internetarchive.session import ArchiveSession
from internetarchive.search import Search
from internetarchive import download
from internetarchive import get_item
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
import PySimpleGUI as sg

s = ArchiveSession()

sg.theme('DarkBlack')

LISTBOX_SELECT_MODE_MULTIPLE = 'multi'

BANDID = ''

cprint = sg.cprint

ids = []


def get_key(val):
    for key, value in chosen.items():
        if val == value:
            return key


bnd_col1 = sg.Column([
    [sg.Radio('Grateful Dead', 'RADIO1', circle_color='DarkRed', font=('Times New Roman', 12, 'normal'),
              key='GratefulDead', pad=(5, 5))],
    [sg.Radio('Little Feat', 'RADIO1', circle_color='DarkRed', font=('Times New Roman', 12, 'normal'),
              key='LittleFeat', pad=(5, 5))],
    [sg.Radio('Dead and Company', 'RADIO1', circle_color='DarkRed', font=('Times New Roman', 12, 'normal'),
              key='DeadAndCompany', pad=(5, 5))],
    [sg.Radio('Billy Strings', 'RADIO1', circle_color='DarkRed', font=('Times New Roman', 12, 'normal'),
              key='BillyStrings', pad=(5, 5))],
    [sg.Radio('Tedeschi Trucks Band', 'RADIO1', circle_color='DarkRed',
              font=('Times New Roman', 12, 'normal'), key='TedeschiTrucksBand', pad=(5, 5))],
    [sg.Radio('North Mississippi Allstars', 'RADIO1', circle_color='DarkRed',
              font=('Times New Roman', 12, 'normal'), key='NorthMississippiAllstars', pad=(5, 5))],
    [sg.Radio('Phil Lesh and Friends', 'RADIO1', circle_color='DarkRed',
              font=('Times New Roman', 12, 'normal'), key='PhilLeshandFriends', pad=(5, 5))]
])

bnd_col2 = sg.Column([
    [sg.Radio('Joe Russos Almost Dead', 'RADIO1', circle_color='DarkRed',
              font=('Times New Roman', 12, 'normal'), key='JoeRussosAlmostDead', pad=(5, 5))],
    [sg.Radio('Yonder Mountain String Band', 'RADIO1', circle_color='DarkRed',
              font=('Times New Roman', 12, 'normal'), key='YonderMountainStringBand', pad=(5, 5))],
    [sg.Radio('Railroad Earth', 'RADIO1', circle_color='DarkRed', font=('Times New Roman', 12, 'normal'),
              key='RailroadEarth', pad=(5, 5))],
    [sg.Radio('MaxCreek', 'RADIO1', circle_color='DarkRed', font=('Times New Roman', 12, 'normal'),
              key='MaxCreek', pad=(5, 5))],
    [sg.Radio('Ratdog', 'RADIO1', circle_color='DarkRed', font=('Times New Roman', 12, 'normal'),
              key='Ratdog', pad=(5, 5))],
    [sg.Radio("Dark Star Orchestra", 'RADIO1', circle_color='DarkRed',
              font=('Times New Roman', 12, 'normal'), key='DarkStarOrchestra', pad=(5, 5))],
    [sg.Radio('Blues Traveler', 'RADIO1', circle_color='DarkRed', font=('Times New Roman', 12, 'normal'),
              key='BluesTraveler', pad=(5, 5))]
])

bnd_col3 = sg.Column([
    [sg.Radio('Furthur', 'RADIO1', circle_color='DarkRed', font=('Times New Roman', 12, 'normal'),
              key='Furthur', pad=(5, 5))],
    [sg.Radio('Leftover Salmon', 'RADIO1', circle_color='DarkRed', font=('Times New Roman', 12, 'normal'),
              key='LeftoverSalmon', pad=(5, 5))],
    [sg.Radio('Drive-By Truckers', 'RADIO1', circle_color='DarkRed', font=('Times New Roman', 12, 'normal'),
              key='Drive-ByTruckers', pad=(5, 5))],
    [sg.Radio('Derek Trucks Band', 'RADIO1', circle_color='DarkRed', font=('Times New Roman', 12, 'normal'),
              key='DerekTrucksBand', pad=(5, 5))],
    [sg.Radio('Bob Weir', 'RADIO1', circle_color='DarkRed', font=('Times New Roman', 12, 'normal'),
              key='BobWeir', pad=(5, 5))],
    [sg.Radio('New Riders of the Purple Sage', 'RADIO1', circle_color='DarkRed',
              font=('Times New Roman', 12, 'normal'), key='NewRidersofthePurpleSage', pad=(5, 5))],
    [sg.Radio('String Cheese Incident', 'RADIO1', circle_color='DarkRed',
              font=('Times New Roman', 12, 'normal'), key='StringCheeseIncident', pad=(5, 5))]
])

bnd_frm_layout = [
    [bnd_col1, bnd_col2, bnd_col3]
]

col1 = sg.Column([
    [sg.Frame('Bands', bnd_frm_layout, font=('Times New Roman', 14, 'normal'), title_color='Red', border_width=3)]
])

col2 = sg.Column([

    [sg.Frame('Date', [[sg.Column([
        [sg.Text(
            'Please enter the Year Month and Day of the Show:\n (to list all shows in a Year, enter the Year only)\n '
            'YYYY - MM - DD', font=('Times New Roman', 12, 'normal'), text_color='#E7D541')],
        [sg.Input(key='-YEAR-', s=(5, 2), text_color='Yellow', font=('Times New Roman', 14, 'normal'), tooltip='Year',
                  border_width=3, pad=(15, 5)),
         sg.Input(key='-MONTH-', s=(3, 2), text_color='Yellow', font=('Times New Roman', 14, 'normal'), tooltip='Month',
                  border_width=3, pad=(10, 5)),
         sg.Input(key='-DAY-', s=(3, 2), text_color='Yellow', font=('Times New Roman', 14, 'normal'), tooltip='Day',
                  border_width=3, pad=(10, 5))]])]],
              title_color='Red', border_width=3, size=(400, 175), font=('Times New Roman', 14, 'normal'))],

    [sg.Button('Search', border_width=3, button_color=('Red', '#2C2D2F'), font=('Times New Roman', 14, 'bold'),
               bind_return_key=True, key='-SETDATE-')]

])

fr_col1 = sg.Column([
    [sg.Image(size=(0, 0))],
    [sg.Column([
        [sg.Text('Select the show you would like to download:', font=('Times New Roman', 12, 'normal'),
                 text_color='#E7D541')],
        [sg.Listbox(ids, select_mode='multi', enable_events=False,
                    size=(70, 10), font=('Times New Roman', 12, 'normal'),
                    text_color='Yellow', highlight_background_color='White',
                    highlight_text_color='Red',
                    key='-LISTBOX-')],
        [sg.Button('Download', border_width=3, button_color=('Red', '#2C2D2F'), font=('Times New Roman', 14, 'bold'),
                   key='-GET_SHOW-')]
    ])]
], key='-COL1-', visible=False)

fr_col2 = sg.Column([
    [sg.Image(size=(0, 0))],
    [sg.Column([
        [sg.Frame('File Type and Location', [[sg.Column([
            [sg.Text(
                'Would you like to download Flac files or MP3?\n(GD soundboard shows can only be downloaded in MP3,'
                '\n by request of the band)',
                font=('Times New Roman', 12, 'normal'), text_color='#E7D541')],
            [sg.Radio('Flac', 'RADIO2', circle_color='DarkRed', font=('Times New Roman', 12, 'normal'),
                      key='-FLAC-', pad=(5, 5)),
             sg.Radio('MP3', 'RADIO2', circle_color='DarkRed', font=('Times New Roman', 12, 'normal'),
                      key='-MP3-', pad=(5, 5))],
            [sg.HorizontalSeparator(color='DarkRed', pad=(5, 20))],
            [sg.Text('Please browse to the download directory:', font=('Times New Roman', 12, 'normal'),
                     text_color='#E7D541')],
            [sg.In(s=(40, 60), key='-FOLD-'), sg.FolderBrowse(button_text="Browse", button_color=('Red', '#2C2D2F'),
                                                              font=('Times New Roman', 14, 'bold'), key='-DIR-')]])]],
                  title_color='Red',
                  border_width=3, size=(500, 300),
                  font=('Times New Roman', 14, 'normal'), element_justification='center')]
    ])]
], key='-COL2-', visible=False)

frame1_layout = [
    [fr_col1, fr_col2]
]

box_layout = sg.Column([
    [sg.Frame('Shows', frame1_layout, font=('Times New Roman', 14, 'normal'), title_color='Red', border_width=3,
              key='-BOXFRAME-', size=(1150, 325), visible=False, element_justification='center')]
], key='-BOXCOL-', visible=False)

prnt_win = sg.Column([
    [sg.Image(size=(0, 0))],
    [sg.Frame('Progress', [[sg.Column([
        [sg.Multiline(key='-ML-', border_width=3, size=(80, 10), autoscroll=True, background_color='Black',
                      text_color='#E7D541', font=('Times New Roman', 14, 'bold'), reroute_stdout=True,
                      reroute_stderr=True, reroute_cprint=False, echo_stdout_stderr=True, write_only=True,
                      auto_refresh=True)]
    ])]], font=('Times New Roman', 14, 'normal'), title_color='Red', border_width=3,)]
], key='-INFOBOX-', visible=False)

layout = [
    [col1, col2],
    [prnt_win],
    [box_layout]
]

window = sg.Window("dropDEAD - Archive Downloader", layout, element_justification='c', grab_anywhere=True)

sg.cprint_set_output_destination(window, '-ML-')

while True:

    event, values = window.read()
    chosen = values
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == '-SETDATE-':
        window['GratefulDead'].reset_group()
        window['-FLAC-'].reset_group()
        window['-YEAR-'].Update('')
        window['-MONTH-'].Update('')
        window['-DAY-'].Update('')
        window['-LISTBOX-'].Update('')
        # window.FindElement('-FLAC-').Update('')
        # window.FindElement('-MP3-').Update('')
        window['-FOLD-'].Update('')
        window['-INFOBOX-'].hide_row()
        window['-INFOBOX-'].Update(visible=False)
        window['-BOXCOL-'].unhide_row()
        window['-BOXCOL-'].Update(visible=True)
        window['-COL1-'].unhide_row()
        window['-COL1-'].Update(visible=True)
        window['-COL2-'].unhide_row()
        window['-COL2-'].Update(visible=True)
        window['-BOXFRAME-'].Update(visible=True)
        BANDID = get_key(True)
        year = chosen.get('-YEAR-')
        month = chosen.get('-MONTH-')
        day = chosen.get('-DAY-')
        showdate = year + "-" + month + "-" + day
        query1 = 'collection:' + BANDID
        query2 = ' title:' + showdate
        search = Search(s, (query1 + query2))
        for result in search:
            ids.append(result['identifier'])
        window['-LISTBOX-'].Update(ids)
    if event == '-GET_SHOW-':
        window['-ML-'].Update('')
        window['-BOXFRAME-'].Update(visible=False)
        window['-BOXCOL-'].Update(visible=False)
        window['-BOXCOL-'].hide_row()
        window['-COL1-'].Update(visible=False)
        window['-COL2-'].Update(visible=False)
        window['-COL1-'].hide_row()
        window['-COL2-'].hide_row()
        window['-INFOBOX-'].unhide_row()
        window['-INFOBOX-'].Update(visible=True)

        down_info = values
        dforms = ['Text', 'Flac', '24bit Flac', 'Item Tile', 'JPEG', 'JPEG Thumb'] if down_info.get(
            '-FLAC-') is True else \
            ['Text', 'VBR MP3', 'Item Tile', 'JPEG', 'JPEG Thumb']
        show_id = down_info.get('-LISTBOX-')
        localdir = down_info.get('-DIR-')
        SHOWID1 = str(show_id)[1: - 1]
        SHOWID = SHOWID1.strip("'")
        item = get_item(SHOWID)
        metadata = item.item_metadata
        creator = metadata['metadata']['creator']
        date = metadata['metadata']['date']
        venue = metadata['metadata']['venue']
        album = date + ' - ' + venue
        localdir = localdir.rstrip('//')
        print(dforms, localdir, SHOWID, creator, date, venue, album)
        download(SHOWID, formats=dforms, verbose=True, ignore_existing=True, destdir=localdir, retries=3)
        source_dir = localdir + '/' + SHOWID

        MBID = ''

        for name in os.listdir(source_dir):
            if BANDID == 'GratefulDead':
                MBID = '6faa7ca7-0d99-4a5e-bfa6-1fd5037520c6'
            elif BANDID == 'LittleFeat':
                MBID = '9b106beb-12b5-4525-8025-42e295a2b90a'
            elif BANDID == 'DeadAndCompany':
                MBID = '94f8947c-2d9c-4519-bcf9-6d11a24ad006'
            elif BANDID == 'BillyStrings':
                MBID = '640db492-34c4-47df-be14-96e2cd4b9fe4'
            elif BANDID == 'TedeschiTrucksBand':
                MBID = 'e33e1ccf-a3b9-4449-a66a-0091e8f55a60'
            elif BANDID == 'NorthMississippiAllstars':
                MBID = '62fa3eb2-1b73-4029-ba35-16ab66d29d02'
            elif BANDID == 'PhilLeshandFriends':
                MBID = 'ffb7c323-5113-4bb0-a5f7-5b657eec4083'
            elif BANDID == 'JoeRussosAlmostDead':
                MBID = '84a69823-3d4f-4ede-b43f-17f85513181a'
            elif BANDID == 'YonderMountainStringBand':
                MBID = '76fda896-7c2a-4e5e-a45b-d40acfb2080c'
            elif BANDID == 'RailroadEarth':
                MBID = 'b2e2abfa-fb1e-4be0-b500-56c4584f41cd'
            elif BANDID == 'MaxCreek':
                MBID = '75f27492-3018-4b1e-aa04-60c31059a5c5'
            elif BANDID == 'Ratdog':
                MBID = '73c5a9bc-3e0d-45e6-a981-ba67435e1f58'
            elif BANDID == 'DarkStarOrchestra':
                MBID = 'e477d9c0-1f35-40f7-ad1a-b915d2523b84'
            elif BANDID == 'BluesTraveler':
                MBID = '6b28ecf0-94e6-48bb-aa2a-5ede325b675b'
            elif BANDID == 'Furthur':
                MBID = '39e07389-bbc0-4629-9ceb-dbd0d13b85fe'
            elif BANDID == 'LeftoverSalmon':
                MBID = '3020be1d-3c41-4e42-911b-ca5e96489300'
            elif BANDID == 'Drive-ByTruckers':
                MBID = '8eae1e0a-1696-4532-9e3c-0a072217ef4c'
            elif BANDID == 'DerekTrucksBand':
                MBID = 'bb110dbc-8daa-407f-a04b-f569e7a5ee7e'
            elif BANDID == 'BobWeir':
                MBID = 'c8a63580-9e6b-4852-bf93-c09760035e76'
            elif BANDID == 'NewRidersofthePurpleSage':
                MBID = '64c8fe79-1f93-483f-aace-b6a6e379e7d2'
            elif BANDID == 'StringCheeseIncident':
                MBID = 'cff95140-6d57-498a-8834-10eb72865b29'
            else:
                print('Wooooo, hold on, gimmie time to think!!!! Something has gone terribly wrong')
            if name.endswith(".flac"):
                path = os.path.join(source_dir, name)
                audio = FLAC(path)
                for file_data in metadata['files']:
                    if file_data['name'] == name:
                        data_name = file_data['name']
                        f1track = file_data['track']
                        ftrack = int(f1track)
                        tracknumber = f'{ftrack:02d}'
                        song_name = file_data['title']
                        track_title = tracknumber + ' ' + song_name.replace('->', '').replace('>', '')\
                            .replace('/', '-').replace('*', '') + '.flac'
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
                        os.rename(source_dir + '/' + data_name, source_dir + '/' + track_title)
            elif name.endswith(".mp3"):
                path = os.path.join(source_dir, name)
                audio = EasyID3(path)
                for file_data in metadata['files']:
                    if file_data['name'] == name:
                        data_name = file_data['name']
                        f1track = file_data['track']
                        ftrack = int(f1track)
                        tracknumber = f'{ftrack:02d}'
                        song_name = file_data['title']
                        track_title = tracknumber + ' ' + song_name.replace('->', '').replace('>', '')\
                            .replace('/', '-').replace('*', '') + '.mp3'
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
                        os.rename(source_dir + '/' + data_name, source_dir + '/' + track_title)
            else:
                cprint('Hey its me, DAVE, I got the stuff!', c='Red',  b='White', key='-ML-')
                ids = []
                continue
window.close()
