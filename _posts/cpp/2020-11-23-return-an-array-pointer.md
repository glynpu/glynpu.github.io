---
layout: post
title: 函数返回array pointer和右左规则
date:   2020-11-21 19:05:00 +0800
tag: c++
---

代码：

```
#include <iostream>

typedef int (*(*func1)(const int *const p))[5];
using func2 = int (*(*)(const int *const p))[5];
using arrT = int[5];

int a[5] = {1, 2, 3, 4, 5};

// Solution1: using type alias
arrT *increase1(const int *const b) {
  for (auto &i : a) {
    i += *b;
  }
  // equivalent to following logic
  // for (int i = 0; i < 5; ++i) {
  //   a[i] += *b;
  // }
  return &a;
}

// Solution2: define a function directly
int (*increase2(const int *const b))[5] {
  for (auto &i : a) {
    i += *b;
  }
  return &a;
}

// Solution3: trailing return type
auto increase3(const int *const b) -> int (*)[5] {
  for (auto &i : a) {
    i += *b;
  }
  return &a;
}

int main() {
  int x = 10;
  func1 f1 = increase1;
  f1(&x);
  func1 f2 = increase2;
  f2(&x);
  func1 f3 = increase3;
  f3(&x);
  func2 f4 = increase1;
  f4(&x);
  for (const auto &i : a) {
    std::cout << i << std::endl;
  }
  return 0;
}

```


输出结果为:

```
41
42
43
44
45
```
