import sys

from dynaconf import LazySettings
from loguru import logger


class Logger:
    def __init__(self):
        logger.remove()
        self._default_level = set()
        self._parse_settings()

    def __call__(self):
        return logger

    def _parse_settings(self):
        root_settings = LazySettings(SETTINGS_FILE_FOR_DYNACONF='log.toml')
        try:
            if sys.platform == 'win32':
                self.settings = root_settings.windows
            else:
                self.settings = root_settings.linux
            try:
                for default_level in root_settings.level.default:
                    self._default_level.add(default_level)
            except:
                raise ValueError('配置文件中的[level.default]必须被保留')
        except AttributeError:
            print('警告：该系统对应的日志配置不存在！！！')
        else:
            self._create_handler()

    def _create_handler(self):
        handlers = {}
        share_options = {}
        for key, option in self.settings.items():
            if key in self._default_level:
                handlers[key] = option
            else:
                share_options[key] = option
        for level, option in handlers.items():
            handler_option = share_options.copy()
            handler_option.update(option)
            handler_option['level'] = level.upper()
            logger.add(**handler_option)


if __name__ == '__main__':
    log = Logger()()
    print(log)
