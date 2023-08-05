from guillotina import schema
from guillotina.fields import CloudFileField
from guillotina.schema.interfaces import IField
from guillotina.schema.interfaces import IObject
from zope.interface import Attribute
from zope.interface import Interface


class INumPyData(Interface):

    value = Attribute("Real value")


class INumPyArrayField(IField):
    pass


class IModelField(IObject):
    """Model field"""


class IModelFieldSchema(Interface):
    """Model field schema"""

    type_model = schema.ASCII(title="Type of model", default="tf")

    file = CloudFileField(title="Model binary file")

    version = schema.Int(title="Version of the model", default=1)
