from guillotina import configure

app_settings = {
    # provide custom application settings here...
}


def includeme(root):
    """
    custom application initialization here
    """
    configure.scan("guillotina_numpy.field")
    configure.scan("guillotina_numpy.writer")
