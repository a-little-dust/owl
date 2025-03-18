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

发现这是一个普遍存在的issue=》需要同步一下这个文件，让他能适应windows

同步原始仓库：git remote -v，发现已经有远程仓库。我们的仓库是origin

```bash
git fetch upstream
git merge upstream/master
```

已经成功同步。然后安装别的东西，并确认配置文件=》已经都添加上了

现在的报错：Error code: 403 - {'error': {'code': 'unsupported_country_region_territory', 'message': 'Country, 
region, or territory not supported', 'param': None, 'type': 'request_forbidden'}}

原因：openai=》把下面改了，然后就能运行

![image-20250316233411692](D:\app\typora\image-20250316233411692.png)

收到了新的警告：node需要在10版本以上。现在的npm version:9.5.1

安装了npm-windows，并理论上已经安装了环境变量，只需要重启一下=》成功

```bash
nvm install lts
nvm list
nvm use 22.14.0
```

另外还要注意：要用cmd窗口执行

npx -y @wonderwhy-er/desktop-commander@latest setup --force-file-protocol --path file:///D:/vs_temp/owl

发现是包的问题，等后面再解决

#### MCP运行结果

问题：搜索某个作者的学术报告，然后整理成markdown并保存

结果：自称已经保存，实际上没保存，说明不对

### 理解代码

看到了官网：[代理 — CAMEL 0.2.31 文档 (camel-ai.org)](https://docs.camel-ai.org/key_modules/agents.html)

打算先自己理解，然后再看官网和代码有什么区别和联系

#### 关于工具

执行命令来安装工具：pip install camel-ai[tools] --target=D:\anaconda3\envs\owl\Lib\site-packages

```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
gensim 4.3.0 requires FuzzyTM>=0.4.0, which is not installed.
numba 0.56.4 requires numpy<1.24,>=1.18, but you have numpy 1.26.4 which is incompatible.
jupyter-server 1.23.4 requires anyio<4,>=3.1.0, but you have anyio 4.9.0 which is incompatible.
conda-repo-cli 1.0.27 requires clyent==1.2.1, but you have clyent 1.2.2 which is incompatible.
conda-repo-cli 1.0.27 requires nbformat==5.4.0, but you have nbformat 5.7.0 which is incompatible.
conda-repo-cli 1.0.27 requires PyYAML==6.0, but you have pyyaml 6.0.2 which is incompatible.
conda-repo-cli 1.0.27 requires requests==2.28.1, but you have requests 2.32.3 which is incompatible.
```

然后试验看能否使用工具：能，顺利新建了一个工具并输出了。代码是：先定义一个函数，然后add_tool = FunctionTool(add)。这个新建的工具有一些默认的方法，并且可以传递给大模型

注意到所有工具都要用FunctionTool封装一次

#### 关于Agent

注意到千问这个例子没有用到。有多种类型的agent

![image-20250317102501197](D:\app\typora\image-20250317102501197.png)

#### 关于思维链等

注意到是封装在datagen这个类里：

![image-20250317103050669](D:\app\typora\image-20250317103050669.png)

如何找到源码=》找到camel的仓库，看到了[camel-ai/camel: 🐫 CAMEL: Finding the Scaling Law of Agents. The first and the best multi-agent framework. https://www.camel-ai.org (github.com)](https://github.com/camel-ai/camel)

思考：快速看一下self-instruct的源码，看是否有参考价值=》应该有。架构很好

##### 思维链

有以下函数：`monte_carlo_tree_search`、`binary_search_error` 和 `solve`。每个函数都有明确的职责，下面我将逐一解释每个函数的作用和逻辑。

**1. `monte_carlo_tree_search` 函数**

这个函数实现了蒙特卡洛树搜索（Monte Carlo Tree Search, MCTS），用于通过模拟和评估找到最佳解决方案。

**功能**

- **输入**：
  - `question`：需要解决的问题。
  - `partial_solution`：当前的部分解（默认为空字符串）。
- **输出**：
  - 返回当前解与标准答案之间的相似度评分（`float` 类型）。

**逻辑**

1. **检查是否有标准答案**：
   - 如果问题没有对应的标准答案，抛出 `ValueError`。
2. **构建评估提示**：
   - 构建一个提示字符串，包含问题、部分解和标准答案，要求评估模型给出一个 0 到 1 之间的评分。
3. **调用生成器代理**：
   - 重置生成器代理（`generator_agent`），并使用构建的提示字符串调用 `step` 方法。
   - 解析生成器代理的响应，提取评分。
4. **返回评分**：
   - 返回评分作为函数的输出。

**2. `binary_search_error` 函数**

这个函数使用二分查找算法来定位解决方案中的第一个错误。

**功能**

- **输入**：
  - `question`：需要解决的问题。
  - `solution`：完整的解决方案。
- **输出**：
  - 返回第一个错误的位置（`int` 类型）。如果没有错误，返回 -1。

**逻辑**

1. **分割句子**：
   - 使用英文句号和中文句号将解决方案分割成句子。
2. **检查整个解决方案是否正确**：
   - 如果整个解决方案正确，返回 -1。
3. **二分查找**：
   - 使用二分查找算法，逐步缩小范围，找到第一个错误的位置。
   - 每次检查当前部分解是否正确，根据结果调整搜索范围。
4. **返回错误位置**：
   - 返回第一个错误的位置。

**3. `solve` 函数**

这个函数是一个多步求解器，用于解决给定的问题。它结合了直接求解、蒙特卡洛树搜索和二分查找错误的方法。

**功能**

- **输入**：
  - `question`：需要解决的问题。
- **输出**：
  - 返回找到的最佳解决方案（`str` 类型）。

**逻辑**

1. **尝试直接求解**：
   - 使用 `get_answer` 方法尝试直接求解问题。
   - 如果直接求解的结果正确，直接返回该解。
2. **蒙特卡洛树搜索**：
   - 如果直接求解失败，使用蒙特卡洛树搜索找到一个评分较高的解。
   - 生成新的解，并评估其与标准答案的相似度。
   - 如果找到评分超过 0.9 的解，提前结束搜索并返回该解。
3. **二分查找错误**：
   - 如果最终解仍然不完全正确，使用二分查找定位错误。
4. **生成新的解**：
   - 根据正确的部分生成新的解，并将结果存储在 `solution_tree` 中。
   - 返回最终解。

**代码中的关键点**

- **`verify_answer` 方法**：用于验证解决方案是否正确。
- **`get_answer` 方法**：用于生成解决方案。
- **`generator_agent`**：一个代理对象，用于生成和评估解决方案。
- **`solution_tree`**：一个字典，用于存储问题及其对应的解决方案和错误位置。

##### 自发现

注意到豆包可以在线查看仓库。

![image-20250317121733323](D:\app\typora\image-20250317121733323.png)

![image-20250317121803542](D:\app\typora\image-20250317121803542.png)

![image-20250317122358212](D:\app\typora\image-20250317122358212.png)

![image-20250317122522394](D:\app\typora\image-20250317122522394.png)

![image-20250317122747134](D:\app\typora\image-20250317122747134.png)

原理：加载人类编写的种子指令、种子任务，然后以此为基础生成指令等（官网有完整解释）

#### 消息

- `role_name`：用户或助理角色的名称。
- `role_type`：角色的类型，或 。`RoleType.ASSISTANT``RoleType.USER`
- `meta_dict`：消息的可选元数据字典。
- `content`：消息的内容。

```python
message = BaseMessage(
    role_name="test_user",
    role_type=RoleType.USER,
    content="test content"
)
```

消息传递：

![image-20250317130953418](D:\app\typora\image-20250317130953418.png)

#### qwen代码

society是RolePlaying的实例，注意到有额外传递这些参数

![image-20250317132447133](D:\app\typora\image-20250317132447133.png)

构建好society就运行它。owl\utils\enhanced_role_playing.py有init RolePlaying和运行society，一般每个文件会用自己的参数传入RolePlaying进行构建，然后自动化运行

### 写代码：构建planning

思路是，把相关文件复制过来，在项目里import这个自定义的包

在哪里进行规划=》注意到model里有planning（设置了这个模型用千问）

注意到可以给assistant_agent_kwargs设置工具

计划把例子全部看一遍再开始写。





周二你需要做什么：做出初版，给出效果图（相当于最低程度的版本）

