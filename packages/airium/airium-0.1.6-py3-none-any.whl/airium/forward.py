from dataclasses import dataclass
from typing import ClassVar, List, Optional, Type


@dataclass
class Airium:
    base_indent: str = '  '
    current_level: int = 0

    _doc_elements: ClassVar[List[str]]
    _most_recent: ClassVar[Optional['Tag']] = None

    def __post_init__(self):
        self._doc_elements: List[str] = []
        self._most_recent: Optional['Tag'] = None

    def __str__(self) -> str:
        self.flush_()
        return '\n'.join(self._doc_elements)

    def __call__(self, text_str) -> None:
        self.flush_()
        self.append(text_str)

    def __getattr__(self, tag_name: str) -> Type['Tag']:
        return self.get_tag_(tag_name)

    def get_tag_(self, tag_name):
        self.flush_()
        doc = self  # avoid local name aliasing
        if tag_name.strip() in doc.SINGLE_TAGS:

            class SingleTag(Tag):
                """E.g. '<img src="src.png" alt="alt text" />"""

                def __init__(self, *p, _t: str = None, **k):
                    super().__init__(tag_name, doc)
                    self.root.append(f'<{self.tag_name}{self._make_xml_args(*p, **k)} />{_t or ""}')

                def __enter__(self):
                    raise AttributeError(f"The tag: {self.tag_name!r} is a single tag, cannot be used with contexts.")

                def __exit__(self, *_, **__):  # pragma: no cover
                    """Cannot ever run exit since enter raises."""

            SingleTag.__name__ += f'_{tag_name}'  # for debug reasons
            return SingleTag

        else:
            class PairedTag(Tag):
                """E.g. '<div klass='panel'>...</div>"""

                def __init__(self, *p, _t: str = None, **k):
                    super().__init__(tag_name, doc)
                    self.root.append(f'<{self.tag_name}{self._make_xml_args(*p, **k)}>{_t or ""}')
                    self.root._most_recent = self

                def __enter__(self):
                    self.root.current_level += 1
                    self.entered = True

                def __exit__(self, *_, **__):
                    self.root.flush_()
                    self.root.current_level -= 1
                    self.finalize()

                def finalize(self, new_line: bool = True) -> None:
                    self.root.append(f'</{self.tag_name}>', new_line)

            PairedTag.__name__ += f'_{tag_name}'  # for debug reasons
            return PairedTag

    def flush_(self) -> None:
        """Close most recent opened tag.
        In case when we use a contextmanager without entering the context
        i.e.: regular call 'doc.div()` instead of `with doc.div():`
        there could be dangling unclosed tags. So we call the flush_ before each
        new tag or text creation."""
        if self._most_recent and not self._most_recent.entered:
            self._most_recent.finalize(new_line=False)
            self._most_recent = None

    def append(self, element: str, new_line: bool = True) -> None:
        if new_line or not self._doc_elements:
            self._doc_elements.append(f"{self.base_indent * self.current_level}{element}")
        else:
            self._doc_elements[-1] += str(element)

    SINGLE_TAGS = [
        # You may change this list after import by overriding it, like this:
        # Airium.SINGLE_TAGS = ['hr', 'br', 'foo', 'ect']
        # or by extend or append:
        # Airium.SINGLE_TAGS.extend(['foo', 'ect'])
        'input', 'hr', 'br', 'img', 'area', 'link',
        'col', 'meta', 'base', 'param', 'wbr',
        'keygen', 'source', 'track', 'embed',
    ]


@dataclass
class Tag:
    tag_name: str
    root: Airium

    entered: ClassVar[bool] = None
    children_count: ClassVar[int] = 0

    def __post_init__(self):
        self.entered = None
        self.children_count = 0

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.tag_name!r})"

    def finalize(self, new_line: bool = True) -> None:
        """Intentionally does nothing"""

    @classmethod
    def _make_xml_args(cls, *p, **k) -> str:
        ret = ''
        for positional in p:
            ret += f' {positional}'

        for key, value in k.items():
            key = str(key)  # sanity reasons
            value = str(value)  # sanity reasons
            normalized_key = cls.ATTRIBUTE_NAME_SUBSTITUTES.get(key, key)
            normalized_value = cls.ATTRIBUTE_VALUE_SUBSTITUTES.get(value, value)
            normalized_value = cls.escape_quotes(normalized_value)
            ret += ' {}="{}"'.format(normalized_key, normalized_value)

        return ret

    @staticmethod
    def escape_quotes(str_value: str) -> str:
        return str_value.replace('"', '&quot;')

    ATTRIBUTE_NAME_SUBSTITUTES = {
        # html tags colliding with python keywords
        'klass': 'class',
        'Class': 'class',
        'class_': 'class',
        'async_': 'async',
        'Async': 'async',
        'for_': 'for',
        'For': 'for',
        'In': 'in',
        'in_': 'in',

        # from XML
        'xmlns_xlink': 'xmlns:xlink',

        # from SVG ns
        'fill_opacity': 'fill-opacity',
        'stroke_width': 'stroke-width',
        'stroke_dasharray': ' stroke-dasharray',
        'stroke_opacity': 'stroke-opacity',
        'stroke_dashoffset': 'stroke-dashoffset',
        'stroke_linejoin': 'stroke-linejoin',
        'stroke_linecap': 'stroke-linecap',
        'stroke_miterlimit': 'stroke-miterlimit',

        # you may add translations to this dict after importing Tag class:
        # Tag.ATTRIBUTE_NAME_SUBSTITUTES.update({
        #   # e.g.
        #   'clas': 'class',
        #   'data_img_url_small': 'data-img_url_small',
        # })
    }

    ATTRIBUTE_VALUE_SUBSTITUTES = {
        'True': 'true',
        'False': 'false',
        'None': 'null',
    }
