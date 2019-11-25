# -*- coding: UTF-8 -*-
"""
Mdpopups manual test module.

On load, it will clear the cache and show the test menu.
Subsequent tests can be loaded:

    mdpopups.tests.menu()

If you need to reload the test module.

    import imp
    mdpopups.tests = imp.reload(mdpopups.tests)

If you need to clear the cache.

    mdpopups.tests.clear_cache()
"""
import sublime
import sublime_plugin
import mdpopups
import sys
from . import plantuml
this = sys.modules[__name__]

TEST_MD = "Packages/mdpopup_test/test.md"
TEST_UML_MD = "Packages/mdpopup_test/test_uml.md"

frontmatter = {
    "markdown_extensions": [
        "markdown.extensions.admonition",
        "markdown.extensions.attr_list",
        "markdown.extensions.def_list",
        "markdown.extensions.nl2br",
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
        "pymdownx.extrarawhtml",
        "pymdownx.keys",
        {"pymdownx.escapeall": {"hardbreak": True, "nbsp": True}},
        # Sublime doesn't support superscript, so no ordinal numbers
        {"pymdownx.smartsymbols": {"ordinal_numbers": False}}
    ]
}

frontmatter_uml = {
    "custom_fences": [
        {'name': 'uml', 'class': 'uml', 'format': plantuml.uml_format}
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
    tests = (
        "Popup Format",
        "Phantom Format"
    )

    def run_test(value, fm, md):
        """Run the test."""
        if value >= 0:
            test = '_'.join(tests[value].lower().split(' '))
            getattr(this, 'mdpopups_%s_test' % test)(fm, md)

    window = active_view().window()
    window.show_quick_panel(tests, lambda v, fm=fmatter, md=md_file: run_test(v, fm, md))


def on_close_popup(href):
    """Close the popup."""
    view = active_view()
    mdpopups.hide_popup(view)


def on_close_phantom(href):
    """Close all phantoms."""
    view = active_view()
    mdpopups.erase_phantoms(view, 'mdpopups_test')


def show_popup(text):
    """Show the popup."""
    clear_cache()
    close = '\n[close](#){: .btn .btn-small .btn-info}\n'
    view = active_view()
    region = view.visible_region()
    mdpopups.show_popup(
        active_view(), text + close, location=region.a, on_navigate=on_close_popup,
        max_height=650, max_width=600, wrapper_class='mdpopups-test',
        css='div.mdpopups-test { padding: 0.5rem; }'
    )


def show_phantom(text):
    """Show the phantom."""
    clear_cache()
    close = '\n[close](#){: .btn .btn-small .btn-info}\n'
    view = active_view()
    region = view.visible_region()
    mdpopups.add_phantom(
        active_view(), 'mdpopups_test', region, text + close, 2,
        on_navigate=on_close_phantom, wrapper_class='mdpopups-test'
    )


def mdpopups_popup_format_test(fm, md):
    """Test popup."""

    show_popup(mdpopups.format_frontmatter(fm) + sublime.load_resource(md))


def mdpopups_phantom_format_test(fm, md):
    """Test phantom."""

    show_phantom(mdpopups.format_frontmatter(fm) + sublime.load_resource(md))


class MdpopupsTestCommand(sublime_plugin.TextCommand):
    """Test command."""

    def run(self, edit):
        """Run command."""

        menu(frontmatter, TEST_MD)

class MdpopupsTestUmlCommand(sublime_plugin.TextCommand):
    """Test UML command."""

    def run(self, edit):
        """Run command."""

        menu(frontmatter_uml, TEST_UML_MD)
