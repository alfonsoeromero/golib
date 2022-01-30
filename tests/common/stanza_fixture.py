from multiprocessing.dummy import Value


class StanzaFixture:
    dummy_tag: str = "tag"
    dummy_value: Value = Value()