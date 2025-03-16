已经执行的命令：

conda create --prefix 

D:\anaconda3\envs\owl python=3.10(要在管理员模式)

conda activate D:\anaconda3\envs\owl

pip install -e .

设置环境变量：拷贝一份.env文件，然后设置api key（为什么这样做：因为这样不会像环境变量一样 每次打开session都要重新设置一次）

注意到这里有一些谷歌搜索相关的key，所以依次注册=》已经顺利完成了，一般只需要提供邮箱地址

示例文件：examples/run_mini.py是最轻量级的，examples/run.py是需要修改的

mcp：examples/run_mcp.py。这需要先设置claude客户端

理解一下readme：

对不同的模型设置了不同的脚本，例如qwen

![image-20250315235500762](D:\app\typora\image-20250315235500762.png)

可以尝试以下示例任务：

- "查询苹果公司的最新股票价格"
- "分析关于气候变化的最新推文情绪"
- “帮我调试这段 Python 代码：[在此粘贴你的代码]”
- “总结这篇研究论文的主要观点：[论文URL]”

观察：没有那么难，但是实用

![image-20250315235837796](D:\app\typora\image-20250315235837796.png)

如何加入他们：解决开放的问题，并完成单元测试、演示视频。观察了一下，问题有：

![image-20250316000733635](D:\app\typora\image-20250316000733635.png)

那么，运行一下=》发现这里设置的模型类型是gpt4

![image-20250316001839749](D:\app\typora\image-20250316001839749.png)

解决办法是 找了qwen_zh版本，他比mini版本 使用了更多工具。逐步调试=》一开始发现运行不起来，所以新建了一个hello world来测试。按下Ctrl + Shift + P，然后输入Python: Select Interpreter来选择正确的解释器，这样就行

发现找不到模块=》执行pip list，发现没有，执行python -c "import dotenv;"，发现报错

解决：set PYTHONPATH=d:/python;%PYTHONPATH%，发现这样就能执行了

长期：1.添加环境变量，让PYTHONPATH等于上面这个（这是因为之前pip install的时候指定了target）

2.重启

遇到了新的报错：from .base_events import *，感觉和路径有关。应该这样解决：pip uninstall 这个包

更永久的解决办法：pip install -e . --target=D:\anaconda3\envs\owl\Lib\site-packages

先清理一下空间。



