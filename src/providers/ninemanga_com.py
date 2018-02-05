from .helpers.nine_helper import NineHelper


class NineMangaCom(NineHelper):
    _local_storage = None

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index(True).split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self, no_increment=False) -> str:
        return '{}'.format(self._chapter_index())

    def get_main_content(self):
        name = self.get_manga_name(False)
        return self.http_get('{}/manga/{}.html?waring=1'.format(self.get_domain(), name))

    def get_manga_name(self, normalize=True) -> str:
        if not self._local_storage:
            name = self.re_name(self.get_url())
            if name:
                self._local_storage = name.group(1)
            else:
                url = self.html_fromstring(self.get_url(), '.subgiude > li + li > a', 0).get('href')
                self._local_storage = self.re_name(url).group(1)
        return self.normalize_name(self._local_storage, normalize)

    def get_chapters(self):
        content = self.get_storage_content()
        result = self.document_fromstring(content, '.chapterbox li a.chapter_list_a')
        if not result:
            return []
        items = []
        for i in result:
            u = self.re.search('(/chapter/.*/\d+)\\.html', i.get('href'))
            items.append('{}{}-10-1.html'.format(self.get_domain(), u.group(1)))
        return items

    def get_files(self):
        content = self._get_page_content(self.get_current_chapter())
        pages = self.document_fromstring(content, '.changepage #page option + option')
        images = self.get_files_on_page(content)
        for i in pages:
            url = self.http().normalize_uri(i.get('value'))
            content = self._get_page_content(url)
            images += self.get_files_on_page(content)
        return images


main = NineMangaCom
