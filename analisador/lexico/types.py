from typing import TypeAlias
from .DFAState import DFAState

Token: TypeAlias = dict[str, str]
TransitionsList: TypeAlias = list[tuple[DFAState, str | set[str], DFAState]]