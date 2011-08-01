#!/usr/bin/env python
# encoding: utf-8
"""
mongobibdesk

Load and displays BibDesk bibliographic data in a MongoDB database.

History
-------
2011-07-31 - Created by Jonathan Sick

Copyright 2011 Jonathan Sick

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import copy
import pymongo
import appscript

class BibDeskInterface(object):
    """Interfaces with a BibDesk document to get and set pub records."""
    def __init__(self):
        self.bd = None # appscript ref to the BibDesk app
        self.bdDoc = None # appscript ref to BibDesk document
        self.db = pymongo.Connection()['bibdesk']
        self.c = None # MongoDB collection

        # Replacement dictionary for stripping tex from the human-readable fields
        # see self.detex()
        self.texReplacements = {"{":"","}":"","~":" "}

    @classmethod
    def top_bibdesk_doc(cls):
        """Initialize and connect to the top-most BibDesk document."""
        instance = cls()
        instance.bd = appscript.app('BibDesk')
        instance.bdDoc = instance.bd.documents()[0] # top-most open doc in BibDesk
        # MongoDB collection name is full path to BibDesk document
        # collection names *can* include full-stops
        docPath = instance.bdDoc.file().path
        instance.c = instance.db[docPath]
        return instance

    def import_publications(self):
        """Import all publications from the connected BibDesk document."""
        for pub in self.bdDoc.publications():
            self.insert_publication(pub)

    def insert_publication(self, pub):
        """Inserts a BibDesk publication into the MongoDB collection."""
        bibtexFields = self.read_bibtex_fields(pub)
        bibString = pub.BibTeX_string() # raw BibTeX string
        citeKey = pub.cite_key()
        trimmedTitle = self.detex(pub.title())
        authorList = self.get_author_list(pub)

        # Assemble the document
        print "Inserting", trimmedTitle
        doc = {'cite_key': citeKey,
            'title': trimmedTitle,
            'authors': authorList,
            'bib': bibtexFields,
            'raw_bibtex': bibString}
        self.c.insert(doc)

    def read_bibtex_fields(self, pub):
        """Reads BibTeX fields for a BibDesk publication, returning a dict."""
        doc = {}
        for field in pub.fields():
            key = field.name()
            val = field.value()
            doc[key] = val
        return doc

    def get_author_list(self, pub):
        """Make a list of normalized, non-tex'd author names in First, Last
        format from a BibDesk pub.
        """
        authorList = [self.detex(author.name()) for author in pub.authors()]
        return authorList

    def detex(self,texStr):
        """Strip tex out of human-readable strings."""
        text = copy.copy(texStr)
        for i, j in self.texReplacements.iteritems():
            text = text.replace(i, j)
        return text


def load_bibdesk_doc():
    """Loads the top-most BibDesk document into MongoDB."""
    bdInterface = BibDeskInterface.top_bibdesk_doc()
    bdInterface.import_publications()

if __name__ == '__main__':
    load_bibdesk_doc()


