# Gomoku
**Authors**: _[Jiancong Gao](https://github.com/jianconggao)_ and _[Zilong Liang](https://github.com/zlliang)_.

This is a Gomoku AI agent implementation, as the final project of [DATA130008](http://www.sdspeople.fudan.edu.cn/zywei/DATA130008/index.html) in Fudan University. Modified Alpha-beta pruned Minimax is implemented as main algorithm in `agent.py`.

It uses [Piskvork](http://gomocup.org/download-gomocup-manager/) as running framework, and we implement our agent according to [pbarin-python](https://github.com/stranskyjan/pbrain-pyrandom) template. To generate executable AI, run:
```
pyinstaller.exe pbrain.py pisqpipe.py --name pbrain-gomoku.exe --onefile
```

## Report
Our [report](report/report.pdf) shows our work in detail.

## References
- Gobang project (written in Javascript). _[Github](https://github.com/lihongxun945/gobang)_
- Qiao Tian and Hu Xiaoti (2016), _**CS221 Project Final Report: Gomoku Game Agent**_. _[Report](http://web.stanford.edu/class/cs221/2017/restricted/p-final/xiaotihu/final.pdf)_
