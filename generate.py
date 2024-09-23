import sys
import datetime
import urllib.parse
import ffmpeg
from pathlib import Path
from string import Template
from math import floor


SONG_HTML = """
      <tr class="song">
        <td>
          <button onclick="play('$url')" title="Play">
            <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M240 128a15.74 15.74 0 0 1-7.6 13.51L88.32 229.65a16 16 0 0 1-16.2.3A15.86 15.86 0 0 1 64 216.13V39.87a15.86 15.86 0 0 1 8.12-13.82a16 16 0 0 1 16.2.3l144.08 88.14A15.74 15.74 0 0 1 240 128"/></svg>
          </button>
          <button onclick="addToQueue('$url')" title="Add to Queue">
            <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M28 64a12 12 0 0 1 12-12h176a12 12 0 0 1 0 24H40a12 12 0 0 1-12-12m12 76h176a12 12 0 0 0 0-24H40a12 12 0 0 0 0 24m104 40H40a12 12 0 0 0 0 24h104a12 12 0 0 0 0-24m88 0h-12v-12a12 12 0 0 0-24 0v12h-12a12 12 0 0 0 0 24h12v12a12 12 0 0 0 24 0v-12h12a12 12 0 0 0 0-24"/></svg>
          </button>
        </td>
        <td class="songname">
          $title
        <td>
          $playtime
        </td>
        </td>
        <td class="download">
          <button onclick="showLyrics('$url')" title="Show Lyrics">
            <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M28 64a12 12 0 0 1 12-12h176a12 12 0 0 1 0 24H40a12 12 0 0 1-12-12m12 76h116a12 12 0 0 0 0-24H40a12 12 0 0 0 0 24m68 40H40a12 12 0 0 0 0 24h68a12 12 0 0 0 0-24m143.49-52.55a12 12 0 0 1-14.94 8L212 128.13V192a36 36 0 1 1-24-33.94V112a12 12 0 0 1 15.45-11.49l40 12a12 12 0 0 1 8.04 14.94M188 192a12 12 0 1 0-12 12a12 12 0 0 0 12-12"/></svg>
          </button>
          <button onclick="showSongInfo('$url')" title="Show Song Info">
            <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M108 84a16 16 0 1 1 16 16a16 16 0 0 1-16-16m128 44A108 108 0 1 1 128 20a108.12 108.12 0 0 1 108 108m-24 0a84 84 0 1 0-84 84a84.09 84.09 0 0 0 84-84m-72 36.68V132a20 20 0 0 0-20-20a12 12 0 0 0-4 23.32V168a20 20 0 0 0 20 20a12 12 0 0 0 4-23.32"/></svg>
          </button>
          <button onclick="downloadSong('$url')" title="Download Song (8 Mb)">
            <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M228 144v64a12 12 0 0 1-12 12H40a12 12 0 0 1-12-12v-64a12 12 0 0 1 24 0v52h152v-52a12 12 0 0 1 24 0m-108.49 8.49a12 12 0 0 0 17 0l40-40a12 12 0 0 0-17-17L140 115V32a12 12 0 0 0-24 0v83L96.49 95.51a12 12 0 0 0-17 17Z"/></svg>
          </button>
        </td>
      </tr>
"""


def populate_songs(song_list):
    songs = []
    song_html = Template(SONG_HTML)
    for song_filepath in song_list:
        if not Path(song_filepath).exists():
            # TODO: Add to a list of missing songs? I guess this shouldn't happen
            continue
        url = get_song_url(song_filepath)
        title = get_song_name(song_filepath)
        playtime = get_song_playtime(song_filepath)
        filesize = get_song_filesize(song_filepath)
        songs.append(song_html.substitute(url=url, title=title, playtime=playtime, filesize=filesize))
    
    return "".join(songs)


def get_song_url(filename):
    path = Path(filename)
    return str(path.parent / urllib.parse.quote_plus(path.name))


def get_song_name(filename):
    return Path(filename).stem.replace("_", " ")


def get_song_playtime(filename):
    time = float(ffmpeg.probe(filename)['format']['duration'])
    minutes = floor(time / 60)
    seconds = floor(time + 0.5) % 60
    return f"{minutes}:{seconds:02}"


def get_song_filesize(filename):
    byte_size = Path(filename).stat().st_size
    return str(round(byte_size / 1048576, 2))


def get_timestamp():
    date = datetime.datetime.now().strftime("%d")
    timestamp = datetime.datetime.now().strftime("%A date of %B %Y %H:%M:%S")
    timestamp = timestamp.replace("date", make_ordinal(date))
    return timestamp


def make_ordinal(n):
    '''
    (From here: https://stackoverflow.com/a/50992575/4173627)
    Convert an integer into its ordinal representation::

        make_ordinal(0)   => '0th'
        make_ordinal(3)   => '3rd'
        make_ordinal(122) => '122nd'
        make_ordinal(213) => '213th'
    '''
    n = int(n)
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix


def main(html_layout_filepath, song_list_filepath):
    song_list = Path(song_list_filepath).read_text().splitlines()
    song_html = populate_songs(song_list)
    timestamp = get_timestamp()
    html_text = Path(html_layout_filepath).read_text()
    layout = Template(html_text)
    html_text = layout.substitute(song_list=song_html, update_timestamp=timestamp)
    print(html_text)


main(sys.argv[1], sys.argv[2])
