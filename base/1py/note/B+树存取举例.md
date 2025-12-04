

## B+树举例

以下是使用一个简单的学生数据表为例，说明 B+ 树如何实现数据的存储和读取操作的逐步解释：

------

### **1. 示例数据表**

假设有一个学生表 `students`，包含以下字段：

| 学号（主键） | 姓名 | 年龄 |
| :----------- | :--- | :--- |
| 3            | 张三 | 20   |
| 7            | 李四 | 21   |
| 10           | 王五 | 22   |
| 15           | 赵六 | 23   |
| 20           | 陈七 | 24   |
| 25           | 孙八 | 25   |

假设 B+ 树的每个节点最多存储 **3 个键值**，超过时需分裂。

------

### **2. B+ 树的存储过程**

#### **步骤 1：插入键值 3、7、10**

- 初始插入时，所有键值存储在同一个叶子节点中：

  ```
  叶子节点: [3, 7, 10] → 指向实际数据行（张三、李四、王五）
  ```

#### **步骤 2：插入键值 15**

- 叶子节点已满（最多 3 个键），触发分裂：

  - 原节点分裂为 `[3, 7]` 和 `[10, 15]`。

  - 中间键 `10` 提升到父节点（新建根节点）：

    ```
    根节点: [10]
      ├─ 左子节点（叶子）: [3, 7] → 张三、李四
      └─ 右子节点（叶子）: [10, 15] → 王五、赵六
    ```

#### **步骤 3：插入键值 20**

- 插入右子节点 `[10, 15]`，更新为 `[10, 15, 20]`（未满）：

  ```
  根节点: [10]
    └─ 右子节点（叶子）: [10, 15, 20] → 王五、赵六、陈七
  ```

#### **步骤 4：插入键值 25**

- 右子节点 `[10, 15, 20]` 已满，触发分裂：

  - 分裂为 `[10, 15]` 和 `[20, 25]`。

  - 中间键 `20` 提升到父节点，根节点更新为 `[10, 20]`：

    ```
    根节点: [10, 20]
      ├─ 左子节点（叶子）: [3, 7] → 张三、李四
      ├─ 中子节点（叶子）: [10, 15] → 王五、赵六
      └─ 右子节点（叶子）: [20, 25] → 陈七、孙八
    ```

------

### **3. B+ 树的读取操作**

#### **场景 1：精确查找学号 15**

1. **从根节点开始**：比较 `15` 与根节点键值 `[10, 20]`，发现 `10 ≤ 15 < 20`，进入中子节点 `[10, 15]`。
2. **在叶子节点中查找**：找到键值 `15`，返回对应数据行（赵六）。

#### **场景 2：范围查找学号 7 ≤ ID ≤ 20**

1. **定位起始键值 7**：
   - 根节点比较 `7 < 10`，进入左子节点 `[3, 7]`。
   - 找到键值 `7`，从该叶子节点开始遍历。
2. **沿叶子节点链表遍历**：
   - 左子节点 `[3, 7]` → 右兄弟节点 `[10, 15]` → 右兄弟节点 `[20, 25]`。
   - 收集所有满足 `7 ≤ ID ≤ 20` 的键值：`7, 10, 15, 20`。



## python实现B+树存储

