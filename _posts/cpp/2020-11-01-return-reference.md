---
layout: post
title: 函数返回引用
date:   2020-11-01 23:05:00 +0800
<!-- categories: 他山之玉 -->
tag: c++
---

代码：

```
#include <iostream>
using namespace std;

int& increase_one(int& a) {
  ++a;
  return a;
}

int main() {
  int a = 10;
  // 虽然increase_one的返回值是引用，但是b 的类型不是
  // 该语句等效于，
  // 	1. 定义一个int 类型的变量 b
  //	2. 用increase_one(a) 的返回值给 b 赋值。
  // 所以b 和 a 不共享内存，修改b 不会改变a的值
  int b = increase_one(a);
  cout << "b: " << b << endl;
  b = 15;
  cout << "b: " << b << endl;
  // a 并不会随着b的更改而更改
  cout << "a: " << a << endl;

  int& c = increase_one(a);
  // c 的类型是引用，c 改为多少，a的值就是多少
  c = 100;
  cout << "a: " << a << endl;
}

```


输出结果为:

```
b: 11
b: 15
a: 11
a: 100
```
