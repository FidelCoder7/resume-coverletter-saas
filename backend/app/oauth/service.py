from datetime import UTC, datetime

from authlib.integrations.starlette_client import OAuthError

from app.auth.service import AuthService
from app.oauth.exceptions import (
    GoogleAuthenticationFailed,
    GoogleAuthorizationCancelled,
    GoogleEmailNotAvailable,
    GoogleEmailNotVerified,
)
from app.oauth.google import get_google_client
from app.refresh_tokens.repository import RefreshTokenRepository
from app.users.repository import UserRepository


class GoogleOAuthService:
    """
    Business logic for Google OAuth authentication.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        refresh_repository: RefreshTokenRepository,
    ):
        self.client = get_google_client()
        self.user_repository = user_repository

        self.auth_service = AuthService(
            user_repository,
            refresh_repository,
        )

    async def authorize_redirect(
        self,
        request,
        redirect_uri: str,
    ):
        return await self.client.authorize_redirect(
            request,
            redirect_uri,
        )

    async def authenticate(
        self,
        request,
    ):
        """
        Authenticate or register a Google user,
        then issue the application's JWT tokens.
        """

        error = request.query_params.get("error")

        if error == "access_denied":
            raise GoogleAuthorizationCancelled("Google login was cancelled.")

        try:
            token = await self.client.authorize_access_token(
                request,
            )

        except OAuthError as exc:
            raise GoogleAuthenticationFailed("Google authentication failed.") from exc

        userinfo = token.get("userinfo")

        if userinfo is None:
            raise GoogleAuthenticationFailed("Google did not return user information.")

        google_id = userinfo["sub"]

        email = userinfo.get("email")

        if email is None:
            raise GoogleEmailNotAvailable(
                "Google account did not provide an email address."
            )

        if not userinfo.get("email_verified", False):
            raise GoogleEmailNotVerified("Google email address has not been verified.")

        full_name = userinfo.get(
            "name",
            email.split("@")[0],
        )

        user = self.user_repository.get_by_google_id(
            google_id,
        )

        if user is None:
            user = self.user_repository.get_by_email(
                email,
            )

            if user is None:
                user = self.user_repository.create_google_user(
                    email=email,
                    full_name=full_name,
                    google_id=google_id,
                )

            elif user.google_id is None:
                user.google_id = google_id
                user.is_email_verified = True

                self.user_repository.update(
                    user,
                )

        user.last_login_at = datetime.now(
            UTC,
        )

        self.user_repository.update(
            user,
        )

        access_token, refresh_token = self.auth_service._issue_tokens(
            user,
        )

        return (
            access_token,
            refresh_token,
            user,
        )
