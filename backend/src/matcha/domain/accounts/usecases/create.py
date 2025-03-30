from matcha.domain.accounts.commands import CreateAccount
from matcha.domain.accounts.events import AccountCreated
from matcha.domain.accounts.exceptions import EmailAlreadyExists, PasswordsMismatch
from matcha.domain.accounts.factories import AccountFactory
from matcha.domain.accounts.models import Account
from matcha.domain.uow import MatchaUnitOfWork
from matcha.infrastructure.framework.usecase import UseCase


class CreateAccountUseCase(UseCase[MatchaUnitOfWork]):
    async def execute(self, cmd: CreateAccount) -> Account:
        self.log.info("create account with email: %s", cmd.email)

        if cmd.confirm_password != cmd.password:
            self.log.error("passwords mismatch for email: %s", cmd.email)
            raise PasswordsMismatch()

        if await self.uow.accounts.get_by_email(cmd.email):
            self.log.error("email already exists: %s", cmd.email)
            raise EmailAlreadyExists()

        account = AccountFactory(self.uow).new(cmd)

        await self.uow.accounts.persist(account)
        await self.uow.msg_bus.add_to_queue(AccountCreated(account_id=account.id))

        return account
