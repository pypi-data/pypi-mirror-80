from typing import Union, Sequence

from markdownmaker.document import *

# Typing aliases
InlineNodeType = Union[InlineNode, str]
NodeType = Union[Node, str]


class Paragraph(Node):
    def __init__(self, content: NodeType):
        self.content = content

    def __str__(self) -> str:
        return f"{self.content}\n\n"


class HorizontalRule(Node):
    def __str__(self) -> str:
        return "---\n"


class UnorderedList(ListNode):
    def __init__(self, items: Sequence[NodeType]):
        self.items = items

    def __str__(self) -> str:
        out = ""
        for item in self.items:
            if isinstance(item, ListNode):
                Document.indent_level += 1
                out += str(item)
                Document.indent_level -= 1

            else:
                out += f"{'  ' * Document.indent_level}- {item}\n"

        return out + "\n"


class OrderedList(ListNode):
    def __init__(self, items: Sequence[NodeType]):
        self.items = items

    def __str__(self) -> str:
        out = ""
        index = 1
        for item in self.items:
            if isinstance(item, ListNode):
                Document.indent_level += 1
                out += str(item)
                Document.indent_level -= 1

            else:
                out += f"{'  ' * Document.indent_level}{index}. {item}\n"
                # Only increase if we don't have a sublist
                index += 1

        return out + "\n"


class Link(InlineNode):
    def __init__(self, label: str, url: str):
        self.label = label
        self.url = url

    def __str__(self) -> str:
        return f"[{self.label}]({self.url})"


class Image(Node):
    def __init__(self, url: str, alt_text: str = ""):
        self.url = url
        self.alt_text = alt_text

    def __str__(self) -> str:
        return f"\n![{self.alt_text}]({self.url})\n\n"


class InlineImage(InlineNode):
    def __init__(self, url: str, alt_text: str = ""):
        self.url = url
        self.alt_text = alt_text

    def __str__(self) -> str:
        return f"![{self.alt_text}]({self.url})"


class CodeBlock(Node):
    def __init__(self, code: str, language: str = ''):
        super()
        self.code = code
        self.language = language

    def __str__(self) -> str:
        return f"```{self.language}\n{self.code}\n```\n"


class InlineCode(InlineNode):
    def __init__(self, code: str):
        super()
        self.code = code

    def __str__(self) -> str:
        return f"`{self.code}`"


class Quote(Node):
    def __init__(self, content: NodeType):
        super()
        self.content = content

    def __str__(self) -> str:
        return "> " + "\n> ".join(str(self.content).splitlines()) + "\n\n"


class Bold(InlineNode):
    def __init__(self, content: InlineNodeType):
        super()
        self.content = content

    def __str__(self) -> str:
        return f"**{self.content}**"


class Italic(InlineNode):
    def __init__(self, content: InlineNodeType):
        super()
        self.content = content

    def __str__(self) -> str:
        return f"*{self.content}*"


class Header(InlineNode):
    content_str: str

    def __init__(self, content: InlineNodeType):
        super()
        self.content = content

    def __str__(self) -> str:
        return f"{'#' * Document.header_level} {self.content}\n"


class HeaderSubLevel:
    steps: int

    def __init__(self, steps: int = 1):
        self.steps = steps

    def __enter__(self):
        Document.header_level += self.steps

    def __exit__(self, exc_type, exc_val, exc_traceback):
        Document.header_level -= self.steps


class ListSubLevel:
    def __init__(self):
        pass

    def __enter__(self):
        Document.indent_level += 1

    def __exit__(self, exc_type, exc_val, exc_traceback):
        Document.indent_level -= 1
