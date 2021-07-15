import os
import time

from zipfile import ZipFile, BadZipFile


class EpubExtractor:
    def __init__(self) -> None:
        self.epubs_dir = os.getcwd() + f"\\media\\epubs\\"

    def format_title(self, epub_path):
        # long_novel_title_100-150_FIN.epub
        title = (
            epub_path.replace(self.epubs_dir, "")
            .replace("_FIN", "")
            .replace(".epub", "")
            .split("_")
        )
        number = title[-1]

        if "-" in number:
            start, end = number.split("-")
            number_list = range(int(start), int(end))
        else:
            number_list = [int(number)]

        return "_".join(title[:-1]), number_list

    def simple_extract(self, epub_path):
        # chapter_3.xhtml
        title, number_list = self.format_title(epub_path)
        chapters = [f"OEBPS/chapter_{item}.xhtml" for item in number_list]

        try:

            with ZipFile(epub_path, "r") as zip:
                novel_dir = f"media/novel_quepubs/{title}"

                for item in zip.namelist():
                    path = novel_dir + "/" + item
                    if "chapter" not in item or os.path.exists(
                        path.replace("/OEBPS", "")
                    ):
                        continue

                    zip.extract(item, path=novel_dir)
                    os.rename(path, path.replace("/OEBPS", ""))
        except BadZipFile:
            print(f" {title} File is not a zip file")
            os.remove(epub_path)
            return None

        print(title)
        return title

    def extract_all(self):
        epub_paths = [self.epubs_dir + item for item in os.listdir(self.epubs_dir)]

        novel_list = []
        for epub_path in epub_paths:
            novel_title = self.simple_extract(epub_path)
            if novel_title is None:
                continue
            novel_list.append(novel_title)
            os.remove(epub_path)

        return set(novel_list)


if __name__ == "__main__":
    EpubExtractor().extract_all()
