# htmlcomparator

This is a light-weight python package used to compare two html files and return the differences. 

The users can choose whether they want a boolean result or string result that specify the difference. They can also choose the types of differences they want to receive. 

## Usage

To start using the comparator, first import the package, and make an object.

```python
from htmlcomparator import HTMLComparator
comparator = HTMLComparator()
```
The method that is used to compare html code is 
```python
comparator.compare(html1, html2, quick_compare = True, compare_type = "all")
```

```html1, html2``` are the two html to be compared. If they are both strings, it will treat them as two html strings. If they are both ```io.IOBase``` objects, then the program will treat them as two opened files. Otherwise the program will raise a ```TypeError```.

```quick_compare``` argument is used to specify whether the user want the method to simply return boolean or to return a detailed information of the differences. If it is set to True, then the method will return False as soon as it encounters the first difference, and return True if there are no difference. If it is set to False, then the two html are compared thoroughly, and the method will return a ```string``` to describe the differences. If there are no differences, it will return an empty string.

```compare_type``` argument is used to specify the type of differences to compare. It is ignored if ```quick_compare``` is set to ```True```. If it is set to ```tag```, then only tag differences will be returned. If it is set to ```data``` then tag and data differences will be returned. If it is set to ```all```, then all differences will be considered, including tags, data, and attributes.

For example, 
```python
s1 = "<!DOCTYPE xml> <head> <p> test </p> <p> different here </p> </head>"
s2 = "<!DOCTYPE html> <head> <p> this is different </p> </head>"
comparator = HTMLComparator()
print(comparator.compare(s1,s2, compare_type = "all", quick_compare = False))
```
will output:
```
@@ DOCTYPE Difference @@
*DOCTYPE xml
-DOCTYPE html

extra tag <p> in the first html at (1, 36)

@@ (1, 25) , (1, 26) @@
*test
-this is different
```
The tuples ```(1, 36)```, ```(1, 25)```, and ```(1, 25)``` give the line number and the offset of the differences.

## Limitations

Currently doesn't support CSS.

## License

Copyright Mengjia Zhao 2020.
Distributed under the terms of the [Apache 2.0 license](https://github.com/in-the-ocean/htmlcomparator/blob/master/LICENSE).
