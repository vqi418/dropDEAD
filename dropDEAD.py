from internetarchive.session import ArchiveSession
from internetarchive.search import Search
from internetarchive import download
from internetarchive import get_item
from mutagen.flac import FLAC
import os
import PySimpleGUI as sg

s = ArchiveSession()

sg.theme('Black')

group_pick = [
    [sg.Text('Please choose a band: ')],
    [sg.Radio('GratefulDead', 'RADIO1', key='GratefulDead')],
    [sg.Radio('LittleFeat', 'RADIO1', key='LittleFeat'), sg.Push(),
     sg.Radio('DeadAndCompany', 'RADIO1', key='DeadAndCompany')],
    [sg.Radio('BillyStrings', 'RADIO1', key='BillyStrings'), sg.Push(),
     sg.Radio('TedeschiTrucksBand', 'RADIO1', key='TedeschiTrucksBand')],
    [sg.Radio('NorthMississippiAllstars', 'RADIO1', key='NorthMississippiAllstars'), sg.Push(),
     sg.Radio('PhilLeshandFriends', 'RADIO1', key='PhilLeshandFriends')],
    [sg.Radio('JoeRussosAlmostDead', 'RADIO1', key='JoeRussosAlmostDead'), sg.Push(),
     sg.Radio('YonderMountainStringBand', 'RADIO1', key='YonderMountainStringBand')],
    [sg.Radio('RailroadEarth', 'RADIO1', key='RailroadEarth'), sg.Push(),
     sg.Radio('MaxCreek', 'RADIO1', key='MaxCreek')],
    [sg.Radio('Ratdog', 'RADIO1', key='Ratdog'), sg.Push(),
     sg.Radio("DarkStarOrchestra", 'RADIO1', key='DarkStarOrchestra')],
    [sg.Radio('BluesTraveler', 'RADIO1', key='BluesTraveler'), sg.Push(),
     sg.Radio('Furthur', 'RADIO1', key='Furthur')],
    [sg.Radio('LeftoverSalmon', 'RADIO1', key='LeftoverSalmon'), sg.Push(),
     sg.Radio('Drive-ByTruckers', 'RADIO1', key='Drive-ByTruckers')],
    [sg.Radio('DerekTrucksBand', 'RADIO1', key='DerekTrucksBand'), sg.Push(),
     sg.Radio('BobWeir', 'RADIO1', key='BobWeir')],
    [sg.Radio('NewRidersofthePurpleSage', 'RADIO1', key='NewRidersofthePurpleSage'), sg.Push(),
     sg.Radio('StringCheeseIncident', 'RADIO1', key='StringCheeseIncident')]
]

date_pick = [
    [sg.Text(
        'Please enter the Year Month and Day of the Show:\n (to list all shows in a Year, enter the Year only)\n YYYY '
        '- MM - DD')],
    [sg.Input(key='-YEAR-', s=4, tooltip='Year', border_width=2, pad=(15, 5)),
     sg.Input(key='-MONTH-', s=2, tooltip='Month', border_width=2, pad=(10, 5)),
     sg.Input(key='-DAY-', s=2, tooltip='Day', border_width=2, pad=(10, 5))]
]

layout = [
    [sg.Frame('Band Selection', group_pick, font='Any 16', title_color='yellow')],
    [sg.Frame('Date of Show', date_pick, font='Any 16', title_color='yellow')],
    [sg.Submit(), sg.Cancel()]
]

window = sg.Window('dropDEAD - Archive Dead and Family Show Download', layout, font=("Helvetica", 16),
                   element_justification='c')

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    chosen = values
    window.close()


def get_key(val):
    for key, value in chosen.items():
        if val == value:
            return key


bandid = get_key(True)

year = chosen.get('-YEAR-')
month = chosen.get('-MONTH-')
day = chosen.get('-DAY-')

showdate = year + "-" + month + "-" + day

query1 = 'collection:' + bandid
query2 = ' title:' + showdate

search = Search(s, (query1 + query2))

ids = []
for result in search:
    ids.append(result['identifier'])

show_pick = [
    [sg.Text('Choose the Show to download: ')],
    [sg.Listbox(ids, size=(55, 15), key='-SHOW-')]
]

format_pick = [
    [sg.Text('Would you like to download Flac files or MP3?')],
    [sg.Radio('Flac', 'RADIO2', key='-FLAC-'), sg.Radio('MP3', 'RADIO2', key='-MP3-')]
]

dir_pick = [
    [sg.Text('Please enter the path to the download directory')],
    [sg.Input(size=55, key='-DIR-')]
]

layout = [
    [sg.Frame('Available Shows', show_pick, font='Any 16', title_color='yellow')],
    [sg.Frame('File Format', format_pick, font='Any 16', title_color='yellow')],
    [sg.Frame('Path to download folder', dir_pick, font='Any 16', title_color='yellow')],
    [sg.Submit(), sg.Cancel()]
]

window = sg.Window('dropDEAD - Archive Dead and Family Show Download', layout, font=("Helvetica", 16),
                   element_justification='c')

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    chosen = values
    window.close()

dforms = ['Text', 'Flac', '24bit Flac', 'Item Tile', 'JPEG', 'JPEG Thumb'] if chosen.get('-FLAC-') is True else \
    ['Text', 'VBR MP3', 'Item Tile', 'JPEG', 'JPEG Thumb']

