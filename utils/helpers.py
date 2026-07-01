from datetime import datetime

def current_date():
    return datetime.now().strftime("%Y-%m-%d")


def current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def calculate_fine(return_date, due_date):

    try:

        return_date = datetime.strptime(
            str(return_date),
            "%Y-%m-%d"
        )

        due_date = datetime.strptime(
            str(due_date),
            "%Y-%m-%d"
        )

        days = (return_date - due_date).days

        if days > 0:
            return days * 10

        return 0

    except:
        return 0


def status_badge(status):

    badges = {
        "Available":"success",
        "Issued":"danger",
        "Returned":"primary",
        "Pending":"warning"
    }

    return badges.get(status,"secondary")