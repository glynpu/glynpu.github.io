---
layout: post
title: container迭代器失效的问题
date:   2019-05-21 23:05:00 +0800
<!-- categories: 他山之玉 -->
tag: c++
---

不同编译器的迭代器失效时机好像还不太一样，研究一下map是怎么实现红黑树的

```
#include<iostream>
#include<map>
using namespace std;
void print(map<int, int> &m) {
	map<int, int>::iterator it;
	for(it = m.begin(); it != m.end(); ++it) {
		cout << it->first << " " << it->second << endl;
	}
}

void deletevalue(map<int, int> &m, int target) {
	for(map<int, int>::iterator it = m.begin(); it!=m.end(); ++it) {
		if(it->first > target) {
			m.erase(it->second * 2);
			m.erase(it);
		}
	}
}
void mapTest()
{
    map<int, int>m;
    for (int i = 0; i < 10; i++)
    {
        m.insert(make_pair(i, i + 1));
    }
    map<int, int>::iterator it;
	deletevalue(m, 3);
	print(m);

}
int main()
{
    mapTest();
    /* system("pause"); */
    return 0;
}
```

采用g++ 5.4.0 on linux,输出为:  
```
0 1
1 2
2 3
3 4
```
采用g++ 4.2.1 on mac os,输出为:  
```
0 1
1 2
2 3
3 4
5 6
6 7
8 9
```
