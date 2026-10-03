from core.metrics import increment


def requires_approval(action):

    high_risk_keywords = [
        "close road",
        "road closure",
        "evacuate",
        "shutdown",
        "disable",
        "block road",
        "reroute traffic"
    ]

    action_lower = action.lower()

    for keyword in high_risk_keywords:

        if keyword in action_lower:
            increment("approval_required")
            return True

    return False


def request_approval(action):

    print("\n===== HUMAN APPROVAL REQUIRED =====")
    print("\nProposed action:")
    print(action)

    while True:

        response = input(
            "\nApprove this action? (yes/no): "
        ).strip().lower()

        if response in ["yes", "y"]:

            increment("approvals")
            return True

        if response in ["no", "n"]:

            increment("rejections")
            return False

        print("Please enter yes or no.")