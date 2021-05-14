from abc import ABC, abstractstaticmethod


class Verifier(ABC):
    @abstractstaticmethod
    def isVerified(args: any) -> bool:
        pass
