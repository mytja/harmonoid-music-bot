def format_duration(duration):
    mins = str(duration // 60)
    secs = str(duration % 60)
    if len(mins) < 2:
        mins = "0" + mins
    if len(secs) < 2:
        secs = "0" + secs
    return f"{mins}:{secs}"


def format_duration_yt(duration):
    mins, secs = duration.split(":")
    if len(mins) < 2:
        mins = "0" + mins
    if len(secs) < 2:
        secs = "0" + secs
    return f"{mins}:{secs}"
