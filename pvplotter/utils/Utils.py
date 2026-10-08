import os
import warnings


#------------------------------------------------------------------------
#    searchForFilesExt
#------------------------------------------------------------------------
# This function searches for files in a directory ('path') with a given
# extension 'ext', e.g., '.pro'. The argument path is usually 
# equal to __file__.

def searchForFilesExt(ext: str, path: str='') -> list:

    if path == '':
        currDir = os.getcwd()

    res = [f for f in os.listdir(currDir) if f.endswith(ext)]

    return res

#------------------------------------------------------------------------
#    getFile
#------------------------------------------------------------------------

def getFile(it: int, ext: str) -> str:

        ext = str(it) + '.' + ext # file extension

        fnames = searchForFilesExt(ext)

        if len(fnames) > 1:
            warnings.warn(
                f'more than one file with extension \'{ext}\': {fnames}!')

        if len(fnames) == 0:
            warnings.warn(
                    f'none file with extension \'{ext}\' has been found!')
            
            return ''
        
        return fnames[0]
