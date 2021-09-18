from .. import LOGS, asst, udB, ultroid_bot  # pylint ignore

CMD_HELP = {}


def sudoers():
    if udB.get("SUDOS"):
        return udB["SUDOS"].split()
    return []


def should_allow_sudo():
    if udB.get("SUDO") == "True":
        return True
    return False


def owner_and_sudos():
    return [str(ultroid_bot.uid), *sudoers()]
