from typing import Optional

from src.base.aliases import TypeUoW
from src.base.services import exceptions
from src.base.uow import UnitOfWork


def bad_logins(*, ip: Optional[str], uow: TypeUoW = UnitOfWork()) -> None:
    with uow:
        if uow.bad_logins.count(ip_address=ip) >= 3:
            raise exceptions.ManyBadLogins('Many bad login attempts, your ip is temporarily blocked.')
        uow.commit()
