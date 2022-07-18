class FakeSession:

    committed = False

    def commit(self) -> None:
        self.committed = True
