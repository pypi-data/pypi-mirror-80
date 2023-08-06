# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['typedstruct']
setup_kwargs = {
    'name': 'typedstruct',
    'version': '0.1.0',
    'description': 'A wrapper around the struct library with support for PEP 484 types.',
    'long_description': '# typedstruct\n\n[![Build Status](https://travis-ci.com/luizribeiro/typedstruct.svg?branch=master)](https://travis-ci.com/luizribeiro/typedstruct)\n[![codecov](https://codecov.io/gh/luizribeiro/typedstruct/branch/master/graph/badge.svg)](https://codecov.io/gh/luizribeiro/typedstruct)\n[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)\n\nA wrapper around the [`struct` built-in module](https://docs.python.org/3/library/struct.html)\nwith support for [typing](https://www.python.org/dev/peps/pep-0484/), on top of\nPython 3.7 [`dataclasses`](https://docs.python.org/3/library/dataclasses.html).\n\n## Example\n\nFor example, if you wanted to read the header of BMP files, you could write\nthis:\n\n```python\nfrom dataclasses import dataclass\nfrom typedstruct import LittleEndianStruct, StructType\n\n\n@dataclass\nclass BMPHeader(LittleEndianStruct):\n    type: int = StructType.uint16()  # magic identifier: 0x4d42\n    size: int = StructType.uint32()  # file size in bytes\n    reserved1: int = StructType.uint16()  # not used\n    reserved2: int = StructType.uint16()  # not used\n    offset: int = StructType.uint32()  # image data offset in bytes\n    dib_header_size: int = StructType.uint32()  # DIB header size in bytes\n    width_px: int = StructType.int32()  # width of the image\n    height_px: int = StructType.int32()  # height of the image\n    num_planes_px: int = StructType.uint16()  # number of color planes\n    bits_per_pixel: int = StructType.uint16()  # bits per pixel\n    compression: int = StructType.uint32()  # compression type\n    image_size_bytes: int = StructType.uint32()  # compression type\n    x_resolution_ppm: int = StructType.int32()  # pixels per meter\n    y_resolution_ppm: int = StructType.int32()  # pixels per meter\n    num_colors: int = StructType.int32()  # number of colors\n    important_colors_colors: int = StructType.int32()  # important colors\n\n\nwith open("some_file.bmp", "rb") as file:\n    raw_data = file.read(BMPHeader.get_size())\n    bmp_header = BMPHeader.unpack(raw_data)\n    assert bmp_header.type == 0x4D42\n    print(f"This image is {bmp_header.width_px}x{bmp_header.height_px}")\n```\n',
    'author': 'Luiz Ribeiro',
    'author_email': 'luizribeiro@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/luizribeiro/typedstruct',
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
