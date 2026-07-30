from fastapi import Depends
from sqlalchemy.orm import Session

from app.billing.providers.base import PaymentProvider
from app.billing.providers.pesapal.provider import PesaPalProvider
from app.billing.repository import PaymentTransactionRepository
from app.billing.service import PaymentTransactionService
from app.database.session import get_db


def get_payment_transaction_repository(
    db: Session = Depends(get_db),
) -> PaymentTransactionRepository:
    """
    Provide a payment transaction repository.
    """

    return PaymentTransactionRepository(
        db,
    )


def get_payment_provider() -> PaymentProvider:
    """
    Provide the configured payment provider.

    The billing service depends on the provider abstraction rather
    than directly depending on a concrete provider implementation.
    """

    return PesaPalProvider()


def get_payment_transaction_service(
    repository: PaymentTransactionRepository = Depends(
        get_payment_transaction_repository,
    ),
    provider: PaymentProvider = Depends(
        get_payment_provider,
    ),
) -> PaymentTransactionService:
    """
    Provide a payment transaction service with its dependencies.
    """

    return PaymentTransactionService(
        repository=repository,
        provider=provider,
    )
