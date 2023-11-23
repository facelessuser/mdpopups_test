# -*- coding: UTF-8 -*-
"""
Mdpopups manual test module.
"""
import sublime
import sublime_plugin
import mdpopups
import sys
import re
this = sys.modules[__name__]

END_YAML = re.compile(r'\.{3}\r?\n\Z')

SETTINGS = "Packages/mdpopups_test/mdpopups_test.sublime-settings"
HTML_SHEET_SUPPORT = int(sublime.version()) >= 4074

TEST_MD = "Packages/mdpopups_test/test.md"
CLOSE_BUTTON = '\n\n<p>\n<a href="#" class="btn btn-small btn-info">close</a>\n</p>'

FRONTMATTER = {
    "allow_code_wrap": False,
    "markdown_extensions": [
        "markdown.extensions.admonition",
        "markdown.extensions.attr_list",
        "markdown.extensions.def_list",
        # Smart quotes always have corner cases that annoy me, so don't bother with them.
        {"markdown.extensions.smarty": {"smart_quotes": False}},
        "pymdownx.betterem",
        {
            "pymdownx.magiclink": {
                "repo_url_shortener": True,
                "repo": "sublime-markdown-popups",
                "user": "facelessuser"
            }
        },
        "markdown.extensions.md_in_html",
        "pymdownx.keys",
        {"pymdownx.escapeall": {"hardbreak": True, "nbsp": True}},
        # Sublime doesn't support superscript, so no ordinal numbers
        {"pymdownx.smartsymbols": {"ordinal_numbers": False}}
    ]
}


def active_view():
    """Get active view."""
    return sublime.active_window().active_view()


def clear_cache():
    """Clear CSS cache."""
    mdpopups.clear_cache()


def menu(fmatter, md_file):
    """Show menu allowing you to select a test."""
    tests = [
        "Popup Format",
        "Phantom Format"
    ]

    if HTML_SHEET_SUPPORT:
        tests.append("Sheet Format")

    tests.append('HTML Output')

    tests = tuple(tests)

    def run_test(value, fm, md):
        """Run the test."""
        if value >= 0:
            test = '_'.join(tests[value].lower().split(' '))
            getattr(this, 'mdpopups_%s_test' % test)(fm, md)

    window = active_view().window()
    window.show_quick_panel(tests, lambda v, fm=fmatter, md=md_file: run_test(v, fm, md))


def on_close_popup(href):
    """Close the popup."""

    if href == '#':
        view = active_view()
        mdpopups.hide_popup(view)


def on_close_phantom(href):
    """Close all phantoms."""

    if href == '#':
        view = active_view()
        mdpopups.erase_phantoms(view, 'mdpopups_test')


def show_popup(text):
    """Show the popup."""
    clear_cache()
    view = active_view()
    region = view.visible_region()
    mdpopups.show_popup(
        active_view(), text + CLOSE_BUTTON, location=region.a, on_navigate=on_close_popup,
        max_height=650, max_width=600, wrapper_class='mdpopups-test',
        css='div.mdpopups-test { padding: 0.5rem; }'
    )


def show_source(fm, text):
    """Show content."""

    clear_cache()
    view = active_view()
    region = view.visible_region()
    html = mdpopups.md2html(active_view(), fm + text)

    view = active_view().window().new_file()
    MdpopupsInsertPayloadCommand.syntax = sublime.load_settings(SETTINGS).get(
        'html_syntax', "Packages/HTML/HTML.sublime-syntax"
    )
    MdpopupsInsertPayloadCommand.payload = html
    MdpopupsInsertPayloadCommand.buffer_name = "MdPopups Test Results.html"
    view.run_command('mdpopups_insert_payload')


def show_phantom(text):
    """Show the phantom."""
    clear_cache()
    view = active_view()
    region = view.visible_region()
    mdpopups.add_phantom(
        active_view(), 'mdpopups_test', region, text + CLOSE_BUTTON, 2,
        on_navigate=on_close_phantom, wrapper_class='mdpopups-test'
    )


