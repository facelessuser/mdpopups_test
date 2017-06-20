import sublime
import subprocess
import tempfile
import os
import base64


class TempFile(object):
    """Open either a temporary HTML or one at the save location."""

    def __enter__(self):
        """Setup HTML file."""

        self.file = tempfile.NamedTemporaryFile(mode='bw+', delete=True, suffix='png')
        return self.file

    def __exit__(self, type, value, traceback):
        """Tear down HTML file."""

        self.file.close()


def escape_code(text, tab_size=4):
    """Format text to HTML."""

    encode_table = {
        '&': '&amp;',
        '>': '&gt;',
        '<': '&lt;',
        '\t': ' ' * tab_size,
        '\n': '<br>'
    }

    return ''.join(
        encode_table.get(c, c) for c in text
    )


def get_environ():
    """Get environment and force utf-8."""

    import os
    env = {}
    env.update(os.environ)

    if sublime.platform() != 'windows':
        shell = env['SHELL']
        p = subprocess.Popen(
            [shell, '-l', '-c', 'echo "#@#@#${PATH}#@#@#"'],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        result = p.communicate()[0].decode('utf8').split('#@#@#')
        if len(result) > 1:
            bin_paths = result[1].split(':')
            if len(bin_paths):
                env['PATH'] = ':'.join(bin_paths)

    env['PYTHONIOENCODING'] = 'utf8'
    env['LANG'] = 'en_US.UTF-8'
    env['LC_CTYPE'] = 'en_US.UTF-8'

    return env


def uml_format(source, language, css_class):
    """Render the UML."""

    plantuml = os.path.join(sublime.packages_path(), 'mdpopup_test', 'plantuml.jar')

    cmd = [
        'java',
        '-splash:no',
        '-jar',
        plantuml,
        '-pipe',
        '-tpng'
        '-charset',
        'UTF-8'
    ]

    with TempFile() as png:
        if sublime.platform() == "windows":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            process = subprocess.Popen(
                cmd,
                startupinfo=startupinfo,
                stdin=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdout=png,
                shell=True,
                env=get_environ()
            )
        else:
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdout=png,
                shell=False,
                env=get_environ()
            )

        process.communicate(input=source.encode('utf-8'))

        png.file.seek(0)

        if process.returncode:
            # Log error and output original source.
            print(png.file.read().decode('utf-8'))
            uml = escape_code(source)
        else:
            png.file.seek(0)
            uml = '<img src="data:image/png;base64,%s">' % base64.b64encode(png.file.read()).decode('ascii')

    return '<div class="%s">%s<div>' % (css_class, uml)
