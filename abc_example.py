import abc
import os
import re
import json
import yaml
from typing import List
from dataclasses import dataclass


"""Note, the check requiring abstract methods to be implemented
only happens when an object is initialized."""


@dataclass
class Config(metaclass=abc.ABCMeta):
    ip: str
    port: int


# Register ConfigWrapper as virtual subclass of Config
@Config.register
class ConfigWrapper(metaclass=abc.ABCMeta):

    """Property wrapper for Config."""

    # TODO ensure that the wrapper is the same type as Config

    def __repr__(self) -> str:
        """repr implementation like a dataclass"""
        return f"{self.__class__.__name__}(ip='{self.ip}', port={self.port})"

    @property
    @abc.abstractmethod
    def ip(self) -> str:
        """Abstract getter for ip."""
        raise NotImplementedError
    
    @ip.setter
    @abc.abstractmethod
    def ip(self, value) -> None:
        """Abstract setter for ip."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def port(self) -> int:
        """Abstract getter for port."""

    @port.setter
    @abc.abstractmethod
    def port(self, value) -> None:
        """Abstract setter for port."""
    

class GuardedConfig(ConfigWrapper):

    _ipv4_regex = r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
    _port_min = 0
    _port_max = 65535

    def __init__(self, config: Config) -> None:
        super().__init__()
        self._config = config

    @property
    def ip(self) -> str:
        """IP address."""
        return self._config.ip

    @ip.setter
    def ip(self, value: str) -> None:
        """Setter for IP address.
        
        Guards against input type and format. Requires IPv4 format."""
        assert isinstance(value, str)
        assert re.match(self._ipv4_regex, value), f"ip '{value}' does not have correct format"
        self._config.ip = value

    @property
    def port(self) -> int:
        """Port."""
        return self._config.port
    
    @port.setter
    def port(self, value) -> None:
        """Setter for port.
        
        Guards against input type and value range."""
        assert isinstance(value, int)
        assert value in range(self._port_min, self._port_max+1), f"port {value} is not in valid range"
        self._config.port = value


class ConfigParser(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def import_config(path: str) -> Config:
        """Import config."""
        raise NotImplementedError
    
    @staticmethod
    @abc.abstractmethod
    def is_file_compatible(path: str) -> bool:
        """Checks if a file is compatible with parser."""
        raise NotImplementedError


class JsonConfigParser(ConfigParser):

    """JSON config handler."""
    
    @staticmethod
    def import_config(path: str) -> Config | None:
        try:
            with open(path, "r") as f:
                config = Config(None, None)
                
                json_ = json.loads(f.read())
                if json_.keys() != config.__dict__.keys():
                    return None
                
                for key in config.__dict__.keys():
                    setattr(config, key, json_[key])

        except Exception as e:
            print(f"import_config(), Exception, e: {e}")
            return None
        
        return config
    
    @staticmethod
    def is_file_compatible(path: str) -> bool:
        return os.path.isfile(path) and path.endswith(".json")


class YamlConfigParser(ConfigParser):

    @staticmethod
    def import_config(path: str) -> Config | None:
        try:
            with open(path, "r") as f:
                config = Config(None, None)
                yaml_ = yaml.load(f.read())
                if yaml_.keys() != config.__dict__.keys():
                    return None
                
                for key in config.__dict__.keys():
                    setattr(config, key, yaml_[key])

        except Exception as e:
            print(f"import_config(), Exception, e: {e}")
            return None
        
        return config
    
    @staticmethod
    def is_file_compatible(path: str) -> bool:
        return os.path.isfile(path) and path.endswith(".yaml")


def main():

    # Check parsers
    parsers: List[ConfigParser] = [
        JsonConfigParser(),
        YamlConfigParser()
    ]

    for parser in parsers:
        assert isinstance(parser, ConfigParser)


    # Check GuardedConfig
    import_path = "abc_example/config.yaml"
    config: ConfigParser = YamlConfigParser().import_config(import_path)
    config.ip = "123.123.123.123"
    print(config)

    # Wrap config with guards
    guarded_config: ConfigParser = GuardedConfig(config)

    try:
        guarded_config.ip = "localhost"
    except AssertionError as _:
        pass

    guarded_config.port = 6321      
    guarded_config.ip = "127.0.0.1"
    print(guarded_config)

    print(f"guarded_config is an instance of Config, {isinstance(guarded_config, Config)}")


if __name__ == "__main__":
    main()


