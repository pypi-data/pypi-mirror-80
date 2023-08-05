# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_datastructures']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-datastructures',
    'version': '0.1.1',
    'description': 'Python datastructures package',
    'long_description': '\n\n# Python-Datastructures\n\nPython-Datastructures is a Python library containing implementations of various data structures in Python that can be used in your projects. Useful when preparing for interviews or building school projects. Focus on developing your algorithms and not worry about finding python implementations of classic data structures.\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install python-datastructures.\n\n```bash\npip install python-datastructures\n```\n\n## Usage\nSample usage of the library. Import any datastructure from the list of supported datastructures.\n\n* Stack \n* Queue\n* SinglyLinkedList\n* DoublyLinkedList\n* MaxHeap\n* MinHeap\n* Trie \n\n```python\nfrom python_datastructures import Stack\n\nstack = Stack()\nstack.push(3)\nstack.push(4)\n\nprint(stack) # returns [4, 3]\n```\n## Datastructure details\n\n<div align="center"> <h2>Stack </h2></div>\n\n|  Methood  | Description                               | Args  | Return  |\n|:---------:|-------------------------------------------|-------|---------|\n| push()    | Add element to the top of the stack.      | Value | None    |\n| pop()     | Remove element from the top of the stack. | None  | Node   |\n| peek()    | View top element in the stack.            | None  | value   |\n| isEmpty() | Check if stack is empty.                  | None  | Boolean |\n| getSize() | Get number of elements in the stack.      | None  | Integer |\n| \\__str__() | Return string representation of stack    | None  | String  |\n\n<br></br>\n<div align="center"> <h2>Queue</h2></div>\n\n|  Methood  | Description                           | Args  | Return  |\n|:---------:|---------------------------------------|-------|---------|\n| getHead() | View first element in the queue.      | None  | Value   |\n| getTail() | View last element in the queue.       | None  | Value   |\n| enqueue() | Add element to the queue.             | Value | None    |\n| dequeue() | Remove element from queue.            | None  | Node   |\n| isEmpty() | Check if queue is empty.              | None  | Boolean |\n| getSize() | Get number of elements in the queue.  | None  | Integer |\n| \\__str__() | Return string representation of queue | None  | String  |\n\n<br></br>\n<div align="center"> <h2>Trie</h2></div>\n\n|   Methood  | Description                                            | Args   | Return  |\n|:----------:|--------------------------------------------------------|--------|---------|\n| build()    | Builds a trie structure given array of words           | Array  | None    |\n| add()      | Add word to the trie structure.                        | String | None    |\n| contains() | Checks if a trie contains a word or substring of word. | String | Boolean |\n\n<br></br>\n<div align="center"> <h2>Min/Max Heap</h2></div>\n\n\n|  Methood | Description                           | Args  | Return |\n|:--------:|---------------------------------------|-------|--------|\n| build()  | Build a Heap from Array of Elements   | Array | Array  |\n| peek()   | Look up top element in Heap           | None  | Value  |\n| add()    | Add element to the Heap.              | Value | None   |\n| remove() | Remove Smallest element from the Heap | None  | Value  |\n\n<br></br>\n<div align="center"> <h2>Singly LinkedList</h2></div>\n\n|  Methood  | Description                                 | args  | return  |\n|:---------:|---------------------------------------------|-------|---------|\n| add()     | Add element to linked list.                 | Value | None    |\n| remove()  | Remove node from linkedlist.                | None  | Value   |\n| getHead() | Get value of the linkedlist head node.      | None  | Value   |\n| isEmpty() | Checks if linkedlist is empty.              | Value | Boolean |\n| getSize() | Return size of the linkedlist.              | None  | Value   |\n| _ _str__() | Return String representation of linkedlist. | None  | String  |\n\n\n<br></br>\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)UtfDBx6N.*bBpHT',
    'author': 'Tomasz Turek',
    'author_email': 'ttomaszito@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TuTomasz/Python-Datastructures',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
