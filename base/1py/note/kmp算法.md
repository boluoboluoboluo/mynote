

#### KMP算法是什么？

KMP算法的全称是Knuth-Morris-Pratt算法，是一种高效的字符串匹配算法，用于在一个主串（文本串）S中查找子串（模式串）P的位置。它的核心优势是：时间复杂度为 O(n + m)（n 是主串长度，m 是模式串长度），并且在匹配过程中不会回溯主串的指针，避免了暴力匹配的低效（暴力匹配最坏情况下是 O(n × m)）。

KMP的核心：next数组（也叫部分匹配表、失败函数）KMP算法的关键是一个叫 next数组（或π数组）的预处理表。

- next[i] 表示：对于模式串P[0...i] 这个前缀，当它和主串失配时，应该把模式串滑动到哪个位置继续匹配。
- 更精确地说：next[i] 是 P[0...i] 这个字符串的最长真前缀，它同时也是真后缀的长度。

例如，模式串 P = "ababac"

解释：

- P[0...2] = "aba" → 最长相等的前缀后缀是 "a"，长度1 → next[2]=1
- P[0...3] = "abab" → 最长相等的前缀后缀是 "ab"，长度2 → next[3]=2
- P[0...4] = "ababa" → 最长相等的前缀后缀是 "aba"，长度3 → next[4]=3
- P[0...5] = "ababac" → 没有更长的，失配后回到0 → next[5]=0

#### **KMP匹配过程（伪代码）**

1. 先预计算模式串P的 next 数组。
2. 初始化 i=0（主串指针），j=0（模式串指针）
3. 遍历主串：

```py
while i < len(S):
    if S[i] == P[j]:      # 匹配成功
        i += 1
        j += 1
    if j == len(P):       # 找到完整匹配
        return i - j      # 返回起始位置
    elif i < len(S) and S[i] != P[j]:  # 失配
        if j != 0:
            j = next[j-1]  # 模式串跳到next位置
        else:
            i += 1         # j已经在0，只能主串前进
```

#### 代码

```py
def compute_next(P):
    m = len(P)
    next = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and P[i] != P[j]:
            j = next[j-1]
        if P[i] == P[j]:
            j += 1
        next[i] = j
    return next

def kmp_search(S, P):
    n, m = len(S), len(P)
    if m == 0: return 0
    next = compute_next(P)
    j = 0
    for i in range(n):
        while j > 0 and S[i] != P[j]:
            j = next[j-1]
        if S[i] == P[j]:
            j += 1
        if j == m:
            return i - m + 1  # 找到匹配位置
            j = next[j-1]     # 继续找下一个（可选）
    return -1  # 未找到
```

#### 补充

```py
# 计算模式串p的所有子串的步长,返回步长数组next
# 步长:最长相等的前缀后缀的长度,举例:假设模式串为ababac:
# 	a 	=>								next[0]=0
# 	ab 	=> 最长相等前缀后缀: 无 			 next[1]=0 		#如果是 aa 则next[1]=1 
# 	aba => 最长相等前缀后缀: a 	长度1 	next[2]=1
# 	abab =>最长相等前缀后缀: ab 	长度2	next[3]=2
# 	ababa =>最长相等前缀后缀: aba 长度3	next[4]=3
# 	ababac =>最长相等前缀后缀: 无 		 next[5]=0
def compute_next(p):
	m = len(p)
	next = [0] * m	#初始化步长数组,为模式串p长度
	j = 0 	#当前匹配的从串指针,0开始
	for i in range(1,m):	#遍历,i:主串指针,从1开始
		#j往前移1位,然后查找next[j-1]子串的最长相等前缀后缀长度,将j偏移到这个位置,然后与p[i]比较
		#如果不相等,继续上面步骤,直到相等,或者j=0为止				
		while True:
			if j == 0:
				break
			if p[i] != p[j]:	#如果不相等
				j = next[j-1]
			else:
				break
		#如果相等,意味着匹配到的前缀多了1位,即最长相等前缀后缀: j+1
		if p[i] == p[j]:		
			j += 1 		#指针向前移动1位,准备下一轮匹配
		
		next[i] = j #当子串长度为i时,最长相等前缀后缀为j
    return next
```

