class FooDict(dict):
    def __init__(self, seq=None, **kwargs):
        super().__init__(seq, **kwargs)