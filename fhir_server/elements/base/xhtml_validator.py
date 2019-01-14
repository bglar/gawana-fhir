import re
from html.parser import HTMLParser


class XHTMLValidator(HTMLParser):
    def handle_starttag(self, tag, attrs):
        errors = []
        valid_tags = [
            "a",
            "abbr",
            "acronym",
            "b",
            "big",
            "blockquote",
            "br",
            "caption",
            "cite",
            "code",
            "col",
            "colgroup",
            "dd",
            "dfn",
            "div",
            "dl",
            "dt",
            "em",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "hr",
            "i",
            "img",
            "li",
            "ol",
            "p",
            "pre",
            "q",
            "samp",
            "small",
            "span",
            "strong",
            "table",
            "tbody",
            "td",
            "tfoot",
            "th",
            "thead",
            "tr",
            "tt",
            "ul",
            "var",
            "img",
            "div",
        ]
        valid_attrs = [
            "abbr",
            "accesskey",
            "align",
            "alt",
            "axis",
            "bgcolor",
            "border",
            "cellhalign",
            "cellpadding",
            "cellspacing",
            "cellvalign",
            "char",
            "charoff",
            "charset",
            "cite",
            "class",
            "colspan",
            "compact",
            "coords",
            "dir",
            "frame",
            "headers",
            "height",
            "href",
            "hreflang",
            "hspace",
            "id",
            "lang",
            "longdesc",
            "name",
            "nowrap",
            "rel",
            "rev",
            "rowspan",
            "rules",
            "scope",
            "shape",
            "span",
            "src",
            "start",
            "style",
            "summary",
            "tabindex",
            "title",
            "type",
            "valign",
            "value",
            "vspace",
            "width",
            "img",
            "xmlns",
        ]
        for attr in attrs:
            if not (attr[0] in valid_attrs):
                errors.append(
                    "The attribute %s is not valid in chapters 7-11 (except "
                    "section 4 of chapter 9) and 15 of the HTML 4.0 standard" % attr[0]
                )

        if not (tag in valid_tags):
            errors.append(
                "The tag %s is not valid in chapters 7-11 (except section "
                "4 of chapter 9) and 15 of the HTML 4.0 standard" % tag
            )

        if len(errors) > 0:
            raise TypeError(errors)

    def handle_data(self, data):
        # check that narrative content has some whitespaces i.e not blank
        pattern = re.compile("^\s*$")
        if re.search(pattern, data):
            raise TypeError("narrative content must not be an empty string")


xhtml_validator = XHTMLValidator()
