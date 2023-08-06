# Package: generalfile
File manager for intuitive cross-platform compatability with gathered useful functionality.
Generalfile operates on the middle ground of all relevant operating systems.
E.g. Windows being case insensitive -> Don't allow paths with same name but differeing case.
Uses a race condition safe lock mechanism for all file operations.

## Installation
```
pip install generalfile
```

## Usage example
```python
from generalfile import Path

Path("newfolder/test.txt").write("foobar")  # Automatically creates new folder
assert Path("newfolder/test.txt").read() == "foobar"
Path("newfolder").delete()  # Delete entire folder

with Path("foo/bar.txt").lock():  # Recursively lock a file or even a folder which doesn't have to exist.
    pass  # The lock is created in a seperate folder, so you're free to do whatever you want in here
```
