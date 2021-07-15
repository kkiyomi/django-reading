import os
import json
import time
import datetime
import subprocess
import logging

logger = logging.Logger("catch_all")


class DiscordChatExporter:
    def __init__(self, token=None) -> None:

        self.token = token
        if not self.token:
            self.token = self.load_token()

        self.app_path = "C:\\Users\\user\\Desktop\\smt\\Downloads\\DiscordChatExporter.CLI\\DiscordChatExporter.Cli.exe"

        self.chat_path = os.getcwd() + f"\\media\\discord\\discord.json"

    def load_token(self):
        credentials = os.getcwd() + f"\\scripts\\credentials.json"
        return self.loadfile_asjs(credentials)["token"]

    def loadfile_asjs(self, filename):
        with open(filename, encoding="utf-8") as outfile:
            return json.load(outfile)

    def get_discord(self, hours, channel):
        last_hour_date_time = (
            datetime.datetime.today() - datetime.timedelta(hours=hours)
        ).strftime("%Y-%m-%d %H:%M")

        if os.path.exists(self.chat_path):
            os.remove(self.chat_path)

        subprocess.run(
            f'{self.app_path} export -t {self.token} -c {channel} -f Json -o "{self.chat_path}" --after "{last_hour_date_time}"',
            shell=True,
            text=True,
        )

        discord = self.loadfile_asjs(self.chat_path)

        # data = [
        #     msg["attachments"][0]
        #     for msg in discord["messages"]
        #     if msg["attachments"] != []
        # ]
        return discord["messages"]

    def get_discord_V2(self, hours, channels):
        index = 0
        loop = True
        while loop:
            try:
                print(datetime.datetime.today().strftime("%Y-%m-%d %H:%M"))
                data = self.get_discord(hours, channels)
                loop = False
            except Exception as e:
                print("get_discord_V2 error")
                logger.exception(e)
                time.sleep(20)
                index += 1
                if index >= 3:
                    print("repeated errors")
                    time.sleep(5 * 60)
        return data
