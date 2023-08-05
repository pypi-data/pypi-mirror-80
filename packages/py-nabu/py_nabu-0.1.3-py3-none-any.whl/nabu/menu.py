from collections import UserDict
from os import stat
from pathlib import Path
from markdown2 import markdown

from .page import Page


class Menu(UserDict):
    def __init__(self, config):
        self.template = Path(config.get('template', 'templates/bootstrap/page.html'))

        menu = config['menu']
        basedir = Path(config.get('content_folder', 'content'))

        self.data = dict()

        self.root = Page(basedir, menu=self)
        self.root.slug = ''

        for chapter, pages in menu.items():
            parent_path = basedir / chapter
            parent = Page(parent_path, menu=self)

            if not pages and parent.metadata.get('autolist'):
                pages = parent.find_siblings()

            self.data[parent] = list()
            for page in pages:
                if not page.endswith('.md'):
                    page = page + '.md'
                path = basedir / chapter / page
                print(path)
                p = Page(path, parent=parent, menu=self)
                print(p)
                
                if p:
                    self.data[parent].append(p)

    @staticmethod
    def make_markdown_item(page, level):
        return '  ' * level + f" * [{page.title}]({page.url})\n"

    def markdown(self, pages=None, level=0):
        md = ''
        if pages is None:
            pages = self.data

        if isinstance(pages, list):
            md += ''.join([self.make_markdown_item(page, level) for page in pages])
        elif isinstance(pages, dict):
            for page in pages.keys():
                md += self.make_markdown_item(page, level)
                for subpage in pages[page]:
                    if isinstance(subpage, dict):
                        md += self.markdown(pages['page'], level+1)
                    else:
                        md += self.make_markdown_item(subpage, level+1)
        return md

    def render_all(self, output_path):
        self.root.render(output_path, self.template)
        for bundle in self.data:
            bundle.render(output_path, self.template)