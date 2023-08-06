import typing
import zipfile
from lxml import etree as tree
from .types.book import Book
from PIL import Image
import weasyprint
import os


class EasyEpub:
    def __init__(self, book: typing.Optional[str]):
        self.book = book
        self.parser = Parser(self.book)

    @property
    def meta(self) -> Book:
        """
        :return: returns dictionary with a book metadata.
        """
        return Book(**self.parser.get_book_meta())

    def get_cover(self, path: typing.Optional[str]) -> typing.Optional[str]:
        """
        :param path: save path for a cover image.
        :return: returns path to the saved file.
        """
        return Parser(self.book).get_book_cover(path)

    def get_content(self, path: typing.Optional[str]) -> typing.Optional[str]:
        """
        :param path: save path for content.
        :return: returns path to the saved chapters.
        """
        return Prepare(Parser(self.book).get_book_content(path)).html_to_png()


class Parser:
    def __init__(self, book: typing.Optional[str]):
        """
        :param book: string path object to
        """
        self.book: typing.Optional[str] = book

    def get_book_meta(self) -> typing.Optional[dict]:
        """
        :return: returns dictionary with a book metadata.
        """
        namespaces = {
            "n": "urn:oasis:names:tc:opendocument:xmlns:container",
            "pkg": "http://www.idpf.org/2007/opf",
            "dc": "http://purl.org/dc/elements/1.1/"
        }
        opened_book = zipfile.ZipFile(self.book)
        meta = tree.fromstring(opened_book.read("META-INF/container.xml")
                               ).xpath("n:rootfiles/n:rootfile/@full-path", namespaces=namespaces)[0]
        opened_meta = opened_book.read(meta)
        book_data = tree.fromstring(opened_meta).xpath('/pkg:package/pkg:metadata', namespaces=namespaces)[0]

        received_data = {}
        for selected in ["identifier", "title", "creator", "date", "language"]:
            received_data[selected] = book_data.xpath("dc:%s/text()" % selected, namespaces=namespaces)[0]
        zipfile.ZipFile.close(opened_book)

        return {
            "uid": received_data["identifier"],
            "title": received_data["title"],
            "author": received_data["creator"],
            "creation_date": received_data["date"],
            "language": received_data["language"],
        }

    def get_book_cover(self, path: typing.Optional[str]) -> typing.Optional[str]:
        """
        :param path: save path for a cover image.
        :return: returns path to the saved file.
        """
        opened_book = zipfile.ZipFile(self.book)
        for file in opened_book.namelist():
            try:
                if file.split("OEBPS/assets/cover")[1]:
                    if not os.path.exists(os.path.dirname(path)):
                        try:
                            os.makedirs(os.path.dirname(path))
                        except:
                            pass
                    with open(path, "wb") as book:
                        book.write(opened_book.read(file))
                    opened_book.close()
                    book.close()
                    return os.path.abspath(path)
                else:
                    return None
            except:
                pass
        raise TypeError("Failed to grab a book cover.")

    def get_book_content(self, path: typing.Optional[str]) -> typing.Optional[str]:
        """
        :param path: save path for content.
        :return: returns path to the saved chapters.
        """
        opened_book = zipfile.ZipFile(self.book)
        if not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path))
            except:
                pass
        try:
            opened_book.extractall(path)
            return os.path.abspath(path)
        except:
            opened_book.close()
            raise TypeError("Failed to grab a book content.")


class Prepare:
    def __init__(self, path: typing.Optional[str]):
        self.path: typing.Optional[str] = path

    def html_to_png(self) -> typing.Optional[str]:
        if not os.path.exists(f"{self.path}/chapters"):
            try:
                os.makedirs(f"{self.path}/chapters")
            except:
                pass
        if not os.path.exists(f"{self.path}/OEBPS"):
            raise Exception("Book does not prepared.")

        chapters: typing.Optional[list] = []
        for file in os.listdir(f"{self.path}/OEBPS"):
            try:
                if file.split("ch")[1]:
                    chapters.append(file)
            except:
                pass
        for chapter in sorted(chapters, key=lambda x: x.split("ch")[1].split(".html")[0]):
            try:
                os.makedirs(f"{self.path}/chapters/{chapter.split('.html')[0]}")
            except:
                pass
            try:
                image = weasyprint.HTML(f"{self.path}/OEBPS/{chapter}").write_png()
                open(f"{self.path}/chapters/{chapter.split('.html')[0]}/{chapter.split('.html')[0]}.png", "wb").write(image)
                self.slice_image(f"{self.path}/chapters/{chapter.split('.html')[0]}/{chapter.split('.html')[0]}.png")
            except:
                pass
        return f"{self.path}/chapters/"

    @staticmethod
    def slice_image(image_path: typing.Optional[str]):
        im = Image.open(image_path)
        im.close()
        upper, bottom = 0, 1020
        for i in range(0, (im.size[1] // 1020)):
            im = Image.open(image_path)
            im = im.crop((0, upper, im.size[0], bottom))
            im.save(f"{os.path.dirname(image_path)}/{i}.png")
            upper += 1020
            bottom += 1020
        os.remove(image_path)
