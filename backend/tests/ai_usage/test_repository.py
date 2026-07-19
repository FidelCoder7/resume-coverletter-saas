from datetime import UTC, datetime, timedelta
from decimal import Decimal

from app.ai_usage.models import AIUsage
from app.ai_usage.repository import AIUsageRepository
from app.common.constants import (
    AIFeature,
    AIRequestStatus,
)
from tests.factories.cover_letter_factory import create_cover_letter
from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import create_user


def create_usage(
    db,
    *,
    user_id,
    resume_id=None,
    cover_letter_id=None,
    feature=AIFeature.RESUME_GENERATION,
    total_tokens=100,
    estimated_cost=Decimal("0.010000"),
    status=AIRequestStatus.SUCCESS,
    created_at=None,
):
    """
    Persist an AIUsage record for repository testing.
    """

    usage = AIUsage(
        user_id=user_id,
        resume_id=resume_id,
        cover_letter_id=cover_letter_id,
        feature=feature,
        provider="openai",
        model="gpt-4.1-mini",
        prompt_version="v1",
        prompt_tokens=40,
        completion_tokens=60,
        total_tokens=total_tokens,
        estimated_cost=estimated_cost,
        latency_ms=250,
        status=status,
        error_message=None,
    )

    if created_at is not None:
        usage.created_at = created_at

    db.add(usage)
    db.commit()
    db.refresh(usage)

    return usage


def test_create_persists_usage_record(db_session):
    repository = AIUsageRepository(db_session)

    user = create_user(db_session)
    resume = create_resume(
        db_session,
        user_id=user.id,
    )
    cover_letter = create_cover_letter(
        db_session,
        resume_id=resume.id,
    )

    usage = AIUsage(
        user_id=user.id,
        resume_id=resume.id,
        cover_letter_id=cover_letter.id,
        feature=AIFeature.RESUME_GENERATION,
        provider="openai",
        model="gpt-4.1-mini",
        prompt_version="v1",
        prompt_tokens=100,
        completion_tokens=50,
        total_tokens=150,
        estimated_cost=Decimal("0.015000"),
        latency_ms=420,
        status=AIRequestStatus.SUCCESS,
        error_message=None,
    )

    created = repository.create(usage)

    assert created.id is not None
    assert created.user_id == user.id
    assert created.resume_id == resume.id
    assert created.cover_letter_id == cover_letter.id
    assert created.total_tokens == 150
    assert created.estimated_cost == Decimal("0.015000")
    assert created.status is AIRequestStatus.SUCCESS


def test_get_by_id_returns_usage(db_session):
    repository = AIUsageRepository(db_session)

    user = create_user(db_session)

    usage = create_usage(
        db_session,
        user_id=user.id,
    )

    found = repository.get_by_id(
        usage.id,
    )

    assert found is not None
    assert found.id == usage.id
    assert found.user_id == user.id


def test_list_by_user_returns_newest_first(db_session):
    repository = AIUsageRepository(db_session)

    user = create_user(db_session)

    older = create_usage(
        db_session,
        user_id=user.id,
        created_at=datetime.now(UTC) - timedelta(days=2),
    )

    newer = create_usage(
        db_session,
        user_id=user.id,
        created_at=datetime.now(UTC),
    )

    history = repository.list_by_user(
        user.id,
    )

    assert len(history) == 2
    assert history[0].id == newer.id
    assert history[1].id == older.id


def test_list_by_resume_returns_matching_records(db_session):
    repository = AIUsageRepository(db_session)

    user = create_user(db_session)

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    other_resume = create_resume(
        db_session,
        user_id=user.id,
        title="Another Resume",
    )

    matching = create_usage(
        db_session,
        user_id=user.id,
        resume_id=resume.id,
    )

    create_usage(
        db_session,
        user_id=user.id,
        resume_id=other_resume.id,
    )

    results = repository.list_by_resume(
        resume.id,
    )

    assert len(results) == 1
    assert results[0].id == matching.id
    assert results[0].resume_id == resume.id


