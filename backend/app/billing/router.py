from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.auth.dependencies import get_current_user
from app.billing.dependencies import (
    get_payment_provider,
    get_payment_transaction_service,
)
from app.billing.exceptions import InvalidSubscriptionPaymentPlan
from app.billing.providers.base import PaymentProvider
from app.billing.schemas import (
    PaymentInitiationRequest,
    PaymentInitiationResponse,
    PaymentStatusResponse,
    PaymentTransactionListResponse,
    PaymentTransactionResponse,
)
from app.billing.service import PaymentTransactionService
from app.common.constants import PaymentStatus, SubscriptionPlan
from app.users.models import User

router = APIRouter(
    prefix="/billing",
    tags=["Billing"],
)


@router.post(
    "/payments",
    response_model=PaymentInitiationResponse,
    status_code=status.HTTP_201_CREATED,
)
def initiate_payment(
    payload: PaymentInitiationRequest,
    current_user: User = Depends(
        get_current_user,
    ),
    service: PaymentTransactionService = Depends(
        get_payment_transaction_service,
    ),
    payment_provider: PaymentProvider = Depends(
        get_payment_provider,
    ),
) -> PaymentInitiationResponse:
    """
    Initiate a subscription payment for the authenticated user.

    The application resolves the authoritative subscription price
    server-side. Client-supplied payment amounts and currencies are
    never accepted.

    The payment provider is resolved through dependency injection.
    """

    if payload.subscription_plan == SubscriptionPlan.FREE:
        raise InvalidSubscriptionPaymentPlan(
            "The free subscription plan does not require payment.",
        )
    transaction, redirect_url = service.start_payment(
        user_id=current_user.id,
        subscription_plan=payload.subscription_plan,
        transaction_type=payload.transaction_type,
        customer_email=current_user.email,
        customer_name=current_user.full_name,
        payment_method=payload.payment_method,
    )

    return PaymentInitiationResponse(
        transaction=PaymentTransactionResponse.model_validate(
            transaction,
        ),
        redirect_url=redirect_url,
    )


@router.post(
    "/payments/callback",
    status_code=status.HTTP_200_OK,
)
def payment_callback(
    payload: dict,
    service: PaymentTransactionService = Depends(
        get_payment_transaction_service,
    ),
    payment_provider: PaymentProvider = Depends(
        get_payment_provider,
    ),
) -> dict[str, str]:
    """
    Process a payment provider callback/IPN notification.

    This endpoint is intentionally unauthenticated because it is
    called server-to-server by the payment provider.

    The callback is correlated using the provider merchant reference.
    The provider transaction ID is persisted, then the authoritative
    payment status is retrieved from the provider Status API.
    """

    service.process_payment_callback(
        provider=payment_provider,
        payload=payload,
    )

    return {
        "status": "received",
    }


@router.get(
    "/transactions",
    response_model=PaymentTransactionListResponse,
)
def list_payment_transactions(
    status_filter: PaymentStatus | None = Query(
        default=None,
        alias="status",
    ),
    current_user: User = Depends(
        get_current_user,
    ),
    service: PaymentTransactionService = Depends(
        get_payment_transaction_service,
    ),
) -> PaymentTransactionListResponse:
    """
    List payment transactions belonging to the authenticated user.

    Transactions may optionally be filtered by payment status.
    """

    transactions = service.list_user_transactions(
        user_id=current_user.id,
        status=status_filter,
    )

    return PaymentTransactionListResponse(
        transactions=[
            PaymentTransactionResponse.model_validate(
                transaction,
            )
            for transaction in transactions
        ],
    )


@router.get(
    "/transactions/{transaction_id}",
    response_model=PaymentTransactionResponse,
)
def get_payment_transaction(
    transaction_id: UUID,
    current_user: User = Depends(
        get_current_user,
    ),
    service: PaymentTransactionService = Depends(
        get_payment_transaction_service,
    ),
) -> PaymentTransactionResponse:
    """
    Retrieve a payment transaction belonging to the authenticated user.

    Transactions owned by another user are intentionally reported as
    not found to avoid exposing resource existence.
    """

    transaction = service.get_transaction(
        transaction_id,
    )

    if transaction.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment transaction not found.",
        )

    return PaymentTransactionResponse.model_validate(
        transaction,
    )


@router.get(
    "/transactions/{transaction_id}/status",
    response_model=PaymentStatusResponse,
)
def synchronize_payment_status(
    transaction_id: UUID,
    current_user: User = Depends(
        get_current_user,
    ),
    service: PaymentTransactionService = Depends(
        get_payment_transaction_service,
    ),
) -> PaymentStatusResponse:
    """
    Retrieve the latest payment status from the provider and
    synchronize the local transaction.

    Only the authenticated owner of the transaction may perform
    this operation.
    """

    transaction = service.get_transaction(
        transaction_id,
    )

    if transaction.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment transaction not found.",
        )

    transaction = service.synchronize_payment_status(
        transaction_id=transaction.id,
    )

    return PaymentStatusResponse(
        transaction=PaymentTransactionResponse.model_validate(
            transaction,
        ),
    )
