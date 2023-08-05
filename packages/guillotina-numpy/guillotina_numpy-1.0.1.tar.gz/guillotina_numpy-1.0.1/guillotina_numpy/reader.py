import io
import numpy


def reader(result):
    buff = io.BytesIO(result["state"])
    from guillotina_numpy.field import NumPyData

    obj = NumPyData()
    obj.value = numpy.load(buff)["v"]
    obj.__uuid__ = result["zoid"]
    obj.__serial__ = result["tid"]
    obj.__name__ = result["id"]
    return obj
