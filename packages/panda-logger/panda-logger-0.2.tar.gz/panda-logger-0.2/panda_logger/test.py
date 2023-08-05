from loguru import logger
import multiprocessing
from time import sleep
import os


def logger_messages():
    # print(id(logger_))
    for i in range(0x1 << 17):
        logger.info('{}: log{}'.format(multiprocessing.current_process().name,
                                       i))
        sleep(0.2)


if __name__ == "__main__":
    logger.remove()
    logger.add('logs/log.log', rotation='10s', enqueue=True)
    processes = []
    for i in range(10):
        process = multiprocessing.Process(target=logger_messages,
                                          name='log_process{}'.format(i))
        processes.append(process)
        process.start()
    for p in processes:
        p.join()
