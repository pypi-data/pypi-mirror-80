# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['trio_gtk']
install_requires = \
['PyGObject>=3.38.0,<4.0.0', 'trio>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'trio-gtk',
    'version': '0.1.0',
    'description': 'Trio guest mode wrapper for PyGTK',
    'long_description': '# trio-gtk\n\n[![Build Status](https://drone.autonomic.zone/api/badges/decentral1se/trio-gtk/status.svg)](https://drone.autonomic.zone/decentral1se/trio-gtk)\n\n## Trio guest mode wrapper for PyGTK\n\nUsing the [Trio guest mode](https://trio.readthedocs.io/en/latest/reference-lowlevel.html#using-guest-mode-to-run-trio-on-top-of-other-event-loops) feature, we can run both the Trio and PyGTK event loops alongside each other in a single program. This allows us to make use of the Trio library and the usual `async`/`await` syntax and not have to directly manage thread pools.\n\nThis library provides a thin wrapper for initialising the guest mode and exposes a single public API function, `trio_gtk.run` into which you can pass your Trio main function. This function must accept a `nursery` argument which can spawn child tasks for the duration of the host loop.\n\n## Install\n\n```sh\n$ pip install trio-gtk\n```\n\n## Example\n\n```python\nimport gi\nimport trio\n\ngi.require_version("Gtk", "3.0")\n\nfrom gi.repository import Gtk as gtk\n\nimport trio_gtk\n\n\nclass Example(gtk.Window):\n    def __init__(self, nursery):\n        gtk.Window.__init__(self, title="Example")\n\n        self.button = gtk.Button(label="Create a task")\n        self.button.connect("clicked", self.on_click)\n        self.add(self.button)\n\n        self.counter = 0\n        self.nursery = nursery\n\n        self.connect("destroy", gtk.main_quit)\n        self.show_all()\n\n    def on_click(self, widget):\n        self.counter += 1\n        self.nursery.start_soon(self.say_hi, self.counter)\n\n    async def say_hi(self, count):\n        while True:\n            await trio.sleep(1)\n            print(f"hi from task {count}")\n\n\nasync def main(nursery):\n    Example(nursery)\n\n\ntrio_gtk.run(main)\n```\n',
    'author': 'decentral1se',
    'author_email': 'lukewm@riseup.net',
    'maintainer': 'decentral1se',
    'maintainer_email': 'lukewm@riseup.net',
    'url': 'https://github.com/decentral1se/trio-gtk',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
