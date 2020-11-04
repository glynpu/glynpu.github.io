---
layout: post
title: 智能指针的引用计数
date:   2020-11-01 23:05:00 +0800
<!-- categories: 他山之玉 -->
tag: c++
---

结论：  
	1. 引用不会增加shared_ptr的计数  
	2. 返回值是引用，如果接受的变量不是引用，而是对应类型的变量，则相当于用函数返回值的引用直接对变量进行赋值。引用计数加1  

代码：

```
#include <iostream>
#include <memory>
using namespace std;
class Student {
 public:
  void func(){};
};

const std::shared_ptr<Student>& func(std::shared_ptr<Student>& a) {
  cout << a.use_count() << endl;
  auto pa = a;
  cout << "in func: " << a.use_count() << endl;
  return a;
}

std::shared_ptr<Student>& foo(std::shared_ptr<Student>& a) { return a; }

int main() {
  std::shared_ptr<Student> s(new Student());

  const std::shared_ptr<Student>& pa = func(s);
  // 报 no matching member function call to 'reset'
  // 因为pa 是一个const 引用, 不能修改
  /* pa.reset(new Stuent()); */
  /* 如果返回值不是const, 则可以修改, 如下所示 */
  /* auto pc = foo(s); */
  /* pc.reset(new Student()); */

  // pa 是s的引用，计数不会增加
  cout << "s.use_count(): " << s.use_count() << endl;
  cout << "pa.use_count(): " << pa.use_count() << endl;

  std::shared_ptr<Student> pc = func(s);
  cout << "pa.use_count(): " << pa.use_count() << endl;
  cout << "pc.use_count(): " << pc.use_count() << endl;
  pc.reset(new Student());
  cout << "pa.use_count(): " << pa.use_count() << endl;
  cout << "pc.use_count(): " << pc.use_count() << endl;

  return 0;
}

```


输出:
```
1
in func: 2
s.use_count(): 1
pa.use_count(): 1
1
in func: 2
pa.use_count(): 2
pc.use_count(): 2
pa.use_count(): 1
pc.use_count(): 1
```

