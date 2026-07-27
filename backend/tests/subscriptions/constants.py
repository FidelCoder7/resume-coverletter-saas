from app.common.constants import (
    AIFeature,
    SubscriptionPlan,
)

DEFAULT_PLAN_LIMITS = {
    SubscriptionPlan.FREE: {
        AIFeature.RESUME_GENERATION: 3,
        AIFeature.COVER_LETTER_GENERATION: 3,
        AIFeature.COVER_LETTER_REGENERATION: 1,
        AIFeature.ATS_OPTIMIZATION: 1,
    },
    SubscriptionPlan.PRO: {
        AIFeature.RESUME_GENERATION: 10,
        AIFeature.COVER_LETTER_GENERATION: 10,
        AIFeature.COVER_LETTER_REGENERATION: 5,
        AIFeature.ATS_OPTIMIZATION: 5,
    },
}
