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

format_text = dedent(
    '''
    # Test Output {: .section}
    ## Headers {: .header}
    # H1
    ## H2
    ### H3
    #### H4
    ##### H5
    ###### H6

    ## Horizontal Ruler {: .header}

    ---

    ## Paragraphs {: .header}
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut \
    labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco \
    laboris nisi ut aliquip ex ea commodo consequat...

    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut \
    labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco \

    ## Inline {: .header}
    Inline **bold**.

    Inline *italic*.

    Inline `code`.

    Inline `#!python import code`

    [mdpopups link](https://github.com/facelessuser/sublime-markdown-popups)

    ## Quotes {: .header}

    > Here is a quote.
    > About something.

    ## Definition Lists {: .header}

    Apple {: .header}
    : 1) The round fruit of a tree of the rose family, which typically has thin red or green skin and crisp flesh.

        Many varieties have been developed as dessert or cooking fruit or for making cider.

    : 2) The tree which bears apples.

    ## Table {: .header}

    <div class="table">
      <div class="tr th">
        <span class="td td-first"><span class="tdc">First Row&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></span>
        <span class="td"><span class="tdc">Col2</span></span>
        <span class="td"><span class="tdc">Col3</span></span>
      </div>
      <div class="tr">
        <span class="td td-first"><span class="tdc">This is Second Row&nbsp;</span></span>
        <span class="td"><span class="tdc">Col2</span></span>
        <span class="td"><span class="tdc">Col3</span></span>
      </div>
      <div class="tr">
        <span class="td td-first"><span class="tdc">Third Row&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></span>
        <span class="td"><span class="tdc">Col2</span></span>
        <span class="td"><span class="tdc">Col3</span></span>
      </div>
      <div class="tr">
        <span class="td td-first"><span class="tdc">Even Fourth&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></span>
        <span class="td"><span class="tdc">Col2</span></span>
        <span class="td"><span class="tdc">Col3</span></span>
      </div>
    </div>

    ## Normal Lists {: .header}
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

        2. item 2

        3. item 3

    ## No Bullet List {: .header}

    <div class="no-bullets click-list">
    <ul>
    <li class="selected"><a href="#">Lists with block items</a></li>
    <ul>
    <li><a href="#">item 1</a></li>
    <li class="selected"><a href="#">item 2</a></li>
    <li><a href="#">item 3</a></li>
    </ul>
    </ul>
    </div>

    ## No Bullet Flat List {: .header}

    <div class="no-bullets flat-list click-list">
    <ul>
    <li><a href="#">item 1</a></li>
    <li class="selected"><a href="#">item 2</a></li>
    <li><a href="#">item 3</a></li>
    </ul>
    </div>

    ## Blocks {: .header}

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

    ## Admonition {: .header}

    !!! panel "Admonition Title"
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut \
    labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco \
    laboris nisi ut aliquip ex ea commodo consequat...

    !!! panel-success "Success!"
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut \
    labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco \
    laboris nisi ut aliquip ex ea commodo consequat...

    !!! panel-warning "Warning!"
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut \
    labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco \
    laboris nisi ut aliquip ex ea commodo consequat...

    !!! panel-error "Error!"
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut \
    labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco \
    laboris nisi ut aliquip ex ea commodo consequat...

    !!! panel-info "Info"
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut \
    labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco \
    laboris nisi ut aliquip ex ea commodo consequat...

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
    close = '\n[close](#){: .btn .bg-bluish}\n'
    view = active_view()
    region = view.visible_region()
    mdpopups.show_popup(
        active_view(), text + close, location=region.a, on_navigate=on_close_popup,
        max_height=512, max_width=512
    )


def show_phantom(text):
    """Show the phantom."""
    clear_cache()
    close = '\n[close](#){: .btn .bg-bluish}\n'
    view = active_view()
    region = view.visible_region()
    mdpopups.add_phantom(
        active_view(), 'mdpopups_test', region, text + close, 2, on_navigate=on_close_phantom
    )


def mdpopups_popup_format_test():
    """Test popup."""
    show_popup(format_text)


def mdpopups_phantom_format_test():
    """Test phantom."""
    show_phantom(format_text)


class MdpopupsBootstrapCommand(sublime_plugin.TextCommand):
    """Test command."""

    def run(self, edit):
        """Run command."""

        menu()
