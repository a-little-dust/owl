## 一、初步了解

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

报错：camel.camel.toolkits.mcp_toolkit - ERROR - 
Failed to connect to MCP server: [WinError 2] 系统找不到指定的文件

Warning: node executable not found, reverting to pure-Python mode. Install Node.js v10 or newer to use Readability.js.

Warning: A working NPM installation was not found. The package will use Python-based article extraction.    
Warning: node executable not found, reverting to pure-Python mode. Install Node.js v10 or newer to use Readability.js.

## 二、理解代码

看到了官网：[代理 — CAMEL 0.2.31 文档 (camel-ai.org)](https://docs.camel-ai.org/key_modules/agents.html)

打算先自己理解，然后再看官网和代码有什么区别和联系

### 2.1 轮子

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

注意到所有工具都要用FunctionTool封装一次，例如：

```python
google_tool = FunctionTool(SearchToolkit().search_google)
wiki_tool = FunctionTool(SearchToolkit().search_wiki)
```

然后给agent设置tool：

```
tool_agent = ChatAgent(
    tools=tools,
)
```

#### 关于Agent

千问这个例子没有用到。有多种类型的agent

![image-20250317102501197](D:\app\typora\image-20250317102501197.png)

有以下类型：chat；批评家；和环境交互；多跳问答；推理；知识图谱；task分解；检索



#### 关于思维链等

注意到是封装在datagen这个类里：

![image-20250317103050669](D:\app\typora\image-20250317103050669.png)

如何找到源码=》找到camel的仓库，看到了[camel-ai/camel: 🐫 CAMEL: Finding the Scaling Law of Agents. The first and the best multi-agent framework. https://www.camel-ai.org (github.com)](https://github.com/camel-ai/camel)

思考：快速看一下self-instruct的源码，看是否有参考价值=》应该有。架构很好

##### 思维链

应用层：设置generator_agent，verifier_agent，问答对，search_limit，然后调用solve函数

![image-20250318212149608](D:\app\typora\image-20250318212149608.png)

注意到豆包可以在线查看仓库。可以把仓库URL发过去

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

思路：将人工编写的种子指令与机器生成的种子指令相结合，以创建多样化、高质量的任务指令，同时通过可配置的过滤机制确保质量。

应用层：设置ChatAgent，设置human-written seed tasks，num_machine_instructions，(6, 2)  # Use 6 human tasks and 2 machine tasks for generation，构建出pipeline，然后调用generate方法

![image-20250318215120285](D:\app\typora\image-20250318215120285.png)

举例：

![image-20250318215916766](D:\app\typora\image-20250318215916766.png)

逻辑层：

![image-20250317121733323](D:\app\typora\image-20250317121733323.png)

![image-20250317121803542](D:\app\typora\image-20250317121803542.png)

![image-20250317122358212](D:\app\typora\image-20250317122358212.png)

![image-20250317122522394](D:\app\typora\image-20250317122522394.png)

![image-20250317122747134](D:\app\typora\image-20250317122747134.png)

##### 多跳问答

“Source2Synth” 是 “Source to Synthesis” 的简写形式，“Synthesis” 意思是 “合成、综合” ，在这个语境中可以理解为对来源信息进行处理、整合后生成新的内容

目的：从源文本数据创建多跳问答对，目的是生成数据。流程：处理原始文本、提取信息对，并生成复杂多跳推理问题，可配置复杂性阈值

构建UserDataProcessor，

![image-20250318225812377](D:\app\typora\image-20250318225812377.png)



#### 消息

- `role_name`：用户或助理角色的名称。
- `role_type`：角色的类型，或 。`RoleType.ASSISTANT``RoleType.USER`
- `meta_dict`：消息的可选元数据字典。
- `content`：消息的内容。

```python
message = BaseMessage( # 创建消息
    role_name="test_user",
    role_type=RoleType.USER,
    content="test content"
)
```

消息可以进行类型转换，比如转为openai中 给用户/给助手的消息

包装好消息以后，可以传递到agent，其中sys_msg用于初始化agent，user_msg用于传递请求

![image-20250317130953418](D:\app\typora\image-20250317130953418.png)

#### 记忆

![image-20250318232921283](D:\app\typora\image-20250318232921283.png)

```python
# Create and write new records
records = [
    MemoryRecord(
        message=BaseMessage.make_user_message(
            role_name="User",
            meta_dict=None,
            content="What is CAMEL AI?",
        ),
        role_at_backend=OpenAIBackendRole.USER,
    ),
    MemoryRecord(
        message=BaseMessage.make_assistant_message(
            role_name="Agent",
            meta_dict=None,
            content="CAMEL-AI.org is the 1st LLM multi-agent framework and "
                    "an open-source community dedicated to finding the scaling law "
                    "of agents.",
        ),
        role_at_backend=OpenAIBackendRole.ASSISTANT,
    ),
]
memory.write_records(records)

# Set memory to the agent
agent.memory = memory

agent.memory.get_context()#读取记忆
#添加记忆
new_user_msg = BaseMessage.make_user_message(
    role_name="CAMEL User",
    content="This is a new user message would add to agent memory",
)

# Update the memory
agent.record_message(new_user_msg)
```

关键的类：memoryrecord, messagerecord, 

关于记忆的存储和检索：

![image-20250318235925431](D:\app\typora\image-20250318235925431.png)

类似地，有VectorDBBlock，是把记忆存储在向量

他们如何被调用：通过agent，有ChatHistoryMemory和VectorDBMemory。例如：

```python
memory = LongtermAgentMemory(
    context_creator=ScoreBasedContextCreator(
        token_counter=OpenAITokenCounter(ModelType.GPT_4O_MINI),
        token_limit=1024,
    ),
    chat_history_block=ChatHistoryBlock(),
    vector_db_block=VectorDBBlock(),
)
```

通常是先把block封装到memory，再往memory添加record。然后把agent的memory设置成这个

其中，memory record的主要信息就是message，ContextCreator用于检索到很多context record，其中每个record都包含memory record和分数

#### 提示词

注意到，TaskSpecifyAgent中提供了很多提示词模板

```python
#创建model
model = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI,
    model_type=ModelType.GPT_4O_MINI,
)
#基于model创建agent，并指定task是和AI_SOCIETY有关的
task_specify_agent = TaskSpecifyAgent(
    model=model, task_type=TaskType.AI_SOCIETY
)
#设定task为“改善舞台表現和表演技巧”，助手为音乐家，这样就会自动套入模板，得到prompt
specified_task_prompt = task_specify_agent.run(
    task_prompt="Improving stage presence and performance skills",
    meta_dict=dict(
        assistant_role="Musician", user_role="Student", word_limit=100
    ),
)
```

自定义提示词：可以使用任意的占位词，后面通过dict来传递信息

```python
my_prompt_template = TextPrompt(
    'Here is a task: I\'m a {occupation} and I want to {task}. Help me to make this task more specific.'
)  # Write anything you would like to use as prompt template
task_specify_agent = TaskSpecifyAgent(
    model=model, task_specify_prompt=my_prompt_template
)
response = task_specify_agent.run(
    task_prompt="get promotion",
    meta_dict=dict(occupation="Software Engineer"),
)
```

直接输入提示词：

```python
# Generate programming languages
languages_prompt = CodePromptTemplateDict.GENERATE_LANGUAGES.format(num_languages=5)
#List the 5 most commonly used computer programming languages.
#Be concise. No explanation required.

# Generate coding tasks
tasks_prompt = CodePromptTemplateDict.GENERATE_TASKS.format(num_tasks=3)
#List 3 diverse tasks that a programmer can assist a person working in {domain} using {language}.
#Be concise. Be creative.

# Create an AI coding assistant prompt，需要设定角色、要执行的任务描述
assistant_prompt = CodePromptTemplateDict.ASSISTANT_PROMPT.format(
    assistant_role="Python Expert",
    task_description="Implement a binary search algorithm",
)
```

得到的助手提示词：

```
Never forget you are a Computer Programmer and I am a person working in {domain}. Never flip roles! Never instruct me!
We share a common interest in collaborating to successfully complete a task.
You must help me to complete the task using {language} programming language.
Here is the task: {task}. Never forget our task!
I must instruct you based on your expertise and my needs to complete the task.

I must give you one instruction at a time.
You must write a specific solution that appropriately solves the requested instruction and explain your solutions.
You must decline my instruction honestly if you cannot perform the instruction due to physical, moral, legal reasons or your capability and explain the reasons.
Unless I say the task is completed, you should always start with:

Solution: <YOUR_SOLUTION>

<YOUR_SOLUTION> must contain {language} code and should be very specific, include detailed explanations and provide preferable implementations and examples for task-solving.
Always end <YOUR_SOLUTION> with: Next request.
```

EvaluationPromptTemplateDict：用于生成提示词，在某个领域，根据示例问题自拟多个问题

```python
questions_prompt = EvaluationPromptTemplateDict.GENERATE_QUESTIONS.format(
    num_questions=5,
    field="Machine Learning",
    examples="1. What is the difference between supervised and unsupervised learning?\n2. Explain the concept of overfitting.",
)
```

类似地，还有专门用于对象识别、专门 用于翻译的提示词

#### Task

定义：这个比提示更高一个级别，一个task可能包含多次对话。一个task可以由多个agent共同完成，并可以分解

常用方法：add_subtask，decompose（分解），compose（根据很多答案组合出答案）

```python
#创建task
task = Task(
    content="Weng earns $12 an hour for babysitting. Yesterday, she just did 51 minutes of babysitting. How much did she earn?",
    id="0",
)
#设置层次结构
root_task.add_subtask(sub_task_1)
#用agent自动分解task，得到task的列表
new_tasks = task.decompose(agent=agent, template=TASK_DECOMPOSE_PROMPT)
#解决各个task以后，用agent来构建答案
task.compose(agent=agent, template=TASK_COMPOSE_PROMPT)
print(task.result)
```

TaskManager：可以对task设置依赖关系，做拓扑排序，做evolve进化任务（比如让提示词更加明确）

```python
task_manager = TaskManager(task)
evolved_task = task_manager.evolve(task, agent=agent)
```

#### Loader数据读取

Base IO 模块专注于与文件相关的基本输入 / 输出

Unstructured IO提供了用于解析文件或 URL、清理数据、提取特定信息、为不同平台暂存元素以及分块元素的工具。该模块的核心在于其先进的 ETL 功能，用于处理非结构化数据，使其可用于检索增强生成 （RAG） 等各种应用程序

Firecrawl Reader 提供了一个 Python 接口来与 Firecrawl API 交互，允许用户将网站转换为大型语言模型 （LLM） 就绪的 markdown 格式

JinaURL Reader 是 Jina AI 的 URL 读取服务的 Python 客户端，经过优化，可从 URL 提供更清晰、对 LLM 友好的内容

```python
#结构化io
from camel.loaders import create_file_from_raw_bytes

# Read a pdf file from disk
with open("test.pdf", "rb") as file:
    file_content = file.read()

# Use the create_file function to create an object based on the file extension
file_obj = create_file_from_raw_bytes(file_content, "test.pdf")

# Once you have the File object, you can access its content
print(file_obj.docs[0]["page_content"])

#非结构化IO
uio = UnstructuredIO()
# Set example url
example_url = (
    "https://www.cnn.com/2023/01/30/sport/empire-state-building-green-"
    "philadelphia-eagles-spt-intl/index.html")
elements = uio.parse_file_or_url(example_url)#从URL获取数据
print(("\n\n".join([str(el) for el in elements])))

example_dirty_text = ("\x93Some dirty text â€™ with extra spaces and – dashes.")

# Set clean options,根据选项做清理  
options = [
    ('replace_unicode_quotes', {}),
    ('clean_dashes', {}),
    ('clean_non_ascii_chars', {}),
    ('clean_extra_whitespace', {}),
]

cleaned_text = uio.clean_text_data(text=example_dirty_text,clean_options=options)

#分块
staged_element = uio.stage_elements(elements=elements,stage_type="stage_for_baseplate")

#Chunkr Reader，用于读PDF
chunkr = ChunkrReader()
task_id = chunkr.submit_task(#构建task
    file_path="/Users/enrei/Large Language Model based Multi-Agents- A Survey of Progress and Challenges.pdf",
    model="Fast",
    ocr_strategy="Auto",
    target_chunk_length=512,
)
task_output = chunkr.get_task_output(#根据task Id获得内容
    task_id="7becf001-6f07-4f63-bddf-5633df363bbb"
)

#使用Jina Reader，获得markdown
jina_reader = JinaURLReader(return_format=JinaReturnFormat.MARKDOWN)
response = jina_reader.read_content("https://docs.camel-ai.org/")
```

#### Society

##### RolePlaying

为什么这样做：克服了许多挑战，例如*角色翻转*、*助手重复指令*、*片状回复*、*消息无限循环*和*对话终止条件*

- 永远不要忘记你是<ASSISTANT_ROLE>，我是<USER_ROLE>。

  *这会将所选角色分配给助理代理，并为其提供有关用户角色的信息。*

- 永远不要互换角色！永远不要指示我！

  *这可以防止代理翻转角色。在某些情况下，我们观察到 Assistant 和用户切换角色，其中 Assistant 突然接管控制权并指示用户，而用户则遵循这些指示。*

- 如果您因身体、道德、法律原因或您的能力而无法执行我的指示，您必须诚实地拒绝我的指示，并解释原因。

  *这禁止代理制作有害、虚假、非法和误导性信息。*

- 除非我说任务已完成，否则您应该始终从以下位置开始：解决方案：<YOUR_SOLUTION>。<YOUR_SOLUTION>应该是具体的，并为任务解决提供更可取的实现和示例。

  *这鼓励助理始终以一致的格式进行回应，避免与对话结构有任何偏差，并防止模糊或不完整的回应，我们称之为片状回应，例如“我会做某事”。*

- 始终以以下方式结束您的解决方案：Next request。

  *这可确保助手通过请求新的指令来解决来保持对话的进行。*

##### 交替对话实例

```python
def main(model=None, chat_turn_limit=50) -> None:
# Initial the role-playing session on developing a trading bot task with default model (`GPT_4O_MINI`)
    task_prompt = "Develop a trading bot for the stock market"
    role_play_session = RolePlaying(
        assistant_role_name="Python Programmer",
        assistant_agent_kwargs=dict(model=model),
        user_role_name="Stock Trader",
        user_agent_kwargs=dict(model=model),
        task_prompt=task_prompt,
        with_task_specify=True,
        task_specify_agent_kwargs=dict(model=model),
    )

    n = 0
    input_msg = role_play_session.init_chat()#初始化对话

# Output response step by step with different colors.
# Keep output until detect the terminate content or reach the loop limit.
    while n < chat_turn_limit:
        n += 1
        assistant_response, user_response = role_play_session.step(input_msg)

        if assistant_response.terminated:
            print(
                Fore.GREEN
                + (
                    "AI Assistant terminated. Reason: "
                    f"{assistant_response.info['termination_reasons']}."
                )
            )
            break
        if user_response.terminated:
            print(
                Fore.GREEN
                + (
                    "AI User terminated. "
                    f"Reason: {user_response.info['termination_reasons']}."
                )
            )
            break

        print_text_animated(
            Fore.BLUE + f"AI User:\n\n{user_response.msg.content}\n"
        )
        print_text_animated(
            Fore.GREEN + "AI Assistant:\n\n"
            f"{assistant_response.msg.content}\n"
        )

        if "CAMEL_TASK_DONE" in user_response.msg.content:
            break

        input_msg = assistant_response.msg

if __name__ == "__main__":
    main()
```

##### 构建society

```python
#设置task的内容，以及如何把task转为prompt
task_kwargs = {
    'task_prompt': 'Develop a plan to TRAVEL TO THE PAST and make changes.',
    'with_task_specify': True,
    'task_specify_agent_kwargs': {'model': model}
}
society = RolePlaying(
    **task_kwargs,             # The task arguments
    **user_role_kwargs,        # The instruction sender's arguments
    **assistant_role_kwargs,   # The instruction receiver's arguments
)

#设置run函数，传入society
def run(society, round_limit: int=10):

    # Get the initial message from the ai assistant to the ai user
    input_msg = society.init_chat()

    # Starting the interactive session
    for _ in range(round_limit):

        # Get the both responses for this round
        assistant_response, user_response = society.step(input_msg)

        # Check the termination condition
        if is_terminated(assistant_response) or is_terminated(user_response):
            break

        # Get the results
        print(f'[AI User] {user_response.msg.content}.\n')
        # Check if the task is end
        if 'CAMEL_TASK_DONE' in user_response.msg.content:
            break
        print(f'[AI Assistant] {assistant_response.msg.content}.\n')



        # 为下一回合，更新input_msg
        input_msg = assistant_response.msg

    return None
```

#### 检索

两种类型：向量检索 关键词检索（分词，从查询提取相关关键字，搜索这些关键字的出现次数，对这些文档进行排名）

```python
# Initialize the VectorRetriever with an embedding model
vr = VectorRetriever(embedding_model=OpenAIEmbedding())
vector_storage = QdrantStorage(#构建存储器，设置存储路径
    vector_dim=OpenAIEmbedding().get_output_dim(),
    collection_name="my first collection",
    path="storage_customized_run",
)
# Embed and store chunks of data in the vector storage
vr.process(content_input_path, vector_storage)
#执行查询
query = "What is CAMEL"
# Execute the query and retrieve results
results = vr.query(query, vector_storage)
```

带有RAG的agent：

```python
def single_agent(query: str) ->str :
    # Set agent role
    assistant_sys_msg = """You are a helpful assistant to answer question,
         I will give you the Original Query and Retrieved Context,
        answer the Original Query based on the Retrieved Context,
        if you can't answer the question just say I don't know."""

    # Add auto retriever
    auto_retriever = AutoRetriever(
            vector_storage_local_path="local_data2/",
            storage_type=StorageType.QDRANT,
            embedding_model=embedding_instance)

    retrieved_info = auto_retriever.run_vector_retriever(
        query=query,
        contents=[
            "local_data/camel_paper.pdf",  # example local path
            "https://github.com/camel-ai/camel/wiki/Contributing-Guidlines",  # example remote url
        ],
        top_k=1,
        return_detailed_info=False,
        similarity_threshold=0.5
    )

    # Pass the retrieved infomation to agent
    user_msg = str(retrieved_info)#把检索到的信息放入user_msg
    agent = ChatAgent(assistant_sys_msg)

    # Get response
    assistant_response = agent.step(user_msg)
    return assistant_response.msg.content
```

类似地，可以把RAG扩展到具有多个AGENT的社会

### 2.2 实例

#### agent和society如何使用工具

```python
agent = ChatAgent(
    assistant_sys_msg,
    model=model,
    tools=tools_list
)
role_play_session = RolePlaying(
    assistant_role_name="Searcher",
    user_role_name="Professor",
    assistant_agent_kwargs=dict(
        model=ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=ModelType.GPT_4O_MINI,
        ),
        tools=tools_list,
    ),
    user_agent_kwargs=dict(
        model=ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=ModelType.GPT_4O_MINI,
        ),
    ),
    task_prompt=task_prompt,
    with_task_specify=False,
)
#在输出中可以看到工具的调用情况：
Function Execution: sub
        Args: {'a': 2024, 'b': 1096}
        Result: 928
```

#### 树搜索

评论家代理负责 选择提案并向角色扮演代理提供信息丰富的口头反馈

<img src="D:\app\typora\image-20250319022249875.png" alt="image-20250319022249875" style="zoom:60%;" />

```python
critic_agent = CriticAgent(system_message=sys_msg, verbose=True)
task_kwargs = {
    'task_prompt': 'Develop a plan to TRAVEL TO THE PAST and make changes.',
    'with_task_specify': True,
    'task_specify_agent_kwargs': {'model': model}
}

user_role_kwargs = {
    'user_role_name': 'an ambitious aspiring TIME TRAVELER',
    'user_agent_kwargs': {'model': model}
}

assistant_role_kwargs = {
    'assistant_role_name': 'the best-ever experimental physicist',
    'assistant_agent_kwargs': {'model': model}
}

critic_role_kwargs = {
    'with_critic_in_the_loop': True,
    'critic_criteria': 'improve the task performance',
    'critic_kwargs': dict(verbose=True)
}
society = RolePlaying(
    **task_kwargs,             # The task arguments
    **user_role_kwargs,        # The instruction sender's arguments
    **assistant_role_kwargs,   # The instruction receiver's arguments
    **critic_role_kwargs,      # The critic's arguments
)
```



#### qwen代码

society是RolePlaying的实例，注意到有额外传递这些参数

![image-20250317132447133](D:\app\typora\image-20250317132447133.png)

构建好society就运行它。owl\utils\enhanced_role_playing.py有init RolePlaying和运行society，一般每个文件会用自己的参数传入RolePlaying进行构建，然后自动化运行society

具体来说：我们主要看文档的代码部分。



## 三、写代码：构建planning

思路是，把相关文件复制过来，在项目里import这个自定义的包

在哪里进行规划=》注意到model里有planning（设置了这个模型用千问）

注意到可以给assistant_agent_kwargs设置工具

计划把例子全部看一遍再开始写。





周二你需要做什么：做出初版，给出效果图（相当于最低程度的版本）

