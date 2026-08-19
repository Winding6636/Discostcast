from discord import opus


def load_opus_lib() -> None:
    """
    Take steps needed to load opus library through discord.py
    """
    if opus.is_loaded():
        return

    # ctypes.util.find_library() relies on `ldconfig`, which musl/Alpine
    # does not ship. That makes _load_default() silently fail (it swallows
    # all exceptions and just returns False) without raising OSError here,
    # so we can't rely on it alone. Fall back to well-known library names.
    if opus._load_default():  # pylint: disable=protected-access
        return

    for candidate in ("libopus.so.0", "libopus.so", "opus"):
        try:
            opus.load_opus(candidate)
            return
        except OSError:
            continue

    raise RuntimeError("Could not load an opus lib.")
