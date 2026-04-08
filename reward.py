def compute_reward(emails, action, history):
    reward = 0.0
    for email in emails:
        if email.id != action.email_id:
            continue

        # Classification reward
        if email.priority_hint == action.label:
            reward += 0.5
        else:
            reward -= 0.4

        # Reply reward
        if action.type == "reply":
            if action.response and len(action.response) > 20:
                reward += 0.4
            else:
                reward -= 0.3

        # Deadline awareness
        if email.deadline:
            reward += 0.1

        # Repetition penalty
        if str(action) in history:
            reward -= 0.5

    # Clamp reward
    return max(min(reward, 1.0), -1.0), "winning"
