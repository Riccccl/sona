
from dataclasses import dataclass


@dataclass
class Study:
    title: str
    compensation: str
    short_description: str
    link : str


    def __str__(self) -> str:
        return f"{self.title}\n\t{self.compensation}\n\t{self.short_description}\n\t{self.link}"