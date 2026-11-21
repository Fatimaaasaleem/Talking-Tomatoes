import time
import uuid


CONFIRMATION_TIMEOUT = 120

_pending_actions = {}


def create_pending_action(user_id, tool_name, arguments):
    """Store a database action awaiting user confirmation."""

    action_id = str(uuid.uuid4())

    _pending_actions[user_id] = {
        "action_id": action_id,
        "tool_name": tool_name,
        "arguments": arguments.copy(),
        "created_at": time.time()
    }

    return action_id


def get_pending_action(user_id):
    """Retrieve a user's pending action if it has not expired."""

    action = _pending_actions.get(user_id)

    if action is None:
        return None

    elapsed = time.time() - action["created_at"]

    if elapsed > CONFIRMATION_TIMEOUT:
        _pending_actions.pop(user_id, None)
        return None

    return action


def clear_pending_action(user_id):
    """Remove a user's pending action."""

    _pending_actions.pop(user_id, None)