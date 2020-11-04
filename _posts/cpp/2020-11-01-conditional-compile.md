---
layout: post
title: 条件编译
date:   2020-11-01 23:05:00 +0800
<!-- categories: 他山之玉 -->
tag: c++
---

代码：

```
#include <iostream>
using namespace std;

// 可以在代码里定义, 也可以编译时外部传入
#define FLAG1

int main() {
  cout << "first line of main" << endl;
#ifdef FLAG1
  cout << "controled by FLAG1" << endl;
#endif
#ifdef FLAG2
  cout << "controled by FLAG2" << endl;
#endif
  // flag 可以是大写也可以是小写，不过通常选择大写
#ifdef flag3
  cout << "controled by flag3" << endl;
#endif
  // 注意flag4用的是 if-n-def, 中间有个n
#ifndef flag4
  cout << "controled by flag4" << endl;
#endif
  return 0;
}

```

编译指令:
```
g++ main.cc -o main
./main

```

输出：
```
first line of main
controled by FLAG1
controled by flag4

```
编译指令：
```
g++ main.cc -o main  -D flag4
./main
```

输出：
```
first line of main
controled by FLAG1

```


编译指令：

```
g++ main.cc -o main -D FLAG2 -D flag3
./main

```

输出：
```
first line of main
controled by FLAG1
controled by FLAG2
controled by flag3
controled by flag4
```


