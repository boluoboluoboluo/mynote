#### 概述

```sh
pip install numpy	# python 安装 numpy 库
```

| 核心模块                     | 主要包含的内容                                               | 核心作用                                                     |
| ---------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **N维数组对象 (`ndarray`)**  | 数组的形状（Shape）、数据类型（dtype）、维度（ndim）。       | 提供了一种连续内存、同质数据的快速存储结构。                 |
| **数组创建与操作**           | `np.array`, `np.zeros`, `np.ones`, `np.arange`, 切片（Slicing）、变形（Reshape）。 | 高效地生成各类矩阵，并进行数据抽取和重构。                   |
| **通用函数 (`ufunc`)**       | 元素级运算，如四则运算、三角函数（`np.sin`, `np.cos`）、对数指数（`np.log`）。 | 避免写 Python 循环，利用 **向量化（Vectorization）** 实现批量高速计算。 |
| **广播机制 (Broadcasting)**  | 不同形状（Shape）的数组之间进行算术运算的底层规则。          | 让非同阶矩阵也能巧妙结合计算，极大节省内存。                 |
| **线性代数 (`np.linalg`)**   | 矩阵点积（Dot Product）、求逆（Inverse）、特征值与特征向量、行列式。 | 支撑起机器学习算法（如线性回归、PCA降维）的底层数学。        |
| **随机数生成 (`np.random`)** | 正态分布、均匀分布、随机抽样、打乱顺序。                     | 广泛用于统计模拟、数据增强、机器学习初始化。                 |
| **统计与聚合函数**           | 最大值/最小值（`max`/`min`）、平均值（`mean`）、中位数（`median`）、标准差（`std`）。 | 快速计算一整组数据的宏观特征。                               |

#### 示例

| 表达式                       | 数组维度 (`ndim`) | 形状 (`shape`) | 计算机视角                            | 数学视角                   |
| :--------------------------- | ----------------- | -------------- | ------------------------------------- | -------------------------- |
| **`np.array([[10,20,30]])`** | **2维**           | `(1, 3)`       | **2D 表格**（只有1行3列的矩阵）       | **行向量 **                |
| **`np.array([10, 20, 30])`** | **1维**           | `(3,)`         | **1D 数组**（只有一排数字，不分横竖） | **纯向量 (Rank-1 Tensor)** |

```sh
# 示例说明:
虽然它们在底层内存中都存储为连续的 3 个数字 [10, 20, 30]，但它们的'元数据（Metadata）'控制台完全不同
# [[10, 20, 30]] 的元数据:
Shape = (1, 3)：明确告诉 NumPy，'我有 2 个坐标轴（轴0和轴1）。轴0的长度是 1（1行），轴1的长度是 3（3列）'
Strides = (24, 8)（假设是 int64）：'要移动到下一行需要跳过 24 字节，移动到下一列需要跳过 8 字节'

# [10, 20, 30] 的元数据:
Shape = (3,)：明确告诉 NumPy，'我只有 1 个坐标轴（轴0），长度是 3。我没有第二维，我也根本不知道什么是行、什么是列'
Strides = (8,)：'移动到下一个元素只需跳过 8 字节'
```



#### 生成

```py
# 导入 library
import numpy as np
# 画图工具
import matplotlib.pyplot as plt

#=========================
# 列表或元组创建
t = np.array([1,2,3])
print(t[1])
t = np.array((1.1, 2.2))
# 指定数据类型
t = np.array([1, 2, 3], dtype=np.float16)
# 如果指定了 dtype，输入的值都会被转为对应的类型，而且不会四舍五入
lst = [
    [1, 2, 3],
    [4, 5, 6.8]
]
t = np.array(lst, dtype=np.int32)
# 转换而不是上面的创建，其实是类似的，无须过于纠结
np.asarray((1,2,3))
#=========================
# 使用 arange 生成 	(序列生成器)
# 在 reshape 时，目标的 shape 需要的元素数量一定要和原始的元素数量相等。
t = np.arange(12).reshape(3, 4)
print(t)
print(t[0])
print(t[1][1])
np.arange(100, 124, 2).reshape(3, 2, 2)
np.arange(100., 124., 2).reshape(2,3,4)		# 浮点数
#=========================
# 使用 ones/zeros 创建	(创建全 1/0 array 的快捷方式) 默认是 float 类型
np.ones(3)
np.ones((2, 3))
np.zeros((2,3,4))
# 像给定向量那样的 0 向量（ones_like 是 1 向量）
np.zeros_like(np.ones((2,3,3)))

```

