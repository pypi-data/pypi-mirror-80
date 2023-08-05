import unittest
from docs_generator.docs_generator.utils import create_object
from docs_generator.docs_generator.Document import Document


class SomeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.documents = [
            Document('a/b/c/d.txt'),
            Document('a/b/c/e.txt'),
        ]

    def test_generate_config(self):
        config = create_object({}, ['a', 'b', 'c'], self.documents)
        self.assertEqual({
            "A": {
                "B": {
                    "C": [{'D': 'a/b/c/d.md'}, {'E': 'a/b/c/e.md'}]
                }
            }
        }, config)

    def test_generate_config2(self):
        prev_nav = {
            "A": {
                "B": [{
                    "bc": 'a/b/bc.txt'
                }, {
                    "cd": 'a/b/cd.txt'
                }]
            }
        }
        config = create_object(prev_nav, ['a', 'b', 'c'], self.documents)
        self.assertEqual({
            "A": {
                "B": [{
                    "bc": 'a/b/bc.txt'
                }, {
                    "cd": 'a/b/cd.txt'
                },
                    {
                        "C": [{'D': 'a/b/c/d.md'}, {'E': 'a/b/c/e.md'}]
                    },
                ]
            }
        }, config)

    def test_generate_config3(self):
        prev_nav = [{
            "New A": {
                "B": [{
                    "bc": 'a/b/bc.txt'
                }, {
                    "cd": 'a/b/cd.txt'
                }]
            }
        }]

        last_one = prev_nav[len(prev_nav) - 1]
        config = create_object(last_one, ['a', 'b', 'c'], self.documents)

        self.assertEqual({
            "A": {
                "B": {
                    "C": [{'D': 'a/b/c/d.md'}, {'E': 'a/b/c/e.md'}]
                }
            }
        }, config)
