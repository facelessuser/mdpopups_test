# MdPopups Test Plugin

A plugin designed to test MdPopups.

![img](tooltips_test.png)

## Usage

- Run command `Mdpopups: Test` and choose either popup, phantom, HTML Sheet, or HTML output. This demonstrates basic
  formatting. HTML Sheet is ST4 specific.

- Run command `Mdpopups: Test Current View` and choose either popup, phantom, HTML Sheet, or HTML output. This will
  parse the current view as the Markdown source.

- If you'd like to start with a view with the default frontmatter, run `Mdpopups: Create Test File`.

## Settings

Currently, the only available settings are for controlling which syntax is used for either the test file's Markdown
syntax or the HTML output result's syntax.

```
{
    // Syntax to use for new test file
    "markdown_syntax": "Packages/Markdown/Markdown.sublime-syntax",

    // Syntax to use for HTML output
    "html_syntax": "Packages/HTML/HTML.sublime-syntax"
}
```
