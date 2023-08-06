import pathlib

class RepoLayoutBase:
    def get_key_location(self, key: str) -> pathlib.Path:
        raise NotImplementedError

class NodirLayout(RepoLayoutBase):
    def get_key_location(self, key: str):
        return pathlib.Path(key)

