
from dataclasses import dataclass


@dataclass
class Study:
    title: str
    compensation: str
    short_description: str
    link: str

    @property
    def gives_vph(self) -> bool:
        return "vph" in self.compensation.lower()

    def __str__(self) -> str:
        return f"{self.title}\n\t{self.compensation}\n\t{self.short_description}\n\t{self.link}"
    


@dataclass
class VPNType:
    name: str
    long_name: str
    required_amount: int

class VPN_MP(VPNType):
    name: str = "MP"
    long_name: str = "Medienpsychologie"
    required_amount: int = 4

class VPN_KPNM(VPNType):
    name: str = "KPNM"
    long_name: str = "Kommunikationspsychologie und Neue Medien"
    required_amount: int = 4

class VPN_MWK(VPNType):
    name: str = "MWK"
    long_name: str = "Medien- und Wirtschaftskommunikation"
    required_amount: int = 4

class VPN_MI(VPNType):
    name: str = "MI"
    long_name: str = "Medieninformatik"
    required_amount: int = 4

class VPN_HCI(VPNType):
    name: str = "HCI"
    long_name: str = "Human-Computer Interaction"
    required_amount: int = 4

class VPN_PsyErgo(VPNType):
    name: str = "PsyErgo"
    long_name: str = "Psychologische Ergonomie"
    required_amount: int = 4

class VPN_MTS(VPNType):
    name: str = "MTS"
    long_name: str = "Mensch-Technik-Systeme"
    required_amount: int = 2

class VPN_FREE(VPNType):
    name: str = "FREE"
    long_name: str = "Freier Bereich"
    required_amount: int = 4