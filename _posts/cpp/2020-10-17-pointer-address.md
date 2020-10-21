---
layout: post
title: c++ 单一对象可能拥有一个以上的地址
date:   2020-10-17 23:05:00 +0800
<!-- categories: 他山之玉 -->
tag: c++
---

在effective c++ 书中第118页，条款27 尽量少做转型动作 指出，c++中一个对象可能有多个地址，
验证代码示例如下：

```
#include <iostream>

using namespace std;
class Person {
 public:
  int age;
};

class Runner {
 public:
  int speed = 0;
};

class Student : public Person, public Runner {
 public:
  virtual void get_score() { cout << "Student rate function"; }

 private:
  int grade;
};

int main() {
  Student s;
  Person *p = &s;
  Runner *sr = &s;
  cout << &s << endl;
  cout << p << endl;
  cout << sr << endl;
}

```

程序输出为:

```
0x7ffee42b9580
0x7ffee42b9588
0x7ffee42b958c
```
