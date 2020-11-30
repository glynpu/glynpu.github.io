---
layout: post
title: 指针的引用与链表逆序
date:   2020-11-01 23:05:00 +0800
<!-- categories: 他山之玉 -->
tag: c++
---

结论：  
	1. 指针的引用

代码：

```
#include <iostream>
struct Node {
  int value1;
  int value2;
  Node *pnext = NULL;
};

void show(Node *p) {
  while (p) {
    std::cout << p->value1 << " " << p->value2 << std::endl;
    p = p->pnext;
  }
  std::cout << std::endl;
}

void invert(Node *&h) {
  // a wrong function declarication
  // void invert(Node *h) {

  // reb: right_end_bridge
  Node *reb;
  // only one node
  if (!h->pnext) {
    return;
  }
  reb = h->pnext;
  // only two node
  if (!reb->pnext) {
    reb->pnext = h;
    h = reb;
    return;
  }
  // three or more nodes
  Node *leb = h;
  reb = h->pnext;
  Node *p = reb->pnext;
  leb->pnext = NULL;
  while (p) {
    reb->pnext = leb;
    leb = reb;
    reb = p;
    p = reb->pnext;
  }
  reb->pnext = leb;
  h = reb;
  return;
}
int main() {

  Node *h = new Node();
  Node *p = h;

  for (int i = 0; i < 10; ++i) {
    if (i > 0) {
      p->pnext = new Node();
      p = p->pnext;
    }

    p->value1 = i;
    p->value2 = i * i;
  }
  p->pnext = NULL;
  p = h;

  show(h);
  invert(h);
  show(h);

  return 0;
}

```


输出:
```
0 0
1 1
2 4
3 9
4 16
5 25
6 36
7 49
8 64
9 81

9 81
8 64
7 49
6 36
5 25
4 16
3 9
2 4
1 1
0 0
```

