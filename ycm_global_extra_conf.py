# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org/>

import os

# These are the compilation flags that will be used
# CHANGE THIS LIST OF FLAGS. YES, THIS IS THE DROID YOU HAVE BEEN LOOKING FOR.
flags = [
'-Wall',
'-Wextra',
'-Werror',
'-Wno-long-long',
'-Wno-variadic-macros',
'-fexceptions',
'-fPIC',
'-DNDEBUG',
# specify Qt include path
'-I',
'./arm-embedded/qt-embedded-4.8.5/include',
'-I',
'./arm-embedded/qt-embedded-4.8.5/include/QtCore',
'-I',
'./arm-embedded/qt-embedded-4.8.5/include/QtGui',
'-I',
'./arm-embedded/qt-embedded-4.8.5/include/QtNetwork',
# THIS IS IMPORTANT! Without a "-std=<something>" flag, clang won't know which
# language to use when compiling headers. So it will guess. Badly. So C++
# headers will be compiled as C headers. You don't want that so ALWAYS specify
# a "-std=<something>".
# For a C project, you would set this to something like 'c99' instead of
# 'c++11'.
'-std=c++11',
# ...and the same thing goes for the magic -x option which specifies the
# language that the files to be compiled are written in. This is mostly
# relevant for c++ headers.
# For a C project, you would set this to 'c' instead of 'c++'.
'-x',
'c++',
# specify c++ header file directory
'-I',
'/usr/include/i386-linux-gnu/c++/4.8',
]


def get_home_direction():
  return os.path.expanduser('~')


def relative_path_to_absolute(flags, base_directory):
  if not base_directory:
    return flags
  new_flags = []
  make_next_absolute = False
  path_flags = [ '-isystem', '-I', '-iquote', '--sysroot=' ]
  for flag in flags:
    new_flag = flag
    if make_next_absolute:
      make_next_absolute = False
      if not flag.startswith( '/' ):
        new_flag = os.path.join(base_directory, flag)
    for path_flag in path_flags:
      if flag == path_flag:
        make_next_absolute = True
        break
      if flag.startswith(path_flag):
        path = flag[len(path_flag): ]
        new_flag = path_flag + os.path.join(base_directory, path)
        break
    if new_flag:
      new_flags.append(new_flag)
  return new_flags


#For appending more custom flags specify in the project directory
def get_custom_flags(filename):
  extra_flags = []
  config_file_name = '.ycm_extra_flags'
  dirname = os.path.dirname(filename)
  while dirname != '/':
    try:
      extra_flags = [line.rstrip('\n') for line in open(
        os.path.join(dirname, config_file_name))]
      break
    except:
      pass
    dirname = os.path.dirname(dirname)
  return relative_path_to_absolute(extra_flags, dirname)


def FlagsForFile(filename):
  final_flags = relative_path_to_absolute(flags, get_home_direction()) \
      + get_custom_flags(filename)
  
  return {
    'flags': final_flags,
    'do_cache': True
  }

# vim: sw=2 ts=2