```py
import numpy as np

# 使用 linspace/logspace 生成
# 3 个参数：开头，结尾，数量；后者需要额外传入一个 base，它默认是 10
np.linspace(0, 9, 10).reshape(2, 5)		# 线性
np.linspace(0, 9, 6).reshape(2, 3)
# 指数 base 默认为 10
np.logspace(0, 9, 6, base=np.e).reshape(2, 3)
# _ 表示上（最近）一个输出
# logspace 结果 log 后就是上面 linspace 的结果
np.log(_)

#=========================
# 使用 random 生成
# 新的 API 方式: 即通过 np.random.default_rng() 先生成 Generator
# 0-1 连续均匀分布
np.random.rand(2, 3)	
# 单个数
np.random.rand()
# 0-1 连续均匀分布
np.random.random((3, 2))
# 指定上下界的连续均匀分布
np.random.uniform(-1, 1, (2, 3))
# 不过从 1.17 版本后推荐这样使用（以后大家可以用新的方法）
# rng 是个 Generator，可用于生成各种分布
rng = np.random.default_rng(42)
t = rng.random((2, 3))
print(t)
# 可以指定上下界，所以更加推荐这种用法
rng.uniform(0, 1, (2, 3))
# 随机整数（离散均匀分布），不超过给定的值（10）
np.random.randint(10, size=2)
# 随机整数（离散均匀分布），指定上下界和 shape
np.random.randint(0, 10, (2, 3))
# 上面推荐的方法，指定大小和上界
rng.integers(10, size=2)
# 标准正态分布
np.random.randn(2, 4)
# 上面推荐的标准正态分布用法
rng.standard_normal((2, 4))
# 高斯分布
np.random.normal(0, 1, (3, 5))
# 上面推荐的高斯分布用法
rng.normal(0, 1, (3, 5))
```

#### 尺寸相关

```py
import numpy as np

arr = np.random.rand(2, 3)
# 维度，array 是二维的（两个维度）
arr.ndim
# 形状，返回一个 Tuple
arr.shape
# 数据量
arr.size

```

#### 最值分位

```py
# 所有元素中最大的
arr.max()
# 按维度（列）最大值
arr.max(axis=0)
# 同理，按行
arr.max(axis=1)

# 是否保持原来的维度
# shape 是 (3,1)，array 的 shape 是 (3,4)，按行，同时保持了行的维度
arr.min(axis=1, keepdims=True)
# 保持维度：（1，4），原始array是（3，4）
arr.min(axis=0, keepdims=True)
# 一维了
arr.min(axis=0, keepdims=False)
# 另一种用法，不过我们一般习惯使用上面的用法，其实两者一回事
np.amax(arr, axis=0)
# 同 amax
np.amin(arr, axis=1)

# 中位数
# 其他用法和 max，min 是一样的
np.median(arr)
# 分位数，按列取1/4数
np.quantile(arr, q=0.25, axis=0)
# 分位数，按行取 3/4，同时保持维度
np.quantile(arr, q=0.75, axis=1, keepdims=True)
```

#### 平均求和标准差

