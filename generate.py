import sys
import datetime
import urllib.parse
import ffmpeg # ffmpeg-python
from pathlib import Path
from string import Template


SONG_HTML = """
      <tr class="song">
        <td class="songname">
          <a onclick="choose('$url')" title="[$playtime]">
            <img src="playbutton.png" alt="Play $title">
            $title
          </a>
        </td>
        <td class="download">
          <a href="$url" download="$title" title="Download ($filesize Mb)">
            <img src="downloadButton.png" alt="Download Audio File">
          </a>
        </td>
      </tr>
"""


def populate_songs(song_list):
    songs = []
    for song_filename in song_list:
        if not (Path("song_audio") / Path(song_filename)).exists():
            # TODO: Add to a list of missing songs? I guess this shouldn't happen
            continue
        url = get_song_url(song_filename)
        title = get_song_name(song_filename)
        playtime = get_song_playtime(song_filename)
        filesize = get_song_filesize(song_filename)
        songs.append(SONG_HTML.replace("$url", url).replace("$title", title).replace("$playtime", playtime).replace("$filesize", filesize))
    
    return "".join(songs)


def get_song_url(filename):
    return urllib.parse.quote_plus(filename)


def get_song_name(filename):
    return filename.replace("_", " ").replace(".mp3", "")


def get_song_playtime(filename):
    time = ffmpeg.probe(filename)['format']['duration']
    minutes = floor(time / 60)
    return f"{minutes}:00"


def get_song_filesize(filename):
    byte_size = (Path("song_audio") / Path(filename)).stat().st_size
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


def main():
    song_list = Path(sys.argv[2]).read_text().splitlines()
    song_html = populate_songs(song_list)
    timestamp = get_timestamp()
    html_text = Path(sys.argv[1]).read_text()
    layout = Template(html_text)
    html_text = layout.substitute(song_list=song_html, update_timestamp=timestamp)
    print(html_text)


main()
