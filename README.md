MongoBibDesk
============

This is an experimental project to host bibliographic data in MongoDB.

Some notes
----------

1. *Goal:* to mirror BibDesk bibliographies onto a MongoDB server.
2. *Why?* Hosting bibliographic data in a convenient database may make machine-learning and linguistic analysis of an academic corpus more convenient. [pyarxiv] is a good example. It also paves the way to a cloud-based, BibDesk-integrated, experience. Put BibDesk in the browser? Put BibDesk on the iPad? *Yes we can.*
3. *Why integrate with BibDesk?* BibDesk's native datastore is pure BibTeX, which makes it easy to integrate in an academic publishing workflow. This project *could* use any library that parses BibTeX, but frankly, a lot of them crashed in my cursory tests. BibDesk has a robust---forgiving---parser and has nice extras, like attachments for PDFs. In principle, the `BibDeskInterface` class could be generalized for anyone's BibTeX parser.
4. *How do you integrate with BibDesk?* I use py-appscript, the Python-AppleScript bridge. Its surprisingly nice to work with.
5. *Why Python?* It rocks.
6. *Why MongoDB?* Its schema-less, easy to use, and easy to query.

Dependencies
------------

* Python 2.x
* a running [MongoDB] server on the localhost
* [PyMongo]
* [py-appscript]


Contact
-------

Created an maintained by Jonathan Sick (jonathansick /at/ mac /dot/ com).

[pyarxiv]: https://github.com/dfm/pyarxiv
[MongoDB]: http://www.mongodb.org
[PyMongo]: http://api.mongodb.org/python/current/
[py-appscript]: http://appscript.sourceforge.net/py-appscript/index.html
