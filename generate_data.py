import asyncio
import random

from faker import Faker

from provisionr.models import Person, Team, create_session


def create_person(faker: Faker, team: Team) -> Person:
    profile = faker.profile()
    return Person(
        username=profile["username"],
        name=profile["name"],
        team=team,
        maintainer=random.randint(0, 1) == 1,
    )


def create_team(faker: Faker) -> Team:
    team_name = faker.company()
    team_slug = team_name.lower().replace(" ", "-").replace(",", "")
    
    team = Team(
        slug=team_slug,
        name=team_name,
    )
    team.members = [create_person(faker, team=team) for _ in range(random.randint(5, 20))]
    return team


async def main() -> None:
    faker = Faker()
    async with create_session() as session:
        for _ in range(10):
            team = create_team(faker)
            print(f"Generating {team.name}...")
            session.add(team)
            session.add_all(team.members)


if __name__ == "__main__":
    asyncio.run(main())
