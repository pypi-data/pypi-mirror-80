※下の方に日本語の説明があります

## English description
This package provides a simple output of python objects.

How to use

```python
from sout import sout

large_obj = [{j:"foo" for j in range(i+2)}
  for i in range(1000)]
sout(large_obj)
```

output
```python
[
  {0: "foo", 1: "foo"},
  {0: "foo", 1: "foo", 2: "foo"},
  {0: "foo", 1: "foo", 2: "foo", 3: "foo"},
  {
    0: "foo",
    1: "foo",
    2: "foo",
    3: "foo",
    4: "foo"
  },
  {
    0: "foo",
    1: "foo",
    2: "foo",
    3: "foo",
    4: "foo",
    ... (all_n = 6)
  },
  ... (all_n = 1000)
]
```

## 日本語の説明
オブジェクトをわかりやすく表示するためのパッケージです

簡単な使い方
```python
from sout import sout

large_obj = [{j:"foo" for j in range(i+2)}
  for i in range(1000)]
sout(large_obj)
```

出力結果
```python
[
  {0: "foo", 1: "foo"},
  {0: "foo", 1: "foo", 2: "foo"},
  {0: "foo", 1: "foo", 2: "foo", 3: "foo"},
  {
    0: "foo",
    1: "foo",
    2: "foo",
    3: "foo",
    4: "foo"
  },
  {
    0: "foo",
    1: "foo",
    2: "foo",
    3: "foo",
    4: "foo",
    ... (all_n = 6)
  },
  ... (all_n = 1000)
]
```
