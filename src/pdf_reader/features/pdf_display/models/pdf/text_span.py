from dataclasses import dataclass

@dataclass
class TextSpan:
    text: str
    bounding_box: tuple
    font_size: float
    font_name: str
    color: int
    flags: int