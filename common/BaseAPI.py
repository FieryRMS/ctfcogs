from abc import ABC, abstractmethod

from pydantic import BaseModel, ConfigDict
from typing_extensions import Generic, TypeVar, overload

from common.types import OptStr


class Challenge(BaseModel):
    id: str
    name: str
    is_solved: bool
    description: OptStr
    flag: OptStr

    model_config = ConfigDict(extra="allow")


class Session(BaseModel):
    model_config = ConfigDict(extra="allow")


TSession = TypeVar("TSession", bound=Session, covariant=True, default=Session)
TChallenge = TypeVar("TChallenge", bound=Challenge, covariant=True, default=Challenge)


class BaseAPI(ABC, Generic[TChallenge, TSession]):
    """Base class API wrapper for ctf platforms"""

    @classmethod
    @abstractmethod
    def verify(cls, link: str) -> bool:
        """
        Verify this is the appropriate platform class for the given link

        Parameters
        ----------
        link: str
            The link to the platform to verify

        Returns
        -------
        bool
            True if this is the appropriate platform class for the given link
        """

    @classmethod
    @overload
    def login(cls, *, uname: str, pwd: str) -> TSession: ...

    @classmethod
    @overload
    def login(cls, *, token: str) -> TSession: ...

    @classmethod
    @abstractmethod
    def login(cls, *, uname: OptStr = None, pwd: OptStr = None, token: OptStr = None) -> TSession:
        """
        Login to the platform

        Parameters
        ----------
        uname: str
            The username to login with
        pwd: str
            The password to login with
        token: str
            The token to login with

        Returns
        -------
        TSession
            The session object for the platform
        """

    @classmethod
    @abstractmethod
    def logout(cls, session: Session) -> None:
        """
        Logout of the platform

        Parameters
        ----------
        session: Session
            The session object to logout
        """

    @classmethod
    @abstractmethod
    def get_challenges(cls, session: Session) -> list[TChallenge]:
        """
        Get the challenges for this platform

        Parameters
        ----------
        session: Session
            The session object to use for the request

        Returns
        -------
        list[TChallenge]
            A list of challenges for this platform
        """

    @classmethod
    @abstractmethod
    def get_challenge(cls, id: str, session: Session) -> TChallenge:
        """
        Get a specific challenge for this platform

        Parameters
        ----------
        id: str
            The id of the challenge to get
        session: Session
            The session object to use for the request

        Returns
        -------
        TChallenge
            The challenge for this platform
        """

    @classmethod
    @abstractmethod
    def submit_flag(cls, session: Session, challenge: Challenge, flag: str) -> bool:
        """
        Submit a flag for a specific challenge

        Parameters
        ----------
        session: Session
            The session object to use for the submission
        challenge: Challenge
            The challenge to submit the flag for
        flag: str
            The flag to submit

        Returns
        -------
        bool
            True if the flag was accepted, False otherwise
        """

    @classmethod
    @abstractmethod
    def submit_flags(
        cls, session: Session, challenges: list[Challenge], flags: list[str]
    ) -> list[bool]:
        """
        Submit multiple flags for multiple challenges

        Parameters
        ----------
        session: Session
            The session object to use for the submission
        challenges: list[Challenge]
            The challenges to submit the flags for
        flags: list[str]
            The flags to submit

        Returns
        -------
        list[bool]
            A list of booleans indicating if the flag was accepted for each challenge

        Raises
        ------
        ValueError
            If the number of challenges and flags do not match
        """
