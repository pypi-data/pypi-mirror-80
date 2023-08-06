"""
The idea with a mixin is a class that is never instantiated on it's own but adds functionality to another class. The
pattern is usually: "If my baseclass has implemented methods x, y, z, then a mixin adds functionality i, j, k".
Example: "if a class has implemented the method `get_url`, it can use the mixin `DisplaysUrl` that will add
`display_url` to the class.
When creating a new class it's like a checklist of things it can do via mixins e.g.
```
class MyClass(DisplaysUrl, PrintsAllAttributes, ...):
    ...
```
They are easy to add/remove and should be de-coupled from each class i.e. the class can do it's job without it

Mixin vs. multiple-inheritance:
The mechanism by which you use both is exactly the same and the difference is purely conceptual.
1) Mixin is never initialized on it's own
2) Mixin usually has a single method added to the class, not a full set of functionality a typical parent class would
   have
3) Mixin has a loose connection to the class inheriting from it, while a typical baseclass and subclass are strongly
   coupled and can often be used interchangably.

Resources:
- https://stackoverflow.com/questions/860245/mixin-vs-inheritance
- https://www.youtube.com/watch?v=S_ipdVNSFlo
"""
import abc
from typing import Union

from IPython.display import display, HTML


class URLString(str):
    """A subclass of strings that displays urls as links in ipython"""

    def _ipython_display_(self):
        url = str(self)
        return display(HTML(f"<a href='{url}'>{url}</a>"))


class DisplaysUrl(abc.ABC):
    """Mixin class that displays urls"""

    @abc.abstractmethod
    def _get_url(self) -> str:
        pass

    @property
    def url(self) -> Union[URLString, str]:
        """Get the URL for results (as defined by the subclass) to view it via web browser in the SiaSearch frontend

        Returns:
            The URL corresponding to the results
        """
        url = self._get_url()
        if url is not None:
            return URLString(url)
        return "No url can be generated from tags, only queries"