```
关于B+树的操作，插入、删除、查找和修改。插入时可能需要分裂节点，删除时可能需要合并或重新分配键。这些操作都需要处理节点的读写，并确保树保持平衡。此外，每个操作后需要将修改后的节点写回文件。

考虑页的大小限制，假设每个键是4字节整数，指针或页号也是4字节。对于内部节点，假设阶数为m，则每个节点最多有m个键和m+1个指针。总大小为 m*4 + (m+1)*4 + 元数据（比如是否是叶子节点1字节，当前键数2字节）。总大小不超过4096。比如，假设元数据占3字节，那么剩下4093字节。每对键和指针占8字节（4+4），所以m*8 +4 <=4093，解得m大约511，但可能计算有误，需要更精确的计算。或者，可能用户希望更简单的实现，阶数可以设置一个合理的值，如每个节点可以存100个键，这样计算更简单，但可能页大小不够。需要精确计算。

例如，元数据：is_leaf（1字节），num_keys（2字节），假设用unsigned short，共3字节。剩下的4093字节。每个内部节点的条目是key和child_ptr，每个占4+4=8字节。那么最多可以有 (4093) // 8 = 511个条目，所以阶数m为511，这样每个内部节点可以有最多510个键（因为B+树的内部节点最多有m-1个键？或者可能需要重新确认B+树的定义）。或者，阶数m指的是子节点的最大数目，内部节点的键数目是m-1。这部分可能需要更仔细的思考。

不过对于简单实现，可能可以设定每个节点的最大键数目为一个固定值，例如200个键，这样每个节点的大小不会超过4KB。或者，根据实际计算来确定。比如，对于内部节点：每个键和子节点指针占8字节，元数据3字节。所以总大小是3 + 8*m <=4096，那么m最大为 (4096-3)/8= 511.625，即每个内部节点最多511个键，对应的子节点数目为512。因此阶数为512，每个内部节点可以有最多511个键和512个子节点。而叶子节点的结构可能不同，每个叶子节点存储键和数据指针，数据可能直接存在叶子节点中或者存在其他地方。例如，如果数据存在叶子节点中，每个数据项的大小需要固定，比如每个数据项是value_size字节。假设键是4字节，数据是例如60字节，那么每个条目占64字节。元数据是3字节，加上兄弟节点的指针4字节（叶子节点之间有链接），总元数据3+4=7字节。剩下的4089字节，每个条目64字节，所以最多4089//64=63个条目。这样叶子节点最多有63个键和数据。这可能比较小，但如果是简单实现的话，可能可以接受。

或者，可能数据不直接存储在叶子节点中，而是存储数据的指针，例如页号和偏移量。但这样会增加复杂度，用户可能需要数据直接存在叶子节点里。所以这里可能需要权衡。

可能用户希望每个叶子节点存储键和对应的数据，每个数据项是固定大小的。例如，假设数据是固定长度的字符串，比如60字节。这样每个键是4字节，数据是60字节，每个条目64字节。加上元数据，比如is_leaf（1字节），num_keys（2字节），next_leaf（4字节，指向下一个叶子节点的页号），总元数据是7字节。剩下的4096-7=4089字节，可以存储4089//64≈63个条目。这样每个叶子节点最多63个键值对。而内部节点的话，每个条目是键（4字节）和子页号（4字节），所以每个条目8字节，加上元数据3字节，剩下的4093字节，可以存储4093//8≈511个条目。所以内部节点可以有最多511个键，512个子节点。这可能比较合理。

接下来，如何设计节点类。可能需要一个基类或者分别处理内部节点和叶子节点。但为了简化，可能可以统一处理，根据is_leaf判断。每个节点在序列化时需要将键和子节点或数据打包成二进制格式。例如，内部节点的结构是：1字节is_leaf（0），2字节num_keys，然后是num_keys个键，每个4字节，然后是num_keys+1个子页号，每个4字节。总大小是1 + 2 + 4*num_keys + 4*(num_keys+1) = 3 + 8*num_keys +4 = 7 +8*num_keys。这个必须小于等于4096。当num_keys最大为511时，总大小是7+8*511=7+4088=4095，刚好不超过4096。所以内部节点的最大键数目是511，子节点数目512。对于叶子节点，结构是1字节is_leaf（1），2字节num_keys，4字节next_leaf，然后是num_keys个条目，每个条目是4字节key和60字节data。总元数据是7字节。每个条目64字节，总大小是7 +64*num_keys <=4096 → num_keys <= (4096-7)/64 ≈63.89，即最多63个条目。这样叶子节点每个最多存63个键值对。

所以，B+树的阶数对于内部节点是512，叶子节点每个最多63条目。这可能是一个可行的结构。

接下来，实现文件存储。文件的结构：第一个页（页号0）是文件头，存储根页号、页大小（4096）、树的其他元数据如阶数等。然后其他页是节点页。每次读取或写入节点时，根据页号计算偏移量（页号*4096）。
```

**以下是一个基于B+树的简单数据文件存储实现，支持基本的插入、查找和页面管理。由于篇幅和复杂度限制，删除和部分高级功能未完全实现，但展示了核心结构和操作。**

