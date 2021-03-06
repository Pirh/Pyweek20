"""
Monkey-patching defects in libraries AGAIN
"""


def fix_openal_get_extensions(self):
    extensions = alc.alcGetString(self._device, alc.ALC_EXTENSIONS)
    if pyglet.compat_platform == 'darwin' or pyglet.compat_platform.startswith('linux'):
        return ctypes.cast(extensions, ctypes.c_char_p).value.split(b' ') # Python 3 fix here
    else:
        return _split_nul_strings(extensions)

def patch():
    try:
        from pyglet.media.drivers.openal import OpenALDriver
        OpenALDriver.get_extensions = fix_openal_get_extensions
    except ImportError:
        pass
