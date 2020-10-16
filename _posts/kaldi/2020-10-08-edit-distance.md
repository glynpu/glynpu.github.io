---
layout: post
title:  编辑距离python 版本
date:   2020-10-08 23:05:00 +0800
<!-- categories: 他山之玉 --> 
tag: kaldi
---

重点:
1. 距离矩阵的维度是reference/test的长度加1
2. 距离矩阵的初始化
3. 三个方向的递推(初始化是递推的边界条件)

```
def cal_cer(reference, test):
    dr = len(reference) + 1
    dt = len(test) + 1
    distance = [[0 for col_index in range(dr)] for row_index in range(dt)]

    # init distance
    for col_index in range(dr):
        distance[0][col_index] = col_index
    for row_index in range(dt):
        distance[row_index][0] = row_index

    # calculate cer with dynamic programming
    for col_index in range(dr - 1):
        for row_index in range(dt - 1):
            ins_error = distance[row_index][col_index + 1] + 1
            del_error = distance[row_index + 1][col_index] + 1
            equality = 0 if reference[col_index] == test[row_index] else 1
            sub_error = distance[row_index][col_index] + equality
            distance[row_index + 1][col_index + 1] = min(
                del_error, ins_error, sub_error)
    return distance[-1][-1]


def main():
    assert 2 == cal_cer("hello", "heel")
    assert 3 == cal_cer("hello", "he")
    assert 5 == cal_cer("hello", "aahe")


if __name__ == '__main__':
    main()
```

上面函数思路为为一个状态会有三个进入状态  
下面实现思路为一个状态会有三个跳出状态

```
def cal_cer(reference, test):
    dist = [[(len(reference) + len(test)) * 2 for _ in range(len(reference) + 1) ] for _ in range(len(test) + 1)]
    # print(dist)
    dist[0][0] = 0
    for row_index in range(0,len(reference)):
        for col_index in range(0,len(test)):
            # print("{} {}".format(row_index, col_index))
            dist[col_index+1][row_index] = min(dist[col_index+1][row_index], dist[col_index][row_index] + 1)
            dist[col_index][row_index + 1] = min(dist[col_index][row_index+1], dist[col_index][row_index] + 1)
            equality = 0 if reference[row_index] == test[col_index] else 1
            dist[col_index + 1][row_index+1] = min(dist[col_index + 1][row_index+1], dist[col_index][row_index] + equality)
    for col_index in range(0,len(test)):
        dist[col_index+1][len(reference)] = min(dist[col_index+1][len(reference)], dist[col_index][len(reference)] + 1)
    for row_index in range(0,len(reference)):
        dist[len(test)][row_index + 1] = min(dist[len(test)][row_index+1], dist[len(test)][row_index] + 1)

    return dist[-1][-1]


def main():
    d = cal_cer("hello", "heel")
    print(d)
    assert 2 == cal_cer("hello", "heel")
    assert 3 == cal_cer("hello", "he")
    assert 5 == cal_cer("hello", "aahe")


if __name__ == '__main__':
    main()


```
