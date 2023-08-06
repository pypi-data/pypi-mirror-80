from abc import abstractmethod
import hashlib
import typing

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol  # type: ignore


class Chooser(Protocol):
    """
    Interface for chooser,
    chooser does one thing: they choose in a sequence item according to a seed given
    """

    @abstractmethod
    def seed(self, seed: str) -> None:
        """set a seed in chooser"""
        pass

    @abstractmethod
    def choice(self, sequence: typing.Sequence[typing.Any]) -> typing.Any:
        """Choose item in list"""
        pass


class HashAlgorithm(Protocol):
    """Hash Algorithm Interface for HashLibChooser """

    @abstractmethod
    def hexdigest(self) -> str:
        pass

    @abstractmethod
    def update(self, seed: typing.Any):
        pass


class HashLibChooser(Chooser):
    """
    Generic class to use any hashlib algorithm for chooser
    """

    def __init__(self, hash_algorithm: HashAlgorithm = None):
        """

        :param hash_algorithm: should be a hashlib algorithm like
        """
        self.hash_algorithm = hash_algorithm or hashlib.sha256()  # type: HashAlgorithm
        self.hexdigest = self.hash_algorithm.hexdigest()  # type: str

    def seed(self, seed: str):
        encoded_seed = seed.encode("utf-8")
        self.hash_algorithm.update(encoded_seed)
        self.hexdigest = self.hash_algorithm.hexdigest()

    def choice(self, sequence: typing.Sequence[typing.Any]):
        hexdigest_as_number = int(self.hexdigest, 16)
        sequence_len = len(sequence)
        index = (hexdigest_as_number % sequence_len) - 1
        return sequence[index]
