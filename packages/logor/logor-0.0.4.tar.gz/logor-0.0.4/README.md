# Logor

A Log Stream Framework. it's easy to replace the native module `logging`:  
```python
import logging

logger = logging.getLogger(__name__)
```
and you can do like this:
```python
import logor

logger = logor.getLogger(__name__)
```
if you are familiar with go-logrus, you can use it:
```python
import logor

logger = logor.withFields({
    "MODULE": __name__,
    "ENV": "DEV",
})
```
