import time
import datetime
from DiscordChatExporter import DiscordChatExporter
from EpubExtractor import EpubExtractor
from ChapterToQU import ChapterToQU

from EpubDownloader import EpubDownloader
from Extras import Utils

from setup_django import setup_django

setup_django()


def filter_data(data):
    return [msg["attachments"][0] for msg in data if msg["attachments"] != []]


def main():

    while True:
        borders = "+-" + "-" * 70 + "-+"
        print(borders)

        time_limmit = 4.5 * 60

        start = time.perf_counter()

        # channel '?? QUReup / qureup_epubs'
        channels = "572588422196101140"
        hours = 1

        data = DiscordChatExporter().get_discord_V2(hours, channels)
        data = filter_data(data)

        print("\nDownloading....")
        EpubDownloader().download(data)

        print("\nExtracting....")
        novel_list = EpubExtractor().extract_all()

        print("\nAdding to database....")
        ChapterToQU().addto_db(novel_list)

        elapsed = time.perf_counter() - start
        time_allowed = time_limmit - elapsed

        # Utils(timed=time_allowed).fix_missing()
        Utils(timed=time_allowed).remove_duplicates(novel_list)

        elapsed = time.perf_counter() - start
        msg = f"\nThe task took {int(elapsed)} seconds..."
        print(msg)

        delay = time_limmit - elapsed
        if delay < 0:
            continue
        next_run = (
            datetime.datetime.today() + datetime.timedelta(seconds=delay)
        ).strftime("%H:%M")
        print(f"Waiting {delay / 60} min... \nNext run at {next_run} ")
        time.sleep(delay)


if __name__ == "__main__":
    main()
