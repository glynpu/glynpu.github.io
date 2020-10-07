src = 'http://homepage.ntu.edu.tw/~karchung/miniconversations/'
with open('resource.txt', 'r') as f:
    for line in f:
        s = line.split()
        for w in s:
            if ('mp3' in w):
                w = w.replace('href=', '')
                w = w.replace('\"', '')

                print(src + w)
        # print(line)
