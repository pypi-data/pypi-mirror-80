# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sock']
setup_kwargs = {
    'name': 'sock',
    'version': '0.5.0',
    'description': 'Small script to simplify network communication',
    'long_description': '# sock\n\nSmall script to simplify network communication.\n\nSomething like [telnetlib](http://docs.python.org/library/telnetlib.html), but for clean TCP/UDP (no command sequences, \\r\\n newlines, etc.)\n\nAs an alternative, consider [pwntools](http://pwntools.com/) which contains unified interface (tubes) for communications with sockets, processes, etc. See [tubes API](http://pwntools.com/).\n\nCurrent development only supports python 3. Old python 2 version is available at the py2 branch.\n\n## Installation\n\n```bash\n$ pip3 install sock\n```\n\nFor development or building from this repository, [poetry](https://python-poetry.org/) is needed.\n\n## Usage\n\n### TCP Client\n\n```python\nfrom sock import *\n\nf = Sock("some.cool.servi.ce:3123", timeout=10)\n# or IPv6\nf = Sock6("::1 3123", timeout=3)\n# or already existing socket\nf = Sock.from_socket(some_socket)  # or toSock(some_socket)\n# or UDP/IPv6\nf = SockU6("::1 3123", timeout=3)\n\n# wait for prompt (skip banner for example)\n# the prompt itself will be skipped (and returned) too\nf.read_until("> ", timeout=3)  # read_until_re also exists\n\nf.send("flip coin\\n")\n\n# skip until regexp\nresult1 = f.skip_until_re(r"You\'ve got (heads|tails)")  # skip_until(str) also exists\n\n# read until also consumes matched part\nf.read_until_re(r"You\'ve g[oe]t ")  # read_until(str) also exists\n\n# read specific number of bytes\nresult2 = f.read_nbytes(5)\n\nassert result1 == result2\n\n# alias for f.send(s + "\\n")\nf.send_line("random please")\n\n# read one packet and flush buffers\nprint(f.read_one())\n\n# non-blocking read (flush buffers)\nprint(f.read_one(0))\n\n# read until disconnect\nprint(f.read_all())\n```\n\n\nAbout\n---------------------\n\nAuthor: hellman\n\nLicense: [MIT License](http://opensource.org/licenses/MIT)\n',
    'author': 'hellman',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
