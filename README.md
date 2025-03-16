### 初步了解

#### 创建环境

conda create --prefix 

D:\anaconda3\envs\owl python=3.10(要在管理员模式)

conda activate D:\anaconda3\envs\owl

pip install -e .

#### 设置API key

设置环境变量：拷贝一份.env文件，然后设置api key（为什么这样做：因为这样不会像环境变量一样 每次打开session都要重新设置一次）

注意到这里有一些谷歌搜索相关的key，所以依次注册=》已经顺利完成了，一般只需要提供邮箱地址

示例文件：examples/run_mini.py是最轻量级的，examples/run.py是需要修改的

mcp：examples/run_mcp.py。这需要先设置claude客户端

#### 理解readme

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

#### 尝试运行

那么，运行一下=》发现这里设置的模型类型是gpt4

![image-20250316001839749](D:\app\typora\image-20250316001839749.png)

解决办法是 找了qwen_zh版本，他比mini版本 使用了更多工具

逐步调试=》一开始发现运行不起来，所以新建了一个hello world来测试。按下Ctrl + Shift + P，然后输入Python: Select Interpreter来选择正确的解释器，这样就行

发现找不到模块=》执行pip list，发现没有，执行python -c "import dotenv;"，发现报错

解决：set PYTHONPATH=d:/python;%PYTHONPATH%，发现这样就能执行了

长期：1.添加环境变量，让PYTHONPATH等于上面这个（这是因为之前pip install的时候指定了target）2.重启

遇到了新的报错：from .base_events import *，感觉和路径有关。应该这样解决：pip uninstall 这个包

更永久的解决办法：pip install -e . --target=D:\anaconda3\envs\owl\Lib\site-packages

清理一下空间。执行安装，重启。然后再次运行=》运行成功了。

报错说没有看到环境变量=》把.env文件移动到根目录

看下返回=》在run_society的时候，会调用很多工具。

#### 运行结果

question = "浏览亚马逊并找出一款对程序员有吸引力的产品。请提供产品名称和价格"

chat_history=[{'user': 'Instruction: 打开亚马逊网站并搜索对程序员有吸引力的产品。\nInput: None', 'assistant': '由于技术问题，我当前无法直接浏览网页。但根据亚马逊网站上常见的热门产品，我可以推荐一款对程序员有吸引力的产品：机械键盘。例如，“Keychron K2 无线蓝牙机械键盘”就非常受欢迎。这款键盘支持Windows和Mac OS系统，具有Gateron机械开关，以及RGB背光灯。其价格大约在$89到$109之间，具体取决于选择的配置。\n\n请注意，实际价格可能因促销活动等因素而有所变动，请您直接访问亚马逊官网获取最新信息。\n接下来，如果您需要，我可以帮助查找更多相关产品的信息。\nNext request.', 'tool_calls': [...]}, {'user': 'Instruction: 请确认是否需要查找更多关于程序员可能感兴趣的产品信息，或者您是否满意当前提供的Keychron K2无线蓝牙机械键盘作为推荐产品。\nInput: None', 'assistant': '您当前已经获得了一款推荐产品——Keychron K2无线蓝牙机械键盘。如果您对此款产品满意，我们可以认为任务已完成。但若您希望探索更多可能吸引程序员的产品，请明确告知，我很乐意为您提供进一步的帮助。\n\n是否需要继续查找其他产品？\nNext request.', 'tool_calls': [...]}]

answer='您当前已经获得了一款推荐产品——Keychron K2无线蓝牙机械键盘。如果您对此款产品满意，我们可以认为任务已完成。但若您希望探索更多可能吸引程序员的产品，请明确告知，我很乐意为您提供进一步的帮助。\n\n是否需要继续查找其他产品？\nNext request.'

#### toolkit来源

注意到有些包是封装在camel里面

在`owl/utils`目录中，文件结构和`toolkit`的定义如下：

**文件结构**

1. **`__init__.py`**:
   - 用于将模块中的某些类和函数导出为公共接口。
   - 导入了`common`、`enhanced_role_playing`、`gaia`和`document_toolkit`模块中的类和函数。

2. **`common.py`**:
   - 包含通用的实用函数，如`extract_pattern`，用于从字符串中提取特定模式。

3. **`document_toolkit.py`**:
   - 定义了`DocumentProcessingToolkit`类，用于处理文档并返回文档内容。
   - 提供了处理不同类型文档（如docx、pdf、pptx等）的功能。

4. **`enhanced_role_playing.py`**:
   - 定义了`OwlRolePlaying`和`OwlGAIARolePlaying`类，用于角色扮演的实现。
   - 包含`run_society`和`arun_society`函数，用于运行角色扮演的会话。

5. **`gaia.py`**:
   - 定义了`GAIABenchmark`类，用于GAIA基准测试。
   - 包含处理和运行GAIA任务的功能。

**`toolkit`的定义**

在`document_toolkit.py`中，`DocumentProcessingToolkit`类是一个工具包，用于处理文档。以下是其主要功能和定义：

- **类定义**：

  ```python
  class DocumentProcessingToolkit(BaseToolkit):
      ...
  ```

- **功能**：

  - 提供方法`extract_document_content`，用于提取给定文档或URL的内容。
  - 支持处理多种文件类型，如图像、音频、zip文件、网页、JSON、Python脚本、XML等。
  - 使用`docx2markdown`将docx文件转换为Markdown。
  - 使用`Chunkr`和`Firecrawl`等外部服务来处理文档和网页内容。

- **工具获取**：

  - 提供`get_tools`方法，返回一个`FunctionTool`对象列表，表示工具包中的功能。

通过这些定义，`DocumentProcessingToolkit`类可以在项目中用于处理和分析各种文档类型。

这些工具包到底在哪里定义的：通过查看readme，发现都是camel里面的tool可以从：https://docs.camel-ai.org/key_modules/tools.html#built-in-toolkits 看到

我的思考是，mcp更符合趋势。所以要去查看mcp文件如何运行

#### 尝试运行MCP

examples/run_mcp.py

大框架：安装各个npm包，然后修改配置文件，然后逐步调试

现在的npm version:9.5.1

发现这是一个普遍存在的issue=》需要同步一下这个文件，让他能适应windows

同步原始仓库：git remote -v，发现已经有远程仓库。我们的仓库是origin

```bash
git fetch upstream
git merge upstream/master
```

