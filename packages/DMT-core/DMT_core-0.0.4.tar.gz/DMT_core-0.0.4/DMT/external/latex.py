""" DMT supplied build latex command
"""
# DMT
# Copyright (C) 2019  Markus Müller and Mario Krattenmacher and the DMT contributors <https://gitlab.hrz.tu-chemnitz.de/CEDIC_Bipolar/DMT/>
#
# This file is part of DMT.
#
# DMT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DMT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
import subprocess
from pathlib import Path

from DMT.external.os import cd

def build_tex(full_path_to_file, additional_compiler=None, wait=False):
    r""" Builds a tex file

    Parameters
    ------------
    full_path_to_file : str or os.Pathlike
    additional_compiler: (str , [str])
        If a additional tex compiler should be used, supply it here. It will be tried as first compiler.
        The additional compiler must be given in this argument with (<call_of_compiler>, List of compiler arguments).
        For example 'latexmk' looks like: ('latexmk', ['--interaction=nonstopmode', '--shell-escape', '--pdf'])
    wait : Boolean, False
        Wait for the build to complete.
    """
    if not isinstance(full_path_to_file, Path):
        full_path_to_file = Path(full_path_to_file)

    directory = full_path_to_file.parent
    file_name = full_path_to_file.name
    if file_name.endswith('.tex'):
        file_name = [file_name]
    else:
        file_name = [file_name + '.tex']

    with cd(directory):
        compilers = (
            ('latexmk', ['--interaction=nonstopmode', '--shell-escape', '--pdf']),
            ('lualatex', ['--interaction=nonstopmode', '--shell-escape']),
            ('pdflatex', ['--interaction=nonstopmode', '--shell-escape'])
        )
        if additional_compiler is not None and additional_compiler[0] is not None:
            compilers = (additional_compiler,) + compilers

        # os_error = None

        for compiler, arguments in compilers:
            command = [compiler] + arguments + file_name

            # try:
            if wait:
                # output = subprocess.call(command, stderr=subprocess.STDOUT)
                subprocess.call(command, stderr=subprocess.STDOUT)
            else:
                # output = subprocess.Popen(command, stderr=subprocess.STDOUT)
                subprocess.Popen(command, stderr=subprocess.STDOUT)
            # except (OSError, IOError) as e:
            #     # Use FileNotFoundError when python 2 is dropped
            #     os_error = e

            #     if os_error.errno == errno.ENOENT:
            #         # If compiler does not exist, try next in the list
            #         continue
            #     raise
            # except subprocess.CalledProcessError as e:
            #     # For all other errors print the output and raise the error
            #     print(e.output.decode())
            #     continue
            #     # raise
            # else:
            #     print(output.decode())

            # Compilation has finished, so no further compilers have to be
            # tried
            return

        # Notify user that none of the compilers worked.
        raise(IOError(
            'No LaTex compiler was found\n' +
            'Make sure you have latexmk, lualatex or pdfLaTex installed and in your PATH environment.'
        ))

def build_svg(full_path_to_file, wait=True):
    r""" Builds a tex file to scalable vector graphic.

    Parameters
    ------------
    full_path_to_file : str or os.Pathlike
    """
    if not isinstance(full_path_to_file, Path):
        full_path_to_file = Path(full_path_to_file)
    directory = full_path_to_file.parent
    file_name = full_path_to_file.name.replace('.tex', '')

    with cd(directory):
        # call latex to compile dvi
        command = ['latex', '--interaction=nonstopmode', file_name + '.tex']
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        except (OSError, IOError, subprocess.CalledProcessError) as e:
            # For all these errors print the output and raise the error
            print(e.output.decode())
            # raise
        else:
            print(output.decode())

        # call dvisvgm to compile dvi to svg
        command = ['dvisvgm', '--no-fonts', file_name]
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        except (OSError, IOError, subprocess.CalledProcessError) as e:
            # For all these errors print the output and raise the error
            print(e.output.decode())
            # raise
        else:
            print(output.decode())


def clean_tex_files(directory, file_name, keep=('.tex', '.pdf')):
    """ Deletes all intermediate files in the directory with name file_name except the tex and pdf.

    Parameters
    ---------------
    directory : str
        Direcory to clean
    file_name : str
        File name without file ending (!) to clean
    keep : iterable, optional
        File endings to keep
    """
    for file_curr in Path(directory).iterdir():
        if (file_name in file_curr.stem) and (file_curr.suffix not in keep):
            file_curr.unlink()
