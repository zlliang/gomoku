# 框架约定

- 将棋局读取、分析等实用工具放入 `utils.py` 
  - `TODO` 设计棋局表示方式 `class Board`
  - `TODO` 设计高效提取 pattern 的方式，比如缓存在对象的一个字典里 `board.pattern()`
- 将评估棋盘的函数放入 `evaluate.py`
  - `TODO` 这个文件里只有一个主要函数 `def evaluate(board)`
- Agent 的主逻辑放入 `[algorithm_name].py`
  - `baseline.py`
  - `TODO` `minimax.py`
  - `TODO` 遗传算法或者 MCTS 算法的精细实现
  - 在这些文件中定义 metadata，比如 `infotext`，然后再在 `pbrain` 框架中替换
- 将框架程序 `example.py` 命名为 `pbrain.py`。为疏松对某个 agent 的耦合，尽量少对这个文件做改动，而是放在各个 agent 文件中，而后 `import` 进 `pbrain.py` 做替换 `pp.brain_turn = brain_turn` 等

## `Board` 类的用法

`util.Board` 类实现了有效的棋局表示，支持类似于 NumPy 的索引和赋值。

```python
>>> b = Board()  # 构造一个空棋盘
>>> b  # 直接访问对象，会打印棋局
[0, 0, 0, 0, 0]
[0, 0, 0, 0, 0]
[0, 0, 0, 0, 0]
[0, 0, 0, 0, 0]
[0, 0, 0, 0, 0]
>>> b[1, 2] = 5  # 支持 NumPy 方式的赋值，每次只能给一个格子赋值
>>> b
[0, 0, 0, 0, 0]
[0, 0, 0, 0, 0]
[0, 5, 0, 0, 0]
[0, 0, 0, 0, 0]
[0, 0, 0, 0, 0]
>>> b[1, 3]  # 支持 NumPy 方式的索引。只提取一个元素时得到的是一个数
0
>>> b[:, 2]  # 提取一个子棋局，得到的是又一个 Board 对象
[0, 5, 0, 0, 0]
>>> b[1, :]
[0]
[0]
[5]
[0]
[0]
>>> b[0:3, 1:3]  # 获取子棋局，便于得到局部状况
[0, 0, 0]
[0, 5, 0]
```
