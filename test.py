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
    # Test Output {: .header}
    ## Headers {: .section}
    # H1
    ## H2
    ### H3
    #### H4
    ##### H5
    ###### H6

    ## Horizontal Ruler {: .section}

    ---

    ## Paragraphs {: .section}
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut 
    labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
    laboris nisi ut aliquip ex ea commodo consequat...

    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut 
    labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco

    ## Inline {: .section}
    Inline **bold**.

    Inline *italic*.

    Inline `code`.

    Inline `#!python import code`

    [mdpopups link](https://github.com/facelessuser/sublime-markdown-popups)

    ## Quotes {: .section}

    > Here is a quote.  
    > About something.

    ## Definition Lists {: .section}

    Apple
    : 1) The round fruit of a tree of the rose family, which typically has thin red or green skin and crisp flesh.

        Many varieties have been developed as dessert or cooking fruit or for making cider.

    : 2) The tree which bears apples.

    ## Table {: .section}

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
    <div class="table-hlines">
      <div class="tr th">
        <span class="td"><span class="tdc">First Row&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></span>
        <span class="td"><span class="tdc">Col2</span></span>
        <span class="td"><span class="tdc">Col3</span></span>
      </div>
      <div class="tr">
        <span class="td"><span class="tdc">This is Second Row&nbsp;</span></span>
        <span class="td"><span class="tdc">Col2</span></span>
        <span class="td"><span class="tdc">Col3</span></span>
      </div>
      <div class="tr">
        <span class="td"><span class="tdc">Third Row&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></span>
        <span class="td"><span class="tdc">Col2</span></span>
        <span class="td"><span class="tdc">Col3</span></span>
      </div>
      <div class="tr">
        <span class="td"><span class="tdc">Even Fourth&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></span>
        <span class="td"><span class="tdc">Col2</span></span>
        <span class="td"><span class="tdc">Col3</span></span>
      </div>
    </div>

    ## Normal Lists {: .section}
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

    ## No Bullet List {: .section}

    <div class="no-bullets" markdown="1">
    - [Lists with block items](#)
        - [Item 1](#)
        - [Item 2](#)
        - [Item 3](#)
    </div>

    ## List Group {: .section}

    <p class="md-list-group" markdown="1">
    <ul class="list-group" markdown="1">
    <li class="list-item">[Normal Item](#)</li>
    <li class="list-item selected">[This is the Selected item](#)</li>
    <li class="list-item fg-bluish">[Info](#)</li>
    <li class="list-item fg-greenish">[Success](#)</li>
    <li class="list-item fg-orangish">[Warning](#)</li>
    <li class="list-item fg-redish">[Error](#)</li>
    </ul>
    </p>

    ## Colors {: .section}

    <div class="content">
    <ul class="no-bullets">
    <li class="fg-foreground">foreground</li>
    <li class="fg-redish">redish</li>
    <li class="fg-orangish">orangish</li>
    <li class="fg-yellowish">yellowish</li>
    <li class="fg-greenish">greenish</li>
    <li class="fg-bluish">bluish</li>
    <li class="fg-purplish">purplish</li>
    <li class="fg-pinkish">pinkish</li>
    </ul>
    </div>

    <div class="content">
    <ul class="fg-background no-bullets">
    <li class="bg-foreground">foreground</li>
    <li class="bg-redish">redish</li>
    <li class="bg-orangish">orangish</li>
    <li class="bg-yellowish">yellowish</li>
    <li class="bg-greenish">greenish</li>
    <li class="bg-bluish">bluish</li>
    <li class="bg-purplish">purplish</li>
    <li class="bg-pinkish">pinkish</li>
    </ul>
    </div>

    ## Blocks {: .section}

        Indented code   block
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

    ## Admonition {: .section}

    !!! panel "Admonition Title"
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut 
        labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
        laboris nisi ut aliquip ex ea commodo consequat...

    !!! panel-success "Success!"
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut 
        labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
        laboris nisi ut aliquip ex ea commodo consequat...

    !!! panel-warning "Warning!"
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut 
        labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco 
        laboris nisi ut aliquip ex ea commodo consequat...

    !!! panel-error "Error!"
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
        labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
        laboris nisi ut aliquip ex ea commodo consequat...

    !!! panel-info "Info"
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
        labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
        laboris nisi ut aliquip ex ea commodo consequat...

    !!! panel-info "Info"
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
        labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
        laboris nisi ut aliquip ex ea commodo consequat...

    ## Color Boxes {: .section}

    <div class="content">
    <span class="box-spacer"><span class="box-wrapper"><span class="box bg-bluish fg-bluish">.</span></span></span>
    <span class="box-spacer"><span class="box-wrapper"><span class="box bg-orangish fg-orangish">.</span></span></span>
    <span class="box-spacer"><span class="box-wrapper"><span class="box bg-greenish fg-greenish">.</span></span></span>
    <span class="box-spacer"><span class="box-wrapper"><span class="box bg-yellowish fg-yellowish">.</span></span></span>
    <span class="box-spacer"><span class="box-wrapper"><span class="box bg-purplish fg-purplish">.</span></span></span>
    </div>

    <div class="content">
    <span class="box-spacer"><span class="box-wrapper1"><span class="box-wrapper2"><span class="box bg-bluish fg-bluish">.</span></span></span></span>
    <span class="box-spacer"><span class="box-wrapper1"><span class="box-wrapper2"><span class="box bg-orangish fg-orangish">.</span></span></span></span>
    <span class="box-spacer"><span class="box-wrapper1"><span class="box-wrapper2"><span class="box bg-greenish fg-greenish">.</span></span></span></span>
    <span class="box-spacer"><span class="box-wrapper1"><span class="box-wrapper2"><span class="box bg-yellowish fg-yellowish">.</span></span></span></span>
    <span class="box-spacer"><span class="box-wrapper1"><span class="box-wrapper2"><span class="box bg-purplish fg-purplish">.</span></span></span></span>
    </div>

    <div class="content rounded-box">
    <span class="box-spacer"><span class="box-wrapper"><span class="box bg-bluish fg-bluish">.</span></span></span>
    <span class="box-spacer"><span class="box-wrapper"><span class="box bg-orangish fg-orangish">.</span></span></span>
    <span class="box-spacer"><span class="box-wrapper"><span class="box bg-greenish fg-greenish">.</span></span></span>
    <span class="box-spacer"><span class="box-wrapper"><span class="box bg-yellowish fg-yellowish">.</span></span></span>
    <span class="box-spacer"><span class="box-wrapper"><span class="box bg-purplish fg-purplish">.</span></span></span>
    </div>

    <div class="content rounded-box">
    <span class="box-spacer"><span class="box-wrapper1"><span class="box-wrapper2"><span class="box bg-bluish fg-bluish">.</span></span></span></span>
    <span class="box-spacer"><span class="box-wrapper1"><span class="box-wrapper2"><span class="box bg-orangish fg-orangish">.</span></span></span></span>
    <span class="box-spacer"><span class="box-wrapper1"><span class="box-wrapper2"><span class="box bg-greenish fg-greenish">.</span></span></span></span>
    <span class="box-spacer"><span class="box-wrapper1"><span class="box-wrapper2"><span class="box bg-yellowish fg-yellowish">.</span></span></span></span>
    <span class="box-spacer"><span class="box-wrapper1"><span class="box-wrapper2"><span class="box bg-purplish fg-purplish">.</span></span></span></span>
    </div>

    ## Buttons {: .section}

    <p class="md-list-group" markdown="1">
    <div class="content" markdown="1">
    [Ok](#){: .btn}&nbsp;[Cancel](#){: .btn}
    </div>
    </p>

    <p class="md-list-group" markdown="1">
    <div class="content" markdown="1">
    [Large](#){: .btn .btn-large}
    </div>
    </p>

    <p class="md-list-group" markdown="1">
    <div class="content" markdown="1">
    [Small](#){: .btn .btn-small}&nbsp;[Small Active](#){: .btn .btn-small .btn-selected}
    </div>
    </p>

    <p class="md-list-group" markdown="1">
    <div class="content" markdown="1">
    [Info](#){: .btn .btn-info}&nbsp;[Error](#){: .btn .btn-error}&nbsp;[Warning](#){: .btn .btn-warning}&nbsp;[Success](#){: .btn .btn-success}
    </div>
    </p>

    <p class="md-list-group" markdown="1">
    <div class="content btn-group" markdown="1">
    <span class="btn-group-spacer">[One](#){: .btn .btn-left}</span>
    <span class="btn-group-spacer">[Two](#){: .btn}</span>
    <span class="btn-group-spacer">[Three](#){: .btn .btn-selected}</span>
    <span class="btn-group-spacer">[Four](#){: .btn .btn-right}</span>
    </div>
    </p>

    <p class="md-list-group" markdown="1">
    <div class="content btn-group" markdown="1">
    <span class="btn-group-spacer">[One](#){: .btn .btn-small .btn-left}</span>
    <span class="btn-group-spacer">[Two](#){: .btn .btn-small .btn-error}</span>
    <span class="btn-group-spacer">[Three](#){: .btn .btn-small}</span>
    <span class="btn-group-spacer">[Four](#){: .btn .btn-small .btn-selected .btn-right}</span>
    </div>
    </p>

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
        max_height=512, max_width=512, nl2br=False
    )


def show_phantom(text):
    """Show the phantom."""
    clear_cache()
    close = '\n[close](#){: .btn .btn-small .btn-info}\n'
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
