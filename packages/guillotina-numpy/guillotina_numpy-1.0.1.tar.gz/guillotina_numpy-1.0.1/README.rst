Guillotina Numpy
----------------

Adding a field that is stored as a numpy binary state


In order to configure::

    applications:
    - guillotina_numpy


Interface configuration::

    class IFoobarType(Interface):
    foobar = NumPyArrayField(
        required=False)