```py
# 平均值
np.average(arr)
# 按维度平均（列）
np.average(arr, axis=0)
# 求和，不多说了，类似
np.sum(arr, axis=1)
np.sum(arr, axis=1, keepdims=True)
# 按列累计求和
np.cumsum(arr, axis=0)
# 按行累计求和
np.cumsum(arr, axis=1)
# 标准差，用法类似
np.std(arr)
# 按列求标准差
np.std(arr, axis=0)
# 方差
np.var(arr, axis=1)
```

#### 形状和转换

```py
# 换个整数的随机 array
rng = np.random.default_rng(seed=42)
arr = rng.integers(1, 100, (3, 4))

# 有时候您可能需要将多维 array 打平
arr.ravel()
arr.shape
# 扩展 1 个维度，需要（必须）指定维度
# 其实就是多嵌套了一下
np.expand_dims(arr, 1).shape
# 扩充维度
expanded = np.expand_dims(arr, axis=(1, 3, 4))
expanded.shape

# 如果指定了维度，那就只会去除该维度，指定的维度必须为 1
np.squeeze(expanded, axis=1).shape
# 去除所有维度为 1 的
np.squeeze(expanded).shape

# reshape 成另一个形状
# 也可以直接变为一维向量
arr.reshape(2, 2, 3)
# 可以偷懒，使用 -1 表示其他维度（此处 -1 为 3），注意，reshape 参数可以是 tuple 或连续整数
arr1 = arr.reshape((4, -1))

# 另一种变换形状的方式 —— 原地变换
# 不过不能用-1
# 另外 resize 不一定和原来的元素数量一样多
arr2 = arr.resize((4, 3))
# 注意：上面的 reshape 会生成一个新的 array，但 resize 不会，所以我们需要用原变量名将它显示出来
# arr2 没有值

# 可以copy一份
arrcopy = np.copy(arr)
arrcopy.resize((2, 3))

# 也可以将 refcheck 设为 False
# 此时 arr 会发生变化
# 元素数量超出时，截断；元素数量不够时，0填充
arr.resize((2,3), refcheck=False)

# 如果用 np.resize 会略有不同
# 元素数量不够时，会自动复制
np.resize(arr, (5, 3))
# 元素数量多出来时，会自动截断
np.resize(arr, (2, 2))
```

#### 反序

```py
# 默认列反序
arr[::-1]
# 列不变行反序
arr[::-1, :]
# 在不同维度上操作：行不变列反序
arr[:, ::-1]
# 行变列也变
arr[::-1, ::-1]
```

#### 转置

```py
# 建议二维矩阵用 arr.T（会快很多），超过二维的张量可以用 np.transpose，会更加灵活

# 一维 (一维数组转置还是自己)
np.array([1,2]).T.shape
# 简便用法，把所有维度顺序都给倒过来
arr.T
# 将 shape=(1,1,3,4) 的转置后得到 shape=(4,3,1,1)
arr.reshape(1, 1, 3, 4).T.shape

# 这种转置方式可以指定 axes
np.transpose(arr)
# 不指定 axes 时和 .T 是一样的
np.transpose(arr.reshape(1, 2, 2, 1, 3, 1)).shape
```

#### 切片和索引

```py
# 取第 0 行
arr[0]
# 取第 0 行第 1 个元素
arr[0, 1]
# 然后带点范围 第 0-2 行
arr[0:3]
# 离散也可以：第 00，3 行
arr[[0, 3]]
# 再来加上维度：第 1-2 行，第 1 列
arr[1:3, 1]
# 离散也是一样：第 1，3 行，第 0 列
arr[[1,3], [0]]
# 还可以有简写：到最后或到开始。如第 3 行到最后一行
arr[3:]
# 开始到第 3 行，第 1-3 列
arr[:3, 1:3]
# 还可以来点跳跃，步长：start:stop:step，第 1 行到第 4 行，间隔为 2，即第 1、3 行
arr[1: 4: 2]
# 第一列的值，其实是所有其他维度第 1 维的值
arr[...,1]
# 与上面类似，但用的更多
arr[:,1]
```

#### 拼接

