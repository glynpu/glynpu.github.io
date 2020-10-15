---
layout: post
title: c++ 虚函数表和函数指针
date:   2019-05-21 23:05:00 +0800
<!-- categories: 他山之玉 -->
tag: c++
---
目录：
1. 类的模版函数能不能是虚函数  
2. 模版类里可以不可以有虚函数  
3. 基类指针指向子类对象时，能不能调用子类新加的虚函数  


虚函数表是一个表，是表就有行有列。  
所以虚函数表不一定是一维的。  
如果类是多继承的，那么虚函数表就是二维的。  
如果是单继承，才是一维的。  


[为什么c++的member function template 不能是virtual的？](https://www.zhihu.com/question/60911582)
因为虚函数表没法填.

1. c++ 程序的编译和链接是分开的
2.  template函数会有多少个示例，只有编译完成之后才确定
3. c++ 编译生成虚函数表过程中就要确定有多少个虚函数. 
所以条件2和条件3是冲突的.
结论： 类的成员函数可以是模版函数，但该模版函数就不能再用virtual 修饰了


```
  #include <iostream>
  #include <string>

  using namespace std;
  class Person {
   public:
    // virtual cannot be specified on member function templates
    // template <typename T>
    // virtual void info() {
    //  cout << "info function" << endl;
    // }
    template <typename T>
    void info() {
     cout << "info function" << endl;
    }
  };

  int main() {
    Person p;
    p.info<int>();
  }

```

模版类的函数可以是虚函数：  

```
#include <iostream>
#include <string>

using namespace std;
template <typename T>
class Person {
 public:
  virtual void info(T a) { cout << "info function  virtual " << a << endl; }
};

int main() {
  Person<int> p;
  p.info(5);
}

```




任何妄图使用父类指针想调用子类中的未覆盖父类的成员函数的行为都会被编译器视为非法，所以，这样的程序根本无法编译通过。但在运行时，我们可以通过指针的方式访问虚函数表来达到违反C++语义的行为。（关于这方面的尝试，通过阅读后面附录的代码，相信你可以做到这一点）

```
#include <iostream>

using namespace std;

class Person {
 public:
  virtual void age() {
    cout << "person age func" << endl;
    return;
  }

  void nonvirtual_function() {
    cout << "person nonvirtual_function" << endl;
    return;
  }
};

class Student : public Person {
 public:
  virtual void age() {
    cout << "student age function" << endl;
    return;
  }
  virtual void score() {
    cout << "studnet score function" << endl;
    return;
  }

  virtual void grade() {
    cout << "studnet grad function" << endl;
    return;
  }

  void nonvirtual_function() {
    cout << "student nonvirtual_function" << endl;
    return;
  }
};
int main() {
  Student s;
  s.score();
  s.age();
  s.nonvirtual_function();
  cout << (long *)&s << endl;
  cout << *(long *)&s << endl;
  cout << (long *)*(long *)&s << endl;
  cout << (long *)*(long *)&s + 1 << endl;
  cout << (long *)*(long *)&s + 2 << endl;
  typedef void (*Func)(void);
  (((Func) * (long *)*(long *)&s))();
  (((Func) * (long *)*(long *)&s))();
  (((Func) * ((long *)*(long *)&s + 1)))();
  (((Func) * ((long *)*(long *)&s + 2)))();

  cout << endl << "invoke with Person pointer" << endl << endl;
  Person *p = &s;
  p->age();
  // error: 'class person' has no member names 'grade'
  // p->grade();
  // 如果非要用基类指针调用子类中新定义的virtual 函数，那么可以hack一下

  p->nonvirtual_function();
  (((Func) * ((long *)*(long *)p + 1)))();
  (((Func) * ((long *)*(long *)p + 2)))();

  printf("第一个虚函数地址:%p\n", (long *)*(long *)&s + 0);
  printf("第二个虚函数地址:%p\n", (long *)*(long *)&s + 1);

  return 0;
}
```
程序输出为:

```
studnet score function
student age function
student nonvirtual_function
0x7ffdbd702550
4198760
0x401168
0x401170
0x401178
student age function
student age function
studnet score function
studnet grad function

invoke with Person pointer

student age function
person nonvirtual_function
studnet score function
studnet grad function
第一个虚函数地址:0x401168
第二个虚函数地址:0x401170
```

[参考文献](https://blog.csdn.net/lyztyycode/article/details/81326699)
* content
{:toc}

