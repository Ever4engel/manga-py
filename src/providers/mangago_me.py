from src.provider import Provider
from .helpers.std import Std


class MangaGoMe(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        tp = self.re.search('/(mf|raw)', self.get_current_chapter()).group(1)
        return 'vol_{:0>3}-{}-{}'.format(*idx, tp)

    def get_chapter_index(self) -> str:
        selector = r'/(?:mf|raw)/.*?(\d+)(?:\.(\d+))?'
        chapter = self.get_current_chapter()
        idx = self.re.search(selector, chapter).groups()
        return '{}-{}'.format(*self._idx_to_x2(idx))

    def get_main_content(self):
        url = '{}/read-manga/{}/'.format(self.get_domain(), self.get_manga_name())
        return self.html_fromstring(url, '#information', 0)

    def get_manga_name(self) -> str:
        return self.re.search(r'/read-manga/([^/]+)/', self.get_url()).group(1)

    def get_chapters(self):
        content = self.get_storage_content()
        chapters = content.cssselect('#chapter_table a.chico')
        raws = content.cssselect('#raws_table a.chicor')
        return chapters + raws

    def prepare_cookies(self):
        self.cf_protect(self.get_url())

    def get_files(self):
        content = self.http_get(self.get_current_chapter())
        parser = self.re.search("imgsrcs.+[^.]+?var.+?=\s?'(.+)'", content)
        if not parser:
            return []
        return parser.group(0).split(',')

    def get_cover(self):
        pass  # TODO


main = MangaGoMe
