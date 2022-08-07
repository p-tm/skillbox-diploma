"""
Парсер html-файла с хелпом

"""
import re

from dataclasses import dataclass
from typing import Callable, Iterable, List

@dataclass
class HelpParser:

    _raw: str           # содержание html-файла
    _src: str           # содежрание html-файла в одну строку

    def __init__(self, src_file: str):

        with open(src_file, mode='r', encoding='utf-8') as f:
            tmp: str = f.read()

        self._raw = tmp
        self._src = re.sub(r'\n *', ' ', tmp, flags=re.DOTALL)

    def get_main_page(self):
        """
        Формирует первое сообщение

        :return: содержание первой страницы (сообщения в Telegram) хелпа

        """
        page: str = self.between_tags(self._src, '<div class="main_page">', '</div>').__next__()
        return self.get_page_content(page)


    def get_next_page(self, cmd: str):
        """
        Формирует сообщения с описанием каждой из команд

        :return: содержание первой страницы (сообщения в Telegram) хелпа

        """
        page: str = self.between_tags(self._src, '<div class="{} cmd".*?>'.format(cmd), '</div>').__next__()
        return self.get_page_content(page)

    def get_page_content(self, page: str):
        """
        Вспомогательная - парсит описание конкретной команды

        :param page: кусок html-файла с описание конкретной команды
        :return: описание по конкретной команде для чата Telegram
        """
        hdr_naked: str = self.between_tags(page, '<p class="header.*?">', '</p>').__next__()
        header: str = '<b>{}</b>\n'.format(hdr_naked)
        subheader: str = self.between_tags(page, '<p class="subheader">', '</p>').__next__()
        add_bullet: Callable = lambda x: ('🔹 ' + x) if x else ''
        body: List = [add_bullet(piece) for piece in self.between_tags(page, '<li>', '</li>')]
        footers: List = [piece for piece in self.between_tags(page, '<p class="footer">', '</p>')]
        return '{}{}\n{}{}'.format(header, subheader, ''.join(body), '\n'.join(footers))

    def between_tags(self, src: str, tb: str, te: str) -> Iterable[str]:
        """
        Выбирает кусок тескта между заданными текстовыми шаблонами
        (в данном случае предполагается указывать два html-тэга

        :param src: исходный текст
        :param tb: начальный тег
        :param te: конечный тег
        :return: список полученных значений

        """
        template = r'{}(.*?){}'.format(tb, te)
        tmp_list: List = re.findall(template, src, flags=re.DOTALL)
        if not tmp_list:
            yield ''
        for piece in re.findall(template, src, flags=re.DOTALL):
            res: str = piece.rstrip().lstrip()
            # обрезаем все тэги, которые не понимает Telegram
            res = re.sub(r'<a.*?>', '', res, flags=re.DOTALL)
            res = re.sub(r'</a>', '', res, flags=re.DOTALL)
            yield '{}\n'.format(res)

    def get_help_buttons(self):
        """
        Выбирает все команды, описание которырх содержится в файле

        """
        template = r'<div class="(.*) cmd'
        return re.findall(template, self._raw)



