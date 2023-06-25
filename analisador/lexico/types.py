from typing import TypeAlias
from .DFAState import DFAState

TransitionsList: TypeAlias = list[tuple[DFAState, str | set[str], DFAState]]