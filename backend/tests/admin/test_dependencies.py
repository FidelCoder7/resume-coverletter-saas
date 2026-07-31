import pytest

from app.admin.dependencies import require_admin
from app.admin.exceptions import AdminAccessDenied
from app.common.constants import UserRole
from tests.factories.user_factory import make_user


def test_require_admin_allows_admin_user():
    admin = make_user(
        role=UserRole.ADMIN,
    )

    result = require_admin(admin)

    assert result is admin
    assert result.role == UserRole.ADMIN


def test_require_admin_rejects_regular_user():
    user = make_user(
        role=UserRole.USER,
    )

    with pytest.raises(
        AdminAccessDenied,
        match="Administrator access required.",
    ):
        require_admin(user)


@pytest.mark.parametrize(
    "role",
    [
        UserRole.USER,
    ],
)
def test_require_admin_rejects_non_admin_roles(role):
    user = make_user(
        role=role,
    )

    with pytest.raises(AdminAccessDenied):
        require_admin(user)
