from guillotina import configure
from guillotina.db.interfaces import IWriter
from guillotina.db.writer import Writer as DefaultWriter
from guillotina_numpy.interfaces import INumPyData

import io
import numpy


@configure.adapter(for_=(INumPyData), provides=IWriter)
class Writer(DefaultWriter):
    def serialize(self):
        output = io.BytesIO()
        numpy.savez_compressed(output, v=self._obj.value)
        output.seek(0)
        return output.read()
