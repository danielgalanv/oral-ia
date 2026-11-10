"""Select the activity's frozen local model for one invocation, reset on all exits."""

from functools import wraps

from oralia.infrastructure.db import models
from oralia.infrastructure.generation.config import activity_model


def configured_generation(function):
    @wraps(function)
    async def invoke(db, session, *args, **kwargs):
        governance = db.get(models.ActivityGovernance, session.activity_configuration_id)
        token = activity_model.set(governance.model_id if governance else None)
        try:
            return await function(db, session, *args, **kwargs)
        finally:
            activity_model.reset(token)

    return invoke
