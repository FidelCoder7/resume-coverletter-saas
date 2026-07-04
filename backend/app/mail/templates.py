from app.core.config import settings


def verification_email(
    *,
    full_name: str,
    token: str,
) -> tuple[str, str]:
    """
    Build the verification email.

    Returns:
        (subject, html)
    """

    verify_url = f"{settings.FRONTEND_URL}" f"/verify-email?token={token}"

    subject = "Verify your email"

    html = f"""
    <html>
      <body
        style="
          font-family: Arial, sans-serif;
          max-width: 600px;
          margin: auto;
        "
      >
        <h2>Welcome, {full_name}!</h2>

        <p>
          Thank you for creating an account.
        </p>

        <p>
          Click the link below to verify your email:
        </p>

        <p>
          <a href="{verify_url}">
            Verify Email
          </a>
        </p>

        <p>
          This link expires in
          {settings.EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS}
          hours.
        </p>

        <hr>

        <small>
          If you didn't create this account,
          you can safely ignore this email.
        </small>
      </body>
    </html>
    """

    return subject, html
