from collections import namedtuple
import frontmatter
import logging
import os
import yaml
import shutil

from collections import UserDict
from jinja2 import Template
from markdown2 import markdown
from pathlib import Path

from .menu import Menu

logger = logging.getLogger(__name__)


class NabuConfig(UserDict):
    def __init__(self, filename="config.yml"):
        with open(filename, "r") as fp:
            data = yaml.load(fp, Loader=yaml.FullLoader)

        super().__init__(data)

class Nabu:
    def __init__(self, config):
        self.config = config
        self.output_path = Path(config['output_folder'])
        self.content_path = Path(config['content_folder'])
        self.menu = Menu(config)

    def render_to_file(self):
        try:
            shutil.rmtree(self.output_path)
        except FileNotFoundError:
            pass
        finally:
            os.makedirs(self.output_path)
            shutil.copyfile(Path('assets/styles.css'), self.output_path / 'styles.css')
            shutil.copyfile(Path('assets/book.css'), self.output_path / 'book.css')
            shutil.copytree(Path('assets/fonts/'), self.output_path / 'fonts')

        self.menu.render_all(self.output_path)