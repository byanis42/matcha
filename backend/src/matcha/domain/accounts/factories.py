from datetime import datetime
from pytz import UTC

from matcha.domain.uow import MatchaUnitOfWork
from matcha.domain.accounts.commands import CreateAccount
from matcha.domain.accounts.models import Account
from matcha.domain.accounts.exceptions import PasswordsMismatch


class AccountFactory:
    def __init__(self, uow: MatchaUnitOfWork):
        self.uow = uow

    def new(self, cmd: CreateAccount) -> Account:
        if cmd.confirm_password != cmd.password:
            raise PasswordsMismatch()

        timestamp = datetime.now(UTC)

        account = Account(
            name=cmd.name,
            surname=cmd.surname,
            email=cmd.email,
            password=self.uow.auth.generate_password(cmd.password),
            created_at=timestamp,
            updated_at=timestamp,
        )

        account.set_as_need_activation()

        return account
