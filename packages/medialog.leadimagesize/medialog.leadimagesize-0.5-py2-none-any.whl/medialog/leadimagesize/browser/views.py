from io import StringIO
from PIL import Image
from PIL.PngImagePlugin import PngImageFile

from zope.interface import implements, Interface
from Products.Five import BrowserView
from zope import schema


class IRotateR(Interface):
    """ Rotate Image view interface """

    def test():
        """ test method"""

class RotateR(BrowserView):
    """ A browser view to rotate image """

    def __call__(self, REQUEST):
        im = Image.open(StringIO(self.context.image.data))
        im.rotate(90)
        self.context.image =  im
        self.context.image.rotate(90)
        self.context.reindexObject()