def test_list_by_cover_letter_returns_matching_records(db_session):
    repository = AIUsageRepository(db_session)

    user = create_user(db_session)

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    other_resume = create_resume(
        db_session,
        user_id=user.id,
        title="Other Resume",
    )

    cover_letter = create_cover_letter(
        db_session,
        resume_id=resume.id,
    )

    other_cover_letter = create_cover_letter(
        db_session,
        resume_id=other_resume.id,
        title="Other Cover Letter",
    )

    matching = create_usage(
        db_session,
        user_id=user.id,
        resume_id=resume.id,
        cover_letter_id=cover_letter.id,
    )

    create_usage(
        db_session,
        user_id=user.id,
        resume_id=other_resume.id,
        cover_letter_id=other_cover_letter.id,
    )

    results = repository.list_by_cover_letter(
        cover_letter.id,
    )

    assert len(results) == 1
    assert results[0].id == matching.id
    assert results[0].cover_letter_id == cover_letter.id


def test_count_by_user_and_period(db_session):
    repository = AIUsageRepository(db_session)

    user = create_user(db_session)
    other_user = create_user(db_session)

    now = datetime.now(UTC)

    create_usage(
        db_session,
        user_id=user.id,
        created_at=now - timedelta(days=2),
    )

    create_usage(
        db_session,
        user_id=user.id,
        created_at=now - timedelta(hours=12),
    )

    create_usage(
        db_session,
        user_id=other_user.id,
        created_at=now - timedelta(hours=6),
    )

    count = repository.count_by_user_and_period(
        user_id=user.id,
        start_date=now - timedelta(days=1),
        end_date=now + timedelta(minutes=1),
    )

    assert count == 1


def test_sum_tokens_by_user_and_period(db_session):
    repository = AIUsageRepository(db_session)

    user = create_user(db_session)

    now = datetime.now(UTC)

    create_usage(
        db_session,
        user_id=user.id,
        total_tokens=120,
        created_at=now - timedelta(hours=8),
    )

    create_usage(
        db_session,
        user_id=user.id,
        total_tokens=80,
        created_at=now - timedelta(hours=4),
    )

    create_usage(
        db_session,
        user_id=user.id,
        total_tokens=500,
        created_at=now - timedelta(days=7),
    )

    total = repository.sum_tokens_by_user_and_period(
        user_id=user.id,
        start_date=now - timedelta(days=1),
        end_date=now + timedelta(minutes=1),
    )

    assert total == 200


def test_sum_cost_by_user_and_period(db_session):
    repository = AIUsageRepository(db_session)

    user = create_user(db_session)

    now = datetime.now(UTC)

    create_usage(
        db_session,
        user_id=user.id,
        estimated_cost=Decimal("0.012500"),
        created_at=now - timedelta(hours=8),
    )

    create_usage(
        db_session,
        user_id=user.id,
        estimated_cost=Decimal("0.007500"),
        created_at=now - timedelta(hours=2),
    )

    create_usage(
        db_session,
        user_id=user.id,
        estimated_cost=Decimal("0.500000"),
        created_at=now - timedelta(days=10),
    )

    total = repository.sum_cost_by_user_and_period(
        user_id=user.id,
        start_date=now - timedelta(days=1),
        end_date=now + timedelta(minutes=1),
    )

    assert total == Decimal("0.020000")


def test_analytics_return_zero_when_no_records_exist(db_session):
    repository = AIUsageRepository(db_session)

    user = create_user(db_session)

    now = datetime.now(UTC)

    assert (
        repository.count_by_user_and_period(
            user_id=user.id,
            start_date=now - timedelta(days=1),
            end_date=now,
        )
        == 0
    )

    assert (
        repository.sum_tokens_by_user_and_period(
            user_id=user.id,
            start_date=now - timedelta(days=1),
            end_date=now,
        )
        == 0
    )

    assert repository.sum_cost_by_user_and_period(
        user_id=user.id,
        start_date=now - timedelta(days=1),
        end_date=now,
    ) == Decimal("0")
