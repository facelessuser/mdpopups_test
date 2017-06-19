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
from textwrap import dedent
import sys
this = sys.modules[__name__]

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
                "base_repo_url": "https://github.com/facelessuser/sublime-markdown-popups"
            }
        },
        "pymdownx.extrarawhtml",
        "pymdownx.keys",
        {"pymdownx.escapeall": {"hardbreak": True, "nbsp": True}},
        # Sublime doesn't support superscript, so no ordinal numbers
        {"pymdownx.smartsymbols": {"ordinal_numbers": False}}
    ]
}

md_text = dedent(
    '''\
    # Test Output
    ## Headers

    # H1
    ## H2
    ### H3
    #### H4
    ##### H5
    ###### H6

    ## Horizontal Ruler

    ---

    ## Paragraphs

    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut 
    labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
    laboris nisi ut aliquip ex ea commodo consequat...

    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut 
    labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco

    ## Inline

    ++ctrl+alt+del++

    Inline **bold**.

    Inline *italic*.

    Inline `code`.

    Inline `#!python import code`

    [mdpopups link](https://github.com/facelessuser/sublime-markdown-popups)

    https://github.com/facelessuser/sublime-markdown-popups/issues/32

    https://github.com/facelessuser/sublime-markdown-popups/commit/ffa39c2ea6a92752eaaab103e4456bdc39918978

    https://github.com/facelessuser/pymdown-extensions/commit/152e85baa10616054535f4bfeb99345d87741655

    ## SmartSymbols

    `(tm)`: (tm)

    `(c)`: (c)

    `(r)`: (r)

    `c/o`: c/o

    `+/-`: +/-

    `-->`: -->

    `<--`: <--

    `<-->`: <-->

    `=/=`: =/=

    `1/4, etc.`: 1/4, etc.

    ## Quotes

    > Here is a quote.  
    > About something.

    ## Definition Lists

    Apple
    : 1) The round fruit of a tree of the rose family, which typically has thin red or green 
        skin and crisp flesh.

        Many varieties have been developed as dessert or cooking fruit or for making cider.

    : 2) The tree which bears apples.

    ## Normal Lists

    - Fruit
        - Apples
        - Bannanas
        - Oranges
        - Grapes

    1. Meat
        1. Chicken
        2. Pork
        3. Beef

    1. Lists With Paragraphs
        1. item 1

            More from Item 1.

        2. item 2

        3. item 3

    ## Blocks

        Indented code block
        goes here

    ```python
    # Fenced code block
    import awesome
    ```

    - Nested Fence:

        ```python
        # Fenced code block
        import awesome
        ```

    ## Admonition

    !!! panel-other "Normal"
        Testing admontions.

        ```python
        import test

        string = """Lorem  ipsum dolor sit amet, consectetur
        adipiscing elit, sed do eiusmod tempor incididunt ut
        labore et dolore magna aliqua. Ut enim ad minim 
        laboris nisi ut aliquip ex ea commodo consequat..."""
        ```

    !!! panel-success "Success"
        Testing admontions.

        ```python
        import test

        string = """Lorem  ipsum dolor sit amet, consectetur
        adipiscing elit, sed do eiusmod tempor incididunt ut
        labore et dolore magna aliqua. Ut enim ad minim 
        laboris nisi ut aliquip ex ea commodo consequat..."""
        ```

    !!! panel-warning "Warning"
        Testing admontions.

        ```python
        import test

        string = """Lorem  ipsum dolor sit amet, consectetur
        adipiscing elit, sed do eiusmod tempor incididunt ut
        labore et dolore magna aliqua. Ut enim ad minim 
        laboris nisi ut aliquip ex ea commodo consequat..."""
        ```

    !!! panel-error "Error"
        Testing admontions.

        ```python
        import test

        string = """Lorem  ipsum dolor sit amet, consectetur
        adipiscing elit, sed do eiusmod tempor incididunt ut
        labore et dolore magna aliqua. Ut enim ad minim 
        laboris nisi ut aliquip ex ea commodo consequat..."""
        ```

    !!! panel-info "Info"
        Testing admontions.

        ```python
        import test

        string = """Lorem  ipsum dolor sit amet, consectetur
        adipiscing elit, sed do eiusmod tempor incididunt ut
        labore et dolore magna aliqua. Ut enim ad minim 
        laboris nisi ut aliquip ex ea commodo consequat..."""
        ```
    '''
)


def active_view():
    """Get active view."""
    return sublime.active_window().active_view()


def clear_cache():
    """Clear CSS cache."""
    mdpopups.clear_cache()


def menu():
    """Show menu allowing you to select a test."""
    tests = (
        "Popup Format",
        "Phantom Format"
    )

    def run_test(value):
        """Run the test."""
        if value >= 0:
            test = '_'.join(tests[value].lower().split(' '))
            getattr(this, 'mdpopups_%s_test' % test)()

    window = active_view().window()
    window.show_quick_panel(tests, run_test)


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


def mdpopups_popup_format_test():
    """Test popup."""

    show_popup(mdpopups.format_frontmatter(frontmatter) + md_text)


def mdpopups_phantom_format_test():
    """Test phantom."""

    show_phantom(mdpopups.format_frontmatter(frontmatter) + md_text)


class MdpopupsTestCommand(sublime_plugin.TextCommand):
    """Test command."""

    def run(self, edit):
        """Run command."""

        menu()
