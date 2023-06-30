from discord import opus

#OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']

#def load_opus_lib(opus_libs=OPUS_LIBS):
def load_opus_lib():
    if opus.is_loaded():
        #return True
        return

    '''
    for opus_lib in opus_libs:
        try:
            opus.load_opus(opus_lib)
            return
        except OSError:
            pass
    '''
    try:
        opus._load_default()
        return
    except OSError:
        pass

    #raise RuntimeError('Could not load an opus lib. Tried %s' % (', '.join(opus_libs)))
    raise RuntimeError("Could not load an opus lib.")
