from decimal import Decimal
from uuid import UUID, uuid4

from app.billing.exceptions import (
    InvalidPaymentCallback,
    InvalidPaymentTransactionState,
    PaymentTransactionAlreadyCompleted,
    PaymentTransactionNotFound,
)
from app.billing.models import PaymentTransaction
from app.billing.pricing import get_subscription_price
from app.billing.providers.base import PaymentProvider
from app.billing.providers.schemas import PaymentInitiationRequest
from app.billing.repository import PaymentTransactionRepository
from app.common.constants import (
    BillingTransactionType,
    PaymentMethod,
    PaymentStatus,
    SubscriptionPlan,
)
from app.common.constants import PaymentProvider as PaymentProviderType
from app.core.config import settings


class PaymentTransactionService:
    """
    Service responsible for payment transaction lifecycle management
    and payment provider orchestration.

    This service coordinates:

    - Payment provider communication through the provider abstraction.
    - Payment transaction persistence through the repository.
    - Payment transaction lifecycle transitions.

    Provider-specific implementations such as PesaPalProvider remain
    outside the billing business logic.
    """

    # ------------------------------------------------------------------
    # Payment Transaction Lifecycle
    # ------------------------------------------------------------------

    _VALID_TRANSITIONS: dict[
        PaymentStatus,
        set[PaymentStatus],
    ] = {
        PaymentStatus.PENDING: {
            PaymentStatus.COMPLETED,
            PaymentStatus.FAILED,
            PaymentStatus.CANCELLED,
            PaymentStatus.EXPIRED,
        },
        PaymentStatus.COMPLETED: set(),
        PaymentStatus.FAILED: set(),
        PaymentStatus.CANCELLED: set(),
        PaymentStatus.EXPIRED: set(),
    }

    def __init__(
        self,
        repository: PaymentTransactionRepository,
        provider: PaymentProvider,
    ) -> None:
        self.repository = repository
        self.provider = provider

    # ------------------------------------------------------------------
    # Provider Integration
    # ------------------------------------------------------------------
    def start_payment(
        self,
        *,
        user_id: UUID,
        subscription_plan: SubscriptionPlan,
        transaction_type: BillingTransactionType,
        customer_email: str,
        customer_name: str,
        payment_method: PaymentMethod | None = None,
    ) -> tuple[
        PaymentTransaction,
        str | None,
    ]:
        """
        Initiate a payment with the configured provider and persist
        the resulting payment transaction.
        """

        price = get_subscription_price(
            subscription_plan,
        )

        provider_order_id = f"ord_{uuid4().hex}"

        request = PaymentInitiationRequest(
            provider_order_id=provider_order_id,
            amount=price.amount,
            currency=price.currency,
            description=(f"{subscription_plan.value.title()} Subscription"),
            callback_url=settings.PESAPAL_CALLBACK_URL,
            customer_email=customer_email,
            customer_name=customer_name,
            payment_method=payment_method,
        )

        result = self.provider.initiate_payment(
            request,
        )

        transaction = self.initiate_payment(
            user_id=user_id,
            subscription_plan=subscription_plan,
            transaction_type=transaction_type,
            provider=PaymentProviderType.PESAPAL,
            provider_order_id=provider_order_id,
            amount=price.amount,
            currency=price.currency,
            payment_method=payment_method,
            provider_response=result.provider_response,
        )

        if result.provider_transaction_id is not None:
            transaction.provider_transaction_id = result.provider_transaction_id

            transaction = self.repository.update(
                transaction,
            )

        if result.status != PaymentStatus.PENDING:
            transaction = self._synchronize_initiation_result(
                transaction=transaction,
                status=result.status,
                provider_transaction_id=result.provider_transaction_id,
                payment_method=payment_method,
                provider_response=result.provider_response,
            )

        return (
            transaction,
            result.redirect_url,
        )

    def synchronize_payment_status(
        self,
        *,
        transaction_id: UUID,
        provider_order_id: str | None = None,
    ) -> PaymentTransaction:
        """
        Retrieve the latest payment status from the provider and
        synchronize the local payment transaction.

        Args:
            transaction_id:
                Local payment transaction ID.

            provider_order_id:
                Optional provider-specific order identifier used for
                status lookup. For PesaPal, this is the order tracking ID.

                If omitted, the transaction's provider_transaction_id
                is used when available.

        Returns:
            The synchronized payment transaction.

        Raises:
            PaymentTransactionNotFound:
                If the transaction does not exist.

            InvalidPaymentTransactionState:
                If the provider reports a state that cannot be applied
                to the local transaction.
        """

        transaction = self.get_transaction(
            transaction_id,
        )

        if transaction.provider_transaction_id is None:
            raise InvalidPaymentCallback(
                "Payment transaction does not have a provider transaction ID.",
            )

        result = self.provider.get_payment_status(
            provider_transaction_id=(transaction.provider_transaction_id),
        )

        if result.status == PaymentStatus.COMPLETED:
            return self.complete_payment(
                transaction_id=transaction.id,
                provider_transaction_id=(result.provider_transaction_id),
                payment_method=result.payment_method,
                provider_response=result.provider_response,
            )

        if result.status == PaymentStatus.FAILED:
            return self.fail_payment(
                transaction_id=transaction.id,
                failure_reason=result.failure_reason,
                provider_response=result.provider_response,
            )

        if result.status == PaymentStatus.CANCELLED:
            return self.cancel_payment(
                transaction_id=transaction.id,
                provider_response=result.provider_response,
            )

        if result.status == PaymentStatus.EXPIRED:
            return self.expire_payment(
                transaction_id=transaction.id,
                provider_response=result.provider_response,
            )

        return transaction

    def process_payment_callback(
        self,
        *,
        provider: PaymentProvider,
        payload: dict,
    ) -> PaymentTransaction:
        """
        Process an asynchronous payment provider callback.

        The callback is used to correlate the provider notification
        with the local transaction and persist the provider tracking ID.

        The provider's Status API remains authoritative for the final
        payment state. Therefore, the callback payload itself does not
        directly complete or fail the transaction.
        """

        callback = provider.normalize_callback(
            payload,
        )

        transaction = self.get_by_provider_order_id(
            provider=provider.provider_type,
            provider_order_id=callback.provider_order_id,
        )

        if callback.provider_transaction_id is not None:
            transaction.provider_transaction_id = callback.provider_transaction_id

        transaction.provider_response = callback.provider_response

        transaction = self.repository.update(
            transaction,
        )

        if transaction.status != PaymentStatus.PENDING:
            return transaction

        if transaction.provider_transaction_id is None:
            return transaction

        return self.synchronize_payment_status(
            transaction_id=transaction.id,
        )

    def _synchronize_initiation_result(
        self,
        *,
        transaction: PaymentTransaction,
        status: PaymentStatus,
        provider_transaction_id: str | None,
        payment_method: PaymentMethod | None,
        provider_response: dict | None,
    ) -> PaymentTransaction:
        """
        Apply a non-pending provider initiation result to the local
        transaction.

        This is primarily a defensive integration path because most
        payment providers return PENDING after accepting an order.
        """

        if status == PaymentStatus.COMPLETED:
            return self.complete_payment(
                transaction_id=transaction.id,
                provider_transaction_id=provider_transaction_id,
                payment_method=payment_method,
                provider_response=provider_response,
            )

        if status == PaymentStatus.FAILED:
            return self.fail_payment(
                transaction_id=transaction.id,
                provider_response=provider_response,
            )

        if status == PaymentStatus.CANCELLED:
            return self.cancel_payment(
                transaction_id=transaction.id,
                provider_response=provider_response,
            )

        if status == PaymentStatus.EXPIRED:
            return self.expire_payment(
                transaction_id=transaction.id,
                provider_response=provider_response,
            )

        return transaction

    # ------------------------------------------------------------------
    # Payment Transaction Lifecycle
    # ------------------------------------------------------------------

    def initiate_payment(
        self,
        *,
        user_id: UUID,
        subscription_plan: SubscriptionPlan,
        transaction_type: BillingTransactionType,
        provider: PaymentProvider,
        provider_order_id: str,
        amount: Decimal,
        currency: str = "KES",
        payment_method: PaymentMethod | None = None,
        provider_response: dict | None = None,
    ) -> PaymentTransaction:
        """
        Create a new pending payment transaction.

        New payment transactions always begin in the PENDING state.
        """

        return self.repository.create(
            user_id=user_id,
            subscription_plan=subscription_plan,
            transaction_type=transaction_type,
            provider=provider,
            provider_order_id=provider_order_id,
            amount=amount,
            currency=currency,
            payment_method=payment_method,
            status=PaymentStatus.PENDING,
            provider_response=provider_response,
        )

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    def get_transaction(
        self,
        transaction_id: UUID,
    ) -> PaymentTransaction:
        """
        Retrieve a payment transaction by ID.

        Raises:
            PaymentTransactionNotFound:
                If no transaction exists with the requested ID.
        """

        transaction = self.repository.get_by_id(
            transaction_id,
        )

        if transaction is None:
            raise PaymentTransactionNotFound(
                f"Payment transaction {transaction_id} was not found.",
            )

        return transaction

    def get_by_provider_order_id(
        self,
        *,
        provider: PaymentProvider,
        provider_order_id: str,
    ) -> PaymentTransaction:
        """
        Retrieve a payment transaction by provider and order ID.

        Raises:
            PaymentTransactionNotFound:
                If no matching transaction exists.
        """

        transaction = self.repository.get_by_provider_order_id(
            provider=provider,
            provider_order_id=provider_order_id,
        )

        if transaction is None:
            raise PaymentTransactionNotFound(
                f"Payment transaction with provider={provider.value} "
                f"and provider_order_id={provider_order_id} "
                "was not found.",
            )

        return transaction

    def get_by_provider_transaction_id(
        self,
        *,
        provider: PaymentProvider,
        provider_transaction_id: str,
    ) -> PaymentTransaction:
        """
        Retrieve a payment transaction by provider and transaction ID.

        Raises:
            PaymentTransactionNotFound:
                If no matching transaction exists.
        """

        transaction = self.repository.get_by_provider_transaction_id(
            provider=provider,
            provider_transaction_id=provider_transaction_id,
        )

        if transaction is None:
            raise PaymentTransactionNotFound(
                f"Payment transaction with provider={provider.value} "
                f"and provider_transaction_id={provider_transaction_id} "
                "was not found.",
            )

        return transaction

    def list_user_transactions(
        self,
        *,
        user_id: UUID,
        status: PaymentStatus | None = None,
    ) -> list[PaymentTransaction]:
        """
        Return payment transactions belonging to a user.

        Transactions are returned newest first.
        Optionally filters by payment status.
        """

        return self.repository.list_by_user(
            user_id=user_id,
            status=status,
        )

    # ------------------------------------------------------------------
    # Lifecycle Transitions
    # ------------------------------------------------------------------

    def complete_payment(
        self,
        *,
        transaction_id: UUID,
        provider_transaction_id: str | None = None,
        payment_method: PaymentMethod | None = None,
        provider_response: dict | None = None,
    ) -> PaymentTransaction:
        """
        Mark a pending payment transaction as completed.
        """

        transaction = self.get_transaction(
            transaction_id,
        )

        self._validate_transition(
            transaction=transaction,
            target_status=PaymentStatus.COMPLETED,
        )

        transaction.status = PaymentStatus.COMPLETED

        if provider_transaction_id is not None:
            transaction.provider_transaction_id = provider_transaction_id

        if payment_method is not None:
            transaction.payment_method = payment_method

        if provider_response is not None:
            transaction.provider_response = provider_response

        return self.repository.update(
            transaction,
        )

    def fail_payment(
        self,
        *,
        transaction_id: UUID,
        failure_reason: str | None = None,
        provider_response: dict | None = None,
    ) -> PaymentTransaction:
        """
        Mark a pending payment transaction as failed.
        """

        transaction = self.get_transaction(
            transaction_id,
        )

        self._validate_transition(
            transaction=transaction,
            target_status=PaymentStatus.FAILED,
        )

        transaction.status = PaymentStatus.FAILED

        if failure_reason is not None:
            transaction.failure_reason = failure_reason

        if provider_response is not None:
            transaction.provider_response = provider_response

        return self.repository.update(
            transaction,
        )

    def cancel_payment(
        self,
        *,
        transaction_id: UUID,
        provider_response: dict | None = None,
    ) -> PaymentTransaction:
        """
        Mark a pending payment transaction as cancelled.
        """

        transaction = self.get_transaction(
            transaction_id,
        )

        self._validate_transition(
            transaction=transaction,
            target_status=PaymentStatus.CANCELLED,
        )

        transaction.status = PaymentStatus.CANCELLED

        if provider_response is not None:
            transaction.provider_response = provider_response

        return self.repository.update(
            transaction,
        )

    def expire_payment(
        self,
        *,
        transaction_id: UUID,
        provider_response: dict | None = None,
    ) -> PaymentTransaction:
        """
        Mark a pending payment transaction as expired.
        """

        transaction = self.get_transaction(
            transaction_id,
        )

        self._validate_transition(
            transaction=transaction,
            target_status=PaymentStatus.EXPIRED,
        )

        transaction.status = PaymentStatus.EXPIRED

        if provider_response is not None:
            transaction.provider_response = provider_response

        return self.repository.update(
            transaction,
        )

    # ------------------------------------------------------------------
    # Internal Lifecycle Validation
    # ------------------------------------------------------------------

    def _validate_transition(
        self,
        *,
        transaction: PaymentTransaction,
        target_status: PaymentStatus,
    ) -> None:
        """
        Validate a payment transaction state transition.
        """

        current_status = transaction.status

        if current_status == PaymentStatus.COMPLETED:
            raise PaymentTransactionAlreadyCompleted(
                f"Payment transaction {transaction.id} " "has already been completed.",
            )

        valid_targets = self._VALID_TRANSITIONS.get(
            current_status,
            set(),
        )

        if target_status not in valid_targets:
            raise InvalidPaymentTransactionState(
                f"Cannot transition payment transaction "
                f"{transaction.id} from "
                f"{current_status.value} to "
                f"{target_status.value}.",
            )
