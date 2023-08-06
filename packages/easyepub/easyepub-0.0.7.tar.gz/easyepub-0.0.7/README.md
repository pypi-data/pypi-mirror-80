# EasyEpub
### Library for easier translating book pages in png.

# Installation

###### Download library using pip
```bash
$ pip3 install easyepub
```

# Usage example
###### Install and import the library
```pip3
from easyepub import EasyEpub

easy = EasyEpub("path-to-book/book.epub")
```
###### Retrieving book metadata
```python3
for meta in easy.meta:
    print(meta)
```
###### Retrieving book cover
```python3
easy.get_cover("path-for-save/cover.png")
```
###### Retrieving book chapters
```python3
easy.get_content("path-for-save")
```
# 🤝 Contributing
#### Feel free to contribute. <a href="https://github.com/xcaq/easyepub/graphs/contributors" align=center>Project contributors</a>

