from typing import Union, Literal

from typing_extensions import TypeAlias

from src.base.uow import UnitOfWork
from tests.base.fake_uow import FakeUnitOfWork

TypeUoW: TypeAlias = Union[UnitOfWork, FakeUnitOfWork]
Msg: TypeAlias = dict[Literal['msg'], str]
Tokens: TypeAlias = dict[Literal['access_token', 'refresh_token', 'token_type'], str]
