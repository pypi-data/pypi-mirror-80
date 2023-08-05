# Field to store a numpy array
from guillotina import configure
from guillotina import schema
from guillotina.db.orm.base import BaseObject
from guillotina.exceptions import ValueDeserializationError
from guillotina.interfaces import IAnnotations
from guillotina.interfaces import IContentBehavior
from guillotina_numpy.interfaces import INumPyArrayField
from guillotina_numpy.interfaces import INumPyData
from guillotina_numpy.reader import reader
from zope.interface import implementer

_default = object()


@implementer(INumPyData)
class NumPyData(BaseObject):
    """
    store data on basic dictionary object but also inherit from base object
    """

    value = None


class NumPyArrayValue:

    # need to store

    def __init__(self, numpy_annotation_prefix="numpy"):
        self.prefix = numpy_annotation_prefix

    async def get(self, context, create=True):
        annotations_container = IAnnotations(context)
        numpy_object = annotations_container.get(self.prefix, _default)
        if numpy_object is _default:
            # needs to be loaded
            numpy_object = await annotations_container.async_get(
                self.prefix, _default, reader=reader
            )
        if numpy_object is _default:
            return None
        return numpy_object

    async def set(self, context, value):
        # create
        annotations_container = IAnnotations(context)
        obj = NumPyData()
        obj.value = value
        obj.register()
        await annotations_container.async_set(self.prefix, obj)


@implementer(INumPyArrayField)
class NumPyArrayField(schema.Field):
    async def set(self, obj, value):

        if IContentBehavior.providedBy(obj):
            anno_context = obj.__dict__["context"]
            self.__key_name__ = (
                obj.__dict__["schema"].__identifier__ + "." + self.__name__
            )
        else:
            anno_context = obj
            self.__key_name__ = self.__name__

        subobj = NumPyArrayValue("numpy." + self.__key_name__)
        await subobj.set(anno_context, value)

        setattr(anno_context, self.__key_name__, subobj)
        anno_context.register()


@configure.value_deserializer(INumPyArrayField)
def field_converter(field, value, context):
    raise ValueDeserializationError(field, value, f"Not valid to set on API")


@configure.value_serializer(NumPyArrayValue)
def numpy_serializer(value):
    if value is None:
        return
    return {"len": len(value)}
