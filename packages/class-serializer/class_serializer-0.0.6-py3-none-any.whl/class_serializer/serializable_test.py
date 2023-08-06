import json
from unittest import TestCase

from src.class_serializer.test_models.bar import Bar
from src.class_serializer.test_models.foo import Foo


class SerializableTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.foo = Foo('foo', 'bar', Bar(1), [Bar(2), Bar(3)], {'bar_key': Bar(4)})
        serialized = cls.foo.serialize()
        cls.as_dict = json.loads(serialized)

    def test_a_str(self):
        self.assertEqual('foo', self.as_dict['a_str'])

    def test_a_str_with_custom_key(self):
        self.assertEqual('bar', self.as_dict['custom_key'])

    def test_bar(self):
        self.assertEqual({'id': 1}, self.as_dict['bar'])

    def test_bars(self):
        bars = self.as_dict['bars']
        self.assertEqual(2, len(bars))
        self.assertEqual(2, bars[0]['id'])
        self.assertEqual(3, bars[1]['id'])

    def test_dict_of_bars(self):
        self.assertEqual(4, self.as_dict['dict_of_bars']['bar_key']['id'])
