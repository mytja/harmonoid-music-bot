class Method:
    
    @staticmethod
    def formatDuration(duration: str) -> str:
        duration = int(duration)
        minutes = duration // 60
        seconds = duration % 60
        if minutes < 10:
            minutes = f'0{minutes}'
        if seconds < 10:
            seconds = f'0{seconds}'
        return f'{minutes}:{seconds}'

    @staticmethod
    def formatDurationYT(duration: str) -> str:
        minutes, seconds = duration.split(":")
        if minutes < 10:
            minutes = f'0{minutes}'
        if seconds < 10:
            seconds = f'0{seconds}'
        return f'{minutes}:{seconds}'
