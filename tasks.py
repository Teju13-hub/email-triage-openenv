def grade_easy(actions):
    """Grade: did the agent correctly label at least one email as urgent?"""
    return 1.0 if any(a.get('label') == 'urgent' for a in actions) else 0.0


def grade_medium(actions):
    """Grade: fraction of spam/normal labels out of expected 6."""
    if not actions:
        return 0.0
    matched = sum(1 for a in actions if a.get('label') in ['spam', 'normal'])
    return min(matched / 6, 1.0)


def grade_hard(actions):
    """Grade: classification accuracy + reply quality bonus."""
    expected = {
        1: 'urgent',
        2: 'spam',
        3: 'normal',
        4: 'normal',
        5: 'urgent',
        6: 'normal',
        7: 'normal',
        8: 'urgent',
        9: 'normal',
        10: 'spam',
    }
    correct = 0
    reply_quality = 0.0

    for a in actions:
        if expected.get(a.get('email_id')) == a.get('label'):
            correct += 1
        if a.get('response') and len(a.get('response', '')) > 20:
            reply_quality += 0.05

    total = len(expected)
    return min((correct / total) + reply_quality, 1.0)