def mdpopups_popup_format_test(fm, md):
    """Test popup."""

    if md is None:
        view = active_view()
        content = view.substr(sublime.Region(0, view.size()))
        frontmatter = ''
    else:
        content = sublime.load_resource(md)
        frontmatter = mdpopups.format_frontmatter(fm)

    show_popup(frontmatter + content)


def mdpopups_phantom_format_test(fm, md):
    """Test phantom."""

    if md is None:
        view = active_view()
        content = view.substr(sublime.Region(0, view.size()))
        frontmatter = ''
    else:
        content = sublime.load_resource(md)
        frontmatter = mdpopups.format_frontmatter(fm)

    show_phantom(frontmatter + content)


def mdpopups_html_output_test(fm, md):
    """Test HTML output."""

    if md is None:
        view = active_view()
        content = view.substr(sublime.Region(0, view.size()))
        frontmatter = ''
    else:
        content = sublime.load_resource(md)
        frontmatter = mdpopups.format_frontmatter(fm)

    show_source(frontmatter, content)


class MdpopupsTestCommand(sublime_plugin.TextCommand):
    """Test command."""

    def run(self, edit, view=False):
        """Run command."""

        menu(
            FRONTMATTER if not view else None,
            TEST_MD if not view else None
        )


class MdpopupsTestUmlCommand(sublime_plugin.TextCommand):
    """Test UML command."""

    def run(self, edit):
        """Run command."""

        menu(
            FRONTMATTER_UML,
            TEST_UML_MD
        )


class MdpopupsInsertPayloadCommand(sublime_plugin.TextCommand):
    """Load default frontmatter."""

    payload = ""
    syntax = ""
    buffer_name = ""

    def run(self, edit):
        """Run command."""

        self.view.insert(edit, 0, MdpopupsInsertPayloadCommand.payload)
        self.view.set_syntax_file(MdpopupsInsertPayloadCommand.syntax)
        self.view.set_name(MdpopupsInsertPayloadCommand.buffer_name)


class MdpopupsCreateDefaultViewCommand(sublime_plugin.WindowCommand):
    """Create default view."""

    def run(self):
        """"Run command."""

        view = self.window.new_file()
        MdpopupsInsertPayloadCommand.syntax = sublime.load_settings(SETTINGS).get(
            'markdown_syntax', "Packages/Markdown/Markdown.sublime-syntax"
        )
        MdpopupsInsertPayloadCommand.payload = END_YAML.sub('---\n', mdpopups.format_frontmatter(FRONTMATTER))
        MdpopupsInsertPayloadCommand.buffer_name = "MdPopups Test File.md"
        view.run_command('mdpopups_insert_payload')


if HTML_SHEET_SUPPORT:
    def show_sheet(text):
        """Show the sheet."""

        clear_cache()
        close = '\n[close](subl:mdpopups_test_sheet_url){: .btn .btn-small .btn-info}\n'
        window = sublime.active_window()
        mdpopups.new_html_sheet(
            window,
            'Sheet Test',
            text + close,
            wrapper_class='mdpopups-test'
        )

    def mdpopups_sheet_format_test(fm, md):
        """Test sheet."""

        if md is None:
            view = active_view()
            content = view.substr(sublime.Region(0, view.size()))
            frontmatter = ''
        else:
            content = sublime.load_resource(md)
            frontmatter = mdpopups.format_frontmatter(fm)

        show_sheet(frontmatter + content)

    class MdpopupsTestSheetUrlCommand(sublime_plugin.WindowCommand):
        """Url handle command."""

        def run(self, **kwargs):
            """Command?"""

            sheet = None
            if self.window is not None:
                group = self.window.active_group()
                if group is not None:
                    sheet = self.window.active_sheet_in_group(group)
            if sheet is not None:
                self.window.run_command('close_file')