```py
# 默认沿axis=0（列）连接
np.concatenate((arr1, arr2))	# 行数增加
# 沿 axis=1（行）连接
np.concatenate((arr1, arr2), axis=1) # 列数增加

# 竖直按行顺序拼接
np.vstack((arr1, arr2))		# 相当于上面 axis=0
# 水平按列顺序拼接
np.hstack((arr1, arr2))		# 相当于上面 axis=1

# 堆叠，默认根据 axis=0 进行
np.stack((arr1, arr2))
```

#### 重复

```py
# 在 axis=0（沿着列）上重复 2 次
np.repeat(arr, 2, axis=0)
# 在 axis=1（沿着行）上重复 3 次
np.repeat(arr, 3, axis=1)
```

#### 分拆

```py
# 默认切分列（axis=0），切成 3 份
np.split(arr, 3)
# （axis=1）切分行
np.split(arr, 2, axis=1)
# 和上面的一个效果
np.vsplit(arr, 3)
# 等价的用法
np.hsplit(arr, 2)
```

#### 条件筛选

```py
# 返回满足条件的索引，因为是两个维度，所以会返回两组结果
np.where(arr > 50)
# 不满足条件的赋值，将 <=50 的替换为 -1
np.where(arr > 50, arr, -1)
```

#### 提取

```py
# 提取和唯一值返回的都是一维向量。

# 提取指定条件的值
np.extract(arr > 50, arr)
# 唯一值，是另一种形式的提取
np.unique(arr)
```

#### 抽样

```py
rng = np.random.default_rng(42)
# 第一个参数是要抽样的集合，如果是一个整数，则表示从 0 到该值
# 第二个参数是样本大小
# 第三个参数表示结果是否可以重复
# 第四个参数表示出现的概率，长度和第一个参数一样

# 由于（0 1 2 3）中 2 和 3 的概率比较高，自然就选择了 2 和 3
rng.choice(4, 2, replace=False, p=[0.1, 0.2, 0.3, 0.4])

# 旧的 API
# 如果是抽样语料的 index，更多的方法是这样：
data_size = 10000
np.random.choice(data_size, 50, replace=False)
```

#### 最值 Index

```py
# 按列（axis=0）最大值的 Index
np.argmax(arr, axis=0)
# 按行（axis=1）最小值的 Index
np.argmin(arr, axis=1)

# 默认按行（axis=1）排序的索引
np.argsort(arr)
# 数据按行（axis=1）排序的索引，同上
np.argsort(arr, axis=1)
```

#### 算术

```py
# +-*/ 四则运算，就跟两个数字计算一样
arr * 2
# 平方也可以
arr ** 2
# 开方
np.sqrt(arr)
# log
np.log(arr)
# 超过5的都换成5
np.minimum(arr, 5)
# 低于5的都换成5
np.maximum(arr, 5)
# 四舍五入
np.round(np.sqrt(arr), 2)
# floor/ceil
np.floor(np.sqrt(arr))
np.ceil(np.sqrt(arr))
# mod <=> x % 3
np.mod(arr, 3)
# 还可以使用多个被除数
np.mod(arr, arr-5)
```

#### 广播

```py
# 广播，后面的被当做 1 行 4 列
a + [1,2,3,4]
# 或者这样广播，后面的被当做 3 行 1 列
a + [[1], [2], [3]]
```

#### 矩阵

```py
# 乘法 = 点积 = 内积

# array 乘法
np.dot(a, b)
# 或者这样乘
a.dot(b)

# 矩阵乘法
# 与 dot 的主要区别是：matmul 矩阵（好像元素一样）堆叠在一起广播
np.matmul(a, b)
# 同上，写起来比较好看的方法
a @ b

# 点积
np.vdot(a, a)
# 对，就是点积
np.sum(a*a)

# 内积
np.inner(a, a)
# 对，就是内积
a.dot(a.T)
===================

# 行列式
np.linalg.det(c)

# 逆矩阵（方阵）
np.linalg.inv(c)
```

