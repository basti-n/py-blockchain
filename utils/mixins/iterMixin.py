class IterMixin:
    def __iter__(self):
        for key, value in self.__dict__.items():
            yield key, value
