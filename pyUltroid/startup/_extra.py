# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

# https://bugs.python.org/issue26789
# 'open' not defined has been fixed in Python3.10
# for other older versions, something need to be done.


def _fix_logging(handler):
    handler._builtin_open = open

    def _new_open(self):
        open_func = self._builtin_open
        return open_func(self.baseFilename, self.mode)

    setattr(handler, "_open", _new_open)


def _ask_input():
    # Ask for Input even on Vps and other platforms.
    def new_input(*args, **kwargs):
        raise EOFError("args=" + str(args) + ", kwargs=" + str(kwargs))

    __builtins__["input"] == new_input


class HOSTED_ON:
    Attrs = ["Heroku", "Local", "Githubactions","Railway", "Windows","Qovery","Termux"]

    def __init__(self):
        self._value = self.get_hosted_on()

    def __eq__(self, what):
        return bool(what == self._value)

    def __repr__(self):
        return f"<pyUltroid.HOSTED_ON.{self._value}>"

    def __getattr__(self, item):
        item = item.replace(" ", "").lower()
        if item not in self.Attrs:
            raise AttributeError(f"{self.__class__.__name__} has no attribute '{item}'")
        return item == self._value

    def get_hosted_on():
        if os.getenv("DYNO"):
            return "heroku"
        if os.getenv("RAILWAY_STATIC_URL"):
            return "railway"
        if os.getenv("KUBERNETES_PORT"):
            return "qovery"
        if os.getenv("WINDOW") and os.getenv("WINDOW") != "0":
            return "windows"
        if os.getenv("RUNNER_USER") or os.getenv("HOSTNAME"):
            return "github actions"
        if os.getenv("ANDROID_ROOT"):
            return "termux"
        return "local"
