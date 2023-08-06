from abc import ABC, abstractmethod
from typing import List, Tuple


class Node(ABC):
    """
    Base class of all nodes. Nodes must override the __str__() method.
    """
    @abstractmethod
    def __str__(self) -> str:
        return ""


class InlineNode(Node, ABC):
    """
    A node which consists only of one line." \
    """
    pass


class ListNode(Node, ABC):
    """
    A node representing a list.
    """
    pass


class Document:
    header_level = 1
    indent_level = 0
    nodes: List[Tuple[int, Node]] = []

    @classmethod
    def add(cls, node: Node) -> None:
        cls.nodes.append((cls.header_level, node))

    @classmethod
    def write(cls) -> str:
        out = ""
        for h_level, node in cls.nodes:
            cls.header_level = h_level
            if isinstance(node, (str, InlineNode)):
                out += f"{node}\n"
            else:
                out += str(node)

        return out
