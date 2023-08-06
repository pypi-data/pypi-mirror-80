from __future__ import unicode_literals
from re import findall
import pyfiglet
from . import iy
from halo import Halo
import time
import sys
import click


import re

import youtube_dl
from rich.progress import Progress
from . import questions
from . import iy

from rich import print
from rich.progress import (
    BarColumn,
    DownloadColumn,
    TextColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
    Progress,
    TaskID,
)


#
# TODO regerous testing and also add doc

progress = Progress(
    TextColumn("[bold blue]{task.description}\n", justify="right"),
    BarColumn(),
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    DownloadColumn(),
    "•",
    TransferSpeedColumn(),
    "•",
    TimeRemainingColumn(),
    transient=True

)

# FIXME inbetween error when one module error cause another tho run

global current_deleting_file
current_deleting_file = ""
class MyLogger(object):
    def error(self, msg):
        if re.findall("requested format not available", msg):
            print(f"[bold red]ERROR: Requested format not available[/bold red]")
        else:
            print(f"[bold red]{msg}[/bold red]")

    def debug(self, msg):

        #
        # print(msg)
        if re.findall("has already been downloaded", msg):
            print(f" [bold #ADFF2F]{msg}[/bold #ADFF2F]")
        # FIXME if not ffmpeg then
        a = re.findall('\[ffmpeg\].*', msg)
        if a != []:
            if re.findall("Correcting container", a[0]):
                progress.update(0, visible=False)
                print(f"[bold #00ff00] {a[0]}[/bold #00ff00]")
            elif re.findall("Merging formats", a[0]):
                progress.update(0, visible=False)
                print(
                    f"[bold #ADFF2F]  Done downloading, now converting ...[/bold #ADFF2F]")
                print(f"[bold #00ff00]✔{a[0]}[/bold #00ff00]")
            elif re.findall("Destination:", a[0]):
                progress.update(0, visible=False)
                print(
                    f"[bold #ADFF2F]  Done downloading, now converting ...[/bold #ADFF2F]")
                print(f"[bold #00ff00]✔{a[0]}[/bold #00ff00]")
        if re.findall("Deleting original", msg):
            #current_deleting_file = msg
            #print(current_deleting_file)
            #print(f"[bold #00ff00]✔ Done converting[/bold #00ff00]")
            if current_deleting_file == None:
                print(f"[bold #00ff00]✔ Done converting[/bold #00ff00]")
            current_deleting_file = msg
            if current_deleting_file == msg:
                current_deleting_file = None

    def warning(self, msg):
        print(f"  [bold #FF8C00]{msg}[/bold #FF8C00]")


def my_hook(d):
    # print(d)
    total_bytes = None
    if "total_bytes_estimate" in d:
        total_bytes = d['total_bytes_estimate']
    elif "total_bytes" in d:
        total_bytes = d['total_bytes']

    if d['status'] == 'finished':

        # print(d)
        #progress.update(0, visible=False)
        filename = d['filename']
        slim_filename = re.sub('-[a-zA-Z0-9]+.f[1-9]+', '', filename)

        if "_elapsed_str" in d and re.findall('f\d', filename):
            if re.findall('f[1-3](0|1|3|4|6|7|9)[0-9]', filename) or re.findall('(\.mp4)', filename):
                print(
                    f"  [bold #ADFF2F	]Downloaded: [Video] {slim_filename}[/bold #ADFF2F	] [bold blue]100% of {d['_total_bytes_str']} in {d['_elapsed_str']}")

            elif re.findall('f(139|140|141|600|249|250|251|171|172)', filename) or re.findall('(\.m4a)', filename):
                print(
                    f"  [bold #ADFF2F	]Downloaded: [Audio] {slim_filename}[/bold #ADFF2F	] [bold blue]100% of {d['_total_bytes_str']} in {d['_elapsed_str']}")

            elif re.findall('f[1-3](2|7|8)', filename):
                print(
                    f"  [bold #ADFF2F	]Downloaded: [Video+Audio] {slim_filename}[/bold #ADFF2F	] [bold blue]100% of {d['_total_bytes_str']} in {d['_elapsed_str']}")

        else:
            print(
                f"  [bold #ADFF2F	]Downloaded: {slim_filename}[/bold #ADFF2F	]")

    if d['status'] == 'downloading':
        downloader_bytes = d['downloaded_bytes']
        filename = d['filename']
        slim_filename = re.sub('-[a-zA-Z0-9]+.f[1-9]+', '', filename)

        if re.findall('f[1-3](0|1|3|4|6|7|9)[0-9]', filename):
            progress.update(0, completed=downloader_bytes, total=total_bytes,
                            description=f"  [Vidio] {slim_filename}", visible=True)
        elif re.findall('f(139|140|141|600|249|250|251|171|172)', filename):
            progress.update(0, completed=downloader_bytes, total=total_bytes,
                            description=f"  [Audio] {slim_filename}", visible=True)
        elif re.findall('f(18|22|37|38)', filename):
            progress.update(0, completed=downloader_bytes, total=total_bytes,
                            description=f"  [Vidio+Audio] {slim_filename}", visible=True)
        else:
            progress.update(0, completed=downloader_bytes, total=total_bytes,
                            description=f"  {slim_filename}", visible=True)


@click.command()
def run():
    """
    Simple interactive youtube downloader written in python. Interactively select the quality and format for youtube-dl

    Run you-dl thats all you need. :-)
    """

    result = pyfiglet.figlet_format("You-dl", font="slant")
    default_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'progress_hooks': [my_hook],
        'verbose': False,
        'http_chunk_size': 2097152000,
        'logger': MyLogger(),

        #'merge_output_format': 'mp4',
    }
    print(f"[bold red]{result}[/bold red]")
    print(f"[bold #fec601]Hi, Welcome to You-dl[/bold #fec601]")
    url = None
    try:
        url = questions.start_1()
    except Exception as e:
        print(e)
        sys.exit(1)
    user_opts = iy.opts(url)
    #print(user_opts)
    if not user_opts:
        print("[bold red]Use keyboard for selection[/bold red]")
        sys.exit(1)
        
    ydl_opts = dict(default_opts, **user_opts)
    # print(ydl_opts)
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            with progress:
                time.sleep(0.3)
                task_id = progress.add_task("Loading...", start=False)
                progress.start_task(0)
                ydl.download([url])
    except:
        pass

def main():
    try: 
        run()

    except KeyboardInterrupt:
        print("it happen")
        sys.exit(1)
    except TypeError:
        #print("[bold red]Check network connection and try again.[/bold red]")
        sys.exit(1)
    except KeyError:
        print("[bold red]Use keyboard for selection[/bold red]")
        sys.exit(1)
    except ValueError:
        print("[bold red]Use keyboard for selection[/bold red]")
        sys.exit(1)
    except Exception as e:
        print(f"[red]{e}[/red]")
        sys.exit(1)


main()

# type error when net is of and Index error when invalid query
# song_name Please try again with a different keyword.
