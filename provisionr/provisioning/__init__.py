from abc import ABCMeta
from abc import abstractmethod
from typing import Awaitable
from typing import Callable
from typing import Generic
from typing import TypeVar

from provisionr.models import Team


ProvisionerState = TypeVar("ProvisionerState")
ProvisioningOperation = Callable[[], Awaitable[None]]


class Provisioner(ABCMeta, Generic[ProvisionerState]):
    @abstractmethod
    def get_target_state(self, teams: list[Team]) -> ProvisionerState:
        """
        Maps from team information to the specific state we want to achieve for this Provisioner.
        """
        pass

    @abstractmethod
    async def get_required_operations(self, team: Team, target_state: ProvisionerState) -> list[ProvisioningOperation]:
        """
        Compares the target_state to the current remote state for this provisioner,
        and produces a list of ProvisioningOperations
        which can be run to make the remote state become the target state.
        """
        pass

    async def execute(self, operations: list[ProvisioningOperation]) -> None:
        """
        Execute a list of operations.
        By default this executes each operation in series,
        and fails on the first error.
        One may want to override this method to implement retries,
        or to continue execution even if a given step fails.
        """
        for operation in operations:
            await operation()
