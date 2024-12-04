def format_number(value):
    """格式化數字為可讀形式"""
    try:
        value = float(value)
        sign = "-" if value < 0 else ""  # 判斷符號
        value = abs(value)  # 取絕對值來進行格式化

        if value >= 1e12:
            return f"{sign}{value / 1e12:.3f}T"
        elif value >= 1e9:
            return f"{sign}{value / 1e9:.3f}B"
        elif value >= 1e6:
            return f"{sign}{value / 1e6:.3f}M"
        return f"{sign}{value:.2f}"
    except:
        return value