<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#sec-1">1. Source</a></li>
<li><a href="#sec-2">2. Pypi</a></li>
</ul>
</div>
</div>

DamePhoto by David Arroyo Menéndez

# Source<a id="sec-1" name="sec-1"></a>

This source is modified from <https://github.com/smahesh29/Gender-and-Age-Detection>
and redistributed under GPLv3.

This source is only for gender detection.

# Pypi<a id="sec-2" name="sec-2"></a>

-   To install from local:

$ pip install -e .

-   To install create tar.gz in dist directory:

$ python3 setup.py register sdist

-   To upload to pypi:

$ twine upload dist/damephoto-0.1.tar.gz

-   You can install from Internet in a python virtual environment to check:

$ python3 -m venv /tmp/funny
$ cd /tmp/funny
$ source bin/activate
$ pip3 install damephoto