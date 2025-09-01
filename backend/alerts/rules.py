# combine model probability with simple rules to decide alert tier

def combine(model_prob, context=None):
    # context can include location, stress_level etc. For now, simple thresholds.
    if model_prob >= 0.9:
        return {'tier': 1, 'alert_score': model_prob, 'reason': ['high_prob']}
    if model_prob >= 0.7:
        return {'tier': 2, 'alert_score': model_prob, 'reason': ['medium_prob']}
    if model_prob >= 0.4:
        return {'tier': 3, 'alert_score': model_prob, 'reason': ['low_prob']}
    return {'tier': 0, 'alert_score': model_prob, 'reason': ['very_low']}


def should_alert(rule_result, user_prefs=None):
    if rule_result['tier'] == 0:
        return False
    # respect user preferences (quiet hours) - omitted for brevity
    return True