```py
import os
import struct

PAGE_SIZE = 4096
HEADER_SIZE = 12  # 4字节魔数 + 4字节根页号 + 4字节页大小
MAX_LEAF_ENTRIES = (PAGE_SIZE - 7) // 64  # 每个叶子节点最多63个条目
MAX_INTERNAL_KEYS = (PAGE_SIZE - 3) // 8   # 每个内部节点最多511个键

class BPlusTree:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, 'r+b') if os.path.exists(filename) else open(filename, 'w+b')
        self.root_page = 1
        self._initialize()

    def _initialize(self):
        if os.path.getsize(self.filename) == 0:
            self.file.write(b'\x00' * PAGE_SIZE)  # 初始化文件头
            self._write_header()
            self._initialize_leaf_page(1)         # 初始化根页为叶子节点

    def _write_header(self):
        magic = 0x424B5452
        self.file.seek(0)
        self.file.write(struct.pack('<III', magic, self.root_page, PAGE_SIZE))

    def _initialize_leaf_page(self, page_num):
        data = struct.pack('<BHI', 1, 0, 0)  # is_leaf=1, num_keys=0, next_leaf=0
        data = data.ljust(PAGE_SIZE, b'\x00')
        self._write_page(page_num, data)

    def _read_page(self, page_num):
        self.file.seek(page_num * PAGE_SIZE)
        return self.file.read(PAGE_SIZE)

    def _write_page(self, page_num, data):
        self.file.seek(page_num * PAGE_SIZE)
        self.file.write(data)

    def _find_leaf_page(self, key):
        current_page = self.root_page
        while True:
            page_data = self._read_page(current_page)
            is_leaf = page_data[0]
            if is_leaf:
                return current_page
            num_keys = struct.unpack_from('<H', page_data, 1)[0]
            keys = struct.unpack_from(f'<{num_keys}I', page_data, 3)
            ptrs = struct.unpack_from(f'<{num_keys + 1}I', page_data, 3 + 4 * num_keys)
            idx = 0
            while idx < num_keys and key >= keys[idx]:
                idx += 1
            current_page = ptrs[idx]

    def insert(self, key, value):
        leaf_page = self._find_leaf_page(key)
        page_data = self._read_page(leaf_page)
        is_leaf, num_keys, next_leaf = struct.unpack_from('<BHI', page_data)
        entries = []
        pos = 7
        for _ in range(num_keys):
            k = struct.unpack_from('<I', page_data, pos)[0]
            v = page_data[pos+4:pos+64]
            entries.append((k, v))
            pos += 64
        
        idx = 0
        while idx < num_keys and entries[idx][0] < key:
            idx += 1
        
        if idx < num_keys and entries[idx][0] == key:
            entries[idx] = (key, value.ljust(60, b'\x00'))
        else:
            entries.insert(idx, (key, value.ljust(60, b'\x00')))
            num_keys += 1

        if num_keys <= MAX_LEAF_ENTRIES:
            self._write_leaf_page(leaf_page, entries, next_leaf)
        else:
            split = num_keys // 2
            left_entries = entries[:split]
            right_entries = entries[split:]
            new_page = self._allocate_page()
            self._write_leaf_page(leaf_page, left_entries, new_page)
            self._write_leaf_page(new_page, right_entries, next_leaf)
            self._insert_into_parent(leaf_page, right_entries[0][0], new_page)

    def _write_leaf_page(self, page_num, entries, next_leaf):
        data = struct.pack('<BHI', 1, len(entries), next_leaf)
        for k, v in entries:
            data += struct.pack('<I', k) + v
        data = data.ljust(PAGE_SIZE, b'\x00')
        self._write_page(page_num, data)

    def _allocate_page(self):
        self.file.seek(0, 2)
        return self.file.tell() // PAGE_SIZE

    def _insert_into_parent(self, old_page, key, new_page):
        # 简化的父节点插入逻辑，可能需要处理根页分裂
        pass

    def get(self, key):
        leaf_page = self._find_leaf_page(key)
        page_data = self._read_page(leaf_page)
        _, num_keys, _ = struct.unpack_from('<BHI', page_data)
        pos = 7
        for _ in range(num_keys):
            k = struct.unpack_from('<I', page_data, pos)[0]
            if k == key:
                return page_data[pos+4:pos+64]
            pos += 64
        return None

    def close(self):
        self.file.close()

# 示例用法
tree = BPlusTree('test.bpt')
tree.insert(1, b'value1')
tree.insert(2, b'value2')
print(tree.get(1))  # 输出: b'value1\x00\x00...'
tree.close()
```

**实现说明**：

1. **文件结构**：文件头包含魔数、根页号和页大小，后续页面按4KB组织。
2. **节点结构**：
   - 叶子节点：标识符+条目数+下一页指针+键值对（键4字节+值60字节）
   - 内部节点：标识符+键数+键列表+子页指针列表（未完整实现）
3. **插入操作**：处理叶子节点分裂，但父节点更新部分未完整实现。
4. **查找操作**：从根页开始递归查找叶子节点。

**注意事项**：

- 该实现未完整处理内部节点分裂和根页更新
- 删除操作和完整的分裂/合并逻辑需要进一步实现
- 值部分固定为60字节，需根据需求调整
- 页面分配使用简单追加策略，未实现空间回收

这个实现展示了B+树的核心结构和基本操作，可以作为进一步开发的基础框架。