show_id = chosen.get('-SHOW-')
localdir = chosen.get('-DIR-')

showid = str(show_id)[1: - 1]
showid = showid.strip("'")
item = get_item(showid)
metadata = item.item_metadata
creator = metadata['metadata']['creator']
date = metadata['metadata']['date']
venue = metadata['metadata']['venue']
album = date + ' - ' + venue
localdir = localdir.rstrip('//')

download(showid, formats=dforms, verbose=True, ignore_existing=True, destdir=localdir, retries=3)

source_dir = localdir + '/' + showid

mbid = ''

for name in os.listdir(source_dir):  # iterate over all files/directories in source_dir
    if bandid == 'GratefulDead':
        mbid = '6faa7ca7-0d99-4a5e-bfa6-1fd5037520c6'
    elif bandid == 'LittleFeat':
        mbid = '9b106beb-12b5-4525-8025-42e295a2b90a'
    elif bandid == 'DeadAndCompany':
        mbid = '94f8947c-2d9c-4519-bcf9-6d11a24ad006'
    elif bandid == 'BillyStrings':
        mbid = '640db492-34c4-47df-be14-96e2cd4b9fe4'
    elif bandid == 'TedeschiTrucksBand':
        mbid = 'e33e1ccf-a3b9-4449-a66a-0091e8f55a60'
    elif bandid == 'NorthMississippiAllstars':
        mbid = '62fa3eb2-1b73-4029-ba35-16ab66d29d02'
    elif bandid == 'PhilLeshandFriends':
        mbid = 'ffb7c323-5113-4bb0-a5f7-5b657eec4083'
    elif bandid == 'JoeRussosAlmostDead':
        mbid = '84a69823-3d4f-4ede-b43f-17f85513181a'
    elif bandid == 'YonderMountainStringBand':
        mbid = '76fda896-7c2a-4e5e-a45b-d40acfb2080c'
    elif bandid == 'RailroadEarth':
        mbid = 'b2e2abfa-fb1e-4be0-b500-56c4584f41cd'
    elif bandid == 'MaxCreek':
        mbid = '75f27492-3018-4b1e-aa04-60c31059a5c5'
    elif bandid == 'Ratdog':
        mbid = '73c5a9bc-3e0d-45e6-a981-ba67435e1f58'
    elif bandid == 'DarkStarOrchestra':
        mbid = 'e477d9c0-1f35-40f7-ad1a-b915d2523b84'
    elif bandid == 'BluesTraveler':
        mbid = '6b28ecf0-94e6-48bb-aa2a-5ede325b675b'
    elif bandid == 'Furthur':
        mbid = '39e07389-bbc0-4629-9ceb-dbd0d13b85fe'
    elif bandid == 'LeftoverSalmon':
        mbid = '3020be1d-3c41-4e42-911b-ca5e96489300'
    elif bandid == 'Drive-ByTruckers':
        mbid = '8eae1e0a-1696-4532-9e3c-0a072217ef4c'
    elif bandid == 'DerekTrucksBand':
        mbid = 'bb110dbc-8daa-407f-a04b-f569e7a5ee7e'
    elif bandid == 'BobWeir':
        mbid = 'c8a63580-9e6b-4852-bf93-c09760035e76'
    elif bandid == 'NewRidersofthePurpleSage':
        mbid = '64c8fe79-1f93-483f-aace-b6a6e379e7d2'
    elif bandid == 'StringCheeseIncident':
        mbid = 'cff95140-6d57-498a-8834-10eb72865b29'
    else:
        print('Wooooo, hold on, gimmie time to think!!!! Something has gone terribly wrong')
    if name.endswith(".flac"):
        path = os.path.join(source_dir, name)
        audio = FLAC(path)
        for file_data in metadata['files']:
            if file_data['name'] == name:
                data_name = file_data['name']
                tracknumber = file_data['track']
                song_name = file_data['title']
                track_title = tracknumber + ' ' + song_name.replace('->', '').replace('>', '').replace('/', '-') \
                    + '.flac'
                audio["title"] = song_name
                audio["artist"] = creator
                audio["album"] = album
                audio["tracknumber"] = tracknumber
                audio["date"] = date
                audio["albumartist"] = creator
                audio["albumartistsort"] = creator
                audio["artistsort"] = creator
                audio["musicbrainz_artistid"] = mbid
                audio["originaldate"] = date
                audio.save()
                os.rename(source_dir + '/' + data_name, source_dir + '/' + track_title)
    elif name.endswith(".mp3"):
        from mutagen.easyid3 import EasyID3
        path = os.path.join(source_dir, name)
        audio = EasyID3(path)
        for file_data in metadata['files']:
            if file_data['name'] == name:
                data_name = file_data['name']
                tracknumber = file_data['track']
                song_name = file_data['title']
                track_title = tracknumber + ' ' + song_name.replace('->', '').replace('>', '').replace('/', '-') \
                    + '.mp3'
                audio["title"] = song_name
                audio["artist"] = creator
                audio["album"] = album
                audio["tracknumber"] = tracknumber
                audio["date"] = date
                audio["albumartist"] = creator
                audio["albumartistsort"] = creator
                audio["artistsort"] = creator
                audio["musicbrainz_artistid"] = mbid
                audio["originaldate"] = date
                audio.save()
                os.rename(source_dir + '/' + data_name, source_dir + '/' + track_title)
    else:
        continue
