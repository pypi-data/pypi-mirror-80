# Contributing instructions 

## What is mixins and how to use it?
The idea with a mixin is a class that is never instantiated on it's own and adds functionality to a class.   
 
The pattern is usually: "If my baseclass has implemented methods x, y, z, then a mixin adds functionality i, j, k".   
In this case it's "if a class has implemented `get_url` `DisplaysUrl` adds `display_url` to the class. 
Then when creating a new class it's like a checklist of things it can do via mixins (I'm just making up some random mixins) e.g.

```python
class MyNewClass(DisplaysUrl, PrintsAllAttributes, ...): ...
```

They are easy to add/remove and should be de-coupled from each class i.e. the class can do it's job without it.
  
`Mixin` is never initialized on it's own, it's always just providing a small set of functionality to the other class 
and that it's not a parent class, it only connects loosely with what the subclass does. 
E.g. the difference in connection between a `car` and a `truck` vs. the connection between `car` and `print_attributes`. 

If you have a parent class you pull in all the methods of the parent 
whether you are interested or not while a `mixin` is usually confined to a single simple purpose

## How does packaging work?

To make `siasearch` package available in your python environment we make it pip-compatible.  
To let pip register our package we have to add `setup.py` file with package details, 
you can read more about it [here](https://packaging.python.org/tutorials/packaging-projects/#creating-setup-py)  
