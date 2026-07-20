from app.ats.scoring import ATSScoringService


def test_tokenize_normalizes_case():
    tokens = ATSScoringService.tokenize(
        "Python FASTAPI Docker",
    )

    assert tokens == [
        "python",
        "fastapi",
        "docker",
    ]


def test_tokenize_ignores_punctuation():
    tokens = ATSScoringService.tokenize(
        "Python, FastAPI. Docker! PostgreSQL?",
    )

    assert tokens == [
        "python",
        "fastapi",
        "docker",
        "postgresql",
    ]


def test_extract_keywords_returns_sorted_unique_keywords():
    keywords = ATSScoringService.extract_keywords(
        ("Python FastAPI Python Docker " "PostgreSQL Docker"),
    )

    assert keywords == [
        "docker",
        "fastapi",
        "postgresql",
        "python",
    ]


def test_score_returns_full_match():
    score, matched, missing = ATSScoringService.score(
        resume=("Python FastAPI Docker PostgreSQL"),
        job_description=("Python FastAPI Docker PostgreSQL"),
    )

    assert score == 100

    assert matched == [
        "docker",
        "fastapi",
        "postgresql",
        "python",
    ]

    assert missing == []


def test_score_returns_partial_match():
    score, matched, missing = ATSScoringService.score(
        resume=("Python FastAPI Docker"),
        job_description=("Python FastAPI Docker Kubernetes AWS"),
    )

    assert score == 60

    assert matched == [
        "docker",
        "fastapi",
        "python",
    ]

    assert missing == [
        "aws",
        "kubernetes",
    ]


def test_score_returns_zero_when_no_keywords_match():
    score, matched, missing = ATSScoringService.score(
        resume=("Java Spring Hibernate"),
        job_description=("Python FastAPI Docker"),
    )

    assert score == 0

    assert matched == []

    assert missing == [
        "docker",
        "fastapi",
        "python",
    ]


def test_score_returns_100_when_job_description_is_empty():
    score, matched, missing = ATSScoringService.score(
        resume="Python FastAPI",
        job_description="",
    )

    assert score == 100
    assert matched == []
    assert missing == []


def test_score_ignores_duplicate_keywords():
    score, matched, missing = ATSScoringService.score(
        resume=("Python Python Python " "FastAPI FastAPI Docker"),
        job_description=("Python Docker FastAPI"),
    )

    assert score == 100

    assert matched == [
        "docker",
        "fastapi",
        "python",
    ]

    assert missing == []


def test_score_is_case_insensitive():
    score, matched, missing = ATSScoringService.score(
        resume="PYTHON fastapi DOCKER",
        job_description="python FastAPI docker",
    )

    assert score == 100

    assert matched == [
        "docker",
        "fastapi",
        "python",
    ]

    assert missing == []


def test_score_handles_special_characters():
    score, matched, missing = ATSScoringService.score(
        resume=("C++ C# .NET Python"),
        job_description=("C++ Python Rust"),
    )

    # The current tokenizer treats only standard word tokens.
    # Language names containing punctuation (C++, C#, .NET, Node.js, etc.)
    # are intentionally not handled in v1.6.0.

    assert score == 50

    assert matched == [
        "python",
    ]

    assert missing == [
        "rust",
    ]


def test_extract_keywords_from_empty_text():
    keywords = ATSScoringService.extract_keywords(
        "",
    )

    assert keywords == []


def test_tokenize_empty_text():
    tokens = ATSScoringService.tokenize(
        "",
    )

    assert tokens == []
