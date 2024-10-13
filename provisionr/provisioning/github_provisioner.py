from dataclasses import dataclass
from typing import override

from provisionr.models import Team
from provisionr.provisioning import Provisioner
from provisionr.provisioning import ProvisioningOperation

@dataclass
class GithubProvisionerState:
    teams: list["GithubTeam"]

@dataclass
class GithubTeam:
    slug: str
    members: list["GithubTeamMember"]


@dataclass
class GithubTeamMember:
    is_maintainer: bool
    username: str


class GithubProvisioner(Provisioner[GithubProvisionerState]):
    @override
    def get_target_state(self, teams: list[Team]) -> GithubProvisionerState:
        return GithubProvisionerState(
            teams=[
                GithubTeam(
                    slug=team.slug,
                    members=[
                        GithubTeamMember(
                            is_maintainer=member.maintainer,
                            username=member.username
                        )
                        for member in team.members
                    ],
                )
                for team in teams
            ],
        )

    @override
    async def get_required_operations(self, team: Team, target_state: GithubProvisionerState) -> list[ProvisioningOperation]:
        # TODO: set up GitHub API, check what we have vs. what we don't have, and then reconcile
        raise NotImplementedError
