# 需要让society知道有哪些工具可用，然后根据工具的名称来选择使用哪个工具

from dotenv import load_dotenv
from camel.models import ModelFactory
from camel.toolkits import (
    CodeExecutionToolkit,
    ExcelToolkit,
    ImageAnalysisToolkit,
    SearchToolkit,
    VideoAnalysisToolkit,
    BrowserToolkit,
    FileWriteToolkit,
) # 引入工具包
from camel.types import ModelPlatformType, ModelType #模型类型
from camel.societies import RolePlaying

from owl.utils import run_society, DocumentProcessingToolkit

from camel.logger import set_log_level


import pathlib

base_dir = pathlib.Path(__file__).parent.parent
env_path = base_dir / "owl" / ".env"
load_dotenv(dotenv_path=str(env_path))

set_log_level(level="DEBUG")


def construct_society(question: str) -> RolePlaying:
    """
    Construct a society of agents based on the given question.

    Args:
        question (str): The task or question to be addressed by the society.

    Returns:
        RolePlaying: A configured society of agents ready to address the question.
    """

    # Create models for different components
    models = {
        "user": ModelFactory.create(
            model_platform=ModelPlatformType.QWEN,
            model_type=ModelType.QWEN_MAX,
            model_config_dict={"temperature": 0},
        ),
        "assistant": ModelFactory.create(
            model_platform=ModelPlatformType.QWEN,
            model_type=ModelType.QWEN_MAX,
            model_config_dict={"temperature": 0},
        ),
        "web": ModelFactory.create(
            model_platform=ModelPlatformType.QWEN,
            model_type=ModelType.QWEN_VL_MAX,
            model_config_dict={"temperature": 0},
        ),
        "planning": ModelFactory.create(
            model_platform=ModelPlatformType.QWEN,
            model_type=ModelType.QWEN_MAX,
            model_config_dict={"temperature": 0},
        ),
        "video": ModelFactory.create(
            model_platform=ModelPlatformType.QWEN,
            model_type=ModelType.QWEN_VL_MAX,
            model_config_dict={"temperature": 0},
        ),
        "image": ModelFactory.create(
            model_platform=ModelPlatformType.QWEN,
            model_type=ModelType.QWEN_VL_MAX,
            model_config_dict={"temperature": 0},
        ),
        "document": ModelFactory.create(
            model_platform=ModelPlatformType.QWEN,
            model_type=ModelType.QWEN_VL_MAX,
            model_config_dict={"temperature": 0},
        ),
    }

    # Configure toolkits
    tools = [
        *BrowserToolkit(
            headless=False,  # Set to True for headless mode (e.g., on remote servers)
            web_agent_model=models["web"],
            planning_agent_model=models["planning"],
            output_language="Chinese",
        ).get_tools(),
        *VideoAnalysisToolkit(model=models["video"]).get_tools(),
        *CodeExecutionToolkit(sandbox="subprocess", verbose=True).get_tools(),
        *ImageAnalysisToolkit(model=models["image"]).get_tools(),
        SearchToolkit().search_duckduckgo,
        SearchToolkit().search_google,  # Comment this out if you don't have google search
        SearchToolkit().search_wiki,
        SearchToolkit().search_baidu,
        *ExcelToolkit().get_tools(),
        *DocumentProcessingToolkit(model=models["document"]).get_tools(),
        *FileWriteToolkit(output_dir="./").get_tools(),
    ]

    # Configure agent roles and parameters
    user_agent_kwargs = {"model": models["user"]}
    assistant_agent_kwargs = {"model": models["assistant"], "tools": tools}

    # Configure task parameters
    task_kwargs = {
        "task_prompt": question,
        "with_task_specify": False,
    }

    # Create and return the society
    society = RolePlaying(
        **task_kwargs,
        user_role_name="user",
        user_agent_kwargs=user_agent_kwargs,
        assistant_role_name="assistant",
        assistant_agent_kwargs=assistant_agent_kwargs,
        output_language="Chinese",
    )

    return society


def main():
    r"""Main function to run the OWL system with an example question."""
    # Example research question
    question = "浏览亚马逊并找出一款对程序员有吸引力的产品。请提供产品名称和价格"

    # Construct and run the society
    society = construct_society(question)
    answer, chat_history, token_count = run_society(society)

    # Output the result
    print(f"\033[94mAnswer: {answer}\033[0m")


if __name__ == "__main__":
    main()
