import frontmatter
import glob
import logging
import os

from jinja2 import Template
from markdown2 import markdown
from pathlib import Path, PurePosixPath

logger = logging.getLogger(__name__)

class Page:
    def __new__(cls, source, **kwargs):
        if not source.exists() or not os.access(source, os.R_OK):
            return None

        instance = object.__new__(cls)
        return instance

    def __init__(self, source, parent=None, menu=None):
        if source.is_dir():
            source = source / 'index.md'

        self.source = source
        self.parent = parent
        self.menu = menu

        self.children = list()
        if parent:
            self.parent.add_child(self)

        self.metadata = dict()
        self.markdown = None
        try:
            with open(source, 'r') as fp:
                data = frontmatter.load(fp)
                self.metadata = data.metadata
                self.markdown = data.content
        except FileNotFoundError:
            pass

        if not self.parent:
            self.slug = self.source.parent.name
        else:
            self.slug = self.metadata.get('slug', f'{self.source.stem}.html')
            if not self.slug.endswith('.html'):
                self.slug = self.slug + '.html'

    def add_child(self, child):
        self.children.append(child)

    def find_siblings(self):
        paths = [Path(p).name for p in glob.glob(f'{self.source.parent}/*.md')]
        return [p for p in paths if p != 'index.md']

    @property
    def title(self):
        return self.metadata.get('title', self.source.parent.name)

    @property
    def url(self):
        url = self.build_output_dir(PurePosixPath('/'))
        if self.parent: url = url / self.slug
        else: url = url / 'index.html'

        return url

    def build_output_dir(self, basedir):
        if self.parent:
            return self.parent.build_output_dir(basedir)
        else:
            return Path(basedir) / self.slug

    def build_output_path(self, basedir):
        path = self.build_output_dir(basedir)

        if not path.exists():
            os.makedirs(path)

        if self.parent: return path / self.slug
        else: return path / 'index.html'

    def render(self, output_path, template_file):
        if not self.markdown:
            self.markdown = self.menu.markdown(self.children)

        if self.metadata.get('toc'):
            self.markdown += "\n\n## Table of contents\n"
            self.markdown += self.menu.markdown(self.children)

        content = markdown(self.markdown, extras={
            'fenced-code-blocks': None,
            'codehilite': None,
            'tables': None,
            'html-classes': {'table': 'table'}
        })

        with open(template_file, 'r') as fp:
            template = Template(fp.read())
            
        data = template.render(content=content, menu=self.menu, metadata=self.metadata)

        full_output_path = self.build_output_path(output_path)

        with open(full_output_path, 'w') as fp:
            success = fp.write(data)

        print("RENDER: ", self.source)
        for page in self.children:
            page.render(output_path, template_file)

        return success

    def __str__(self):
        return f"<Page '{self.source}'>"

    __repr__ = __str__
