import sys
import datetime
import urllib.parse
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
    return "0:00"


def get_song_filesize(filename):
    return "0"


def get_timestamp():
    date = datetime.datetime.now().strftime("%d")
    # TODO: To ordinal somehow
    timestamp = datetime.datetime.now().strftime("%A date of %B %Y %H:%M:%S")
    timestamp = timestamp.replace("date", date)
    return timestamp


def main():
    song_list = Path("index.txt").read_text().splitlines()
    song_html = populate_songs(song_list)

    timestamp = get_timestamp()

    html_text = Path(sys.argv[1]).read_text()
    layout = Template(html_text)
    html_text = layout.substitute(song_list=song_html, update_timestamp=timestamp)
    print(html_text) # TODO: Return it?


main()