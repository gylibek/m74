import functools
import logging
import time
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:

    """
    Декоратор для логирования вызовов функций.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger = logging.getLogger(func.__name__)
            logger.setLevel(logging.INFO)

            if logger.handlers:
                logger.handlers.clear()

            handler: logging.Handler
            if filename:
                handler = logging.FileHandler(filename, encoding='utf-8')
            else:
                handler = logging.StreamHandler()

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            start_time = time.time()
            args_repr = ', '.join([repr(a) for a in args])
            kwargs_repr = ', '.join([f"{k}={repr(v)}" for k, v in kwargs.items()])
            all_args = ', '.join(filter(None, [args_repr, kwargs_repr]))
            logger.info(f"Calling {func.__name__}({all_args})")

            try:
                result = func(*args, **kwargs)
                end_time = time.time()
                logger.info(f"{func.__name__} returned {repr(result)} in {end_time - start_time:.4f} sec")
                return result
            except Exception as e:
                end_time = time.time()
                logger.error(
                    f"{func.__name__} raised {type(e).__name__}: {e} "
                    f"(args: {args_repr}, kwargs: {kwargs_repr}) "
                    f"after {end_time - start_time:.4f} sec"
                )
                raise

        return wrapper

    return decorator
