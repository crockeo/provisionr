from base64 import b64encode, b64decode

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.util import b64decode
from provisionr.models import Person, Team


async def get_teams(
    session: AsyncSession,
    *,
    continuation_token: str | None = None,
    page_size: int | None = None,
) -> tuple[list[Team], str | None]:
    query = select(Team).order_by(Team.id)
    if continuation_token:
        prev_max_id = int(b64decode(continuation_token).decode())
        query = query.where(Team.id > prev_max_id)
    if page_size:
        # `page_size + 1` because we want to check if there's a subsequent continuation_token.
        query = query.limit(page_size + 1)

    teams = list(await session.scalars(query))

    next_continuation_token = None
    if page_size and len(teams) > page_size:
        teams = teams[:page_size]
        last_id = teams[-1].id
        next_continuation_token = b64encode(str(last_id).encode()).decode()

    return teams, next_continuation_token


async def get_team(session: AsyncSession, team_slug: str) -> Team:
    team = await session.scalar(select(Team).where(Team.slug == team_slug).options(joinedload(Team.members)))
    if team is None:
        raise HTTPException(404, f"No such team: {team_slug}")
    return team
