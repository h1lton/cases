import asyncio
import time

from src.logger import logger


def assets(path: str):
    """
    Передайте путь к ресурсу в assets
    и вернётся относительный путь от cwd.

    Изначально нужен был для подсказок в PyCharm.
    """
    return f"assets/{path}"


def blend_colors(color1, color2):
    """Смешивает два цвета в формате hex"""
    if color1[0] == "#":
        color1 = color1[1:]

    if color2[0] == "#":
        color2 = color2[1:]

    # Смешивание цветов
    r = (int(color1[0:2], 16) + int(color2[0:2], 16)) // 2
    g = (int(color1[2:4], 16) + int(color2[2:4], 16)) // 2
    b = (int(color1[4:6], 16) + int(color2[4:6], 16)) // 2

    # Преобразование RGB в HEX
    blended_color = f"#{r:02x}{g:02x}{b:02x}"

    return blended_color


def extime(message: str = "Execution time"):
    def wrapper(func):
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000
            logger.info(f"{message}: {execution_time:.0f} ms")
            return result

        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            result = await func(*args, **kwargs)
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000
            logger.info(f"{message}: {execution_time:.0f} ms")
            return result

        def wrapper(*args, **kwargs):
            if asyncio.iscoroutinefunction(func):
                return async_wrapper(*args, **kwargs)
            else:
                return sync_wrapper(*args, **kwargs)

        return wrapper

    return wrapper
