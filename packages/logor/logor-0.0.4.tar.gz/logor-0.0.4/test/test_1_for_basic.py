import logor
import time

logger = logor.withFields({
    "FUNC": __name__,
    "ENV": "DEV",
})


def main():
    count = 0
    while count < 20:
        count += 1
        logger.info("hello world")
        logger.warning("hello world")
        logger.error("hello world")
        time.sleep(10)


if __name__ == '__main__':
    with logor.Logor(__name__, info_hooks=["logor.hooks.file.TimeFileHook"]):
        main()
