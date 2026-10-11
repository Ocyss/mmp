from typing import TYPE_CHECKING, Any, Optional

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from app.schemas.context import Context, MediaInfo
    from app.schemas.download import DownloadTask
    from app.schemas.file import FileItem
    from app.schemas.site import Site
    from app.schemas.subscribe import Subscribe


class Workflow(BaseModel):
    """
    工作流信息
    """

    id: int | None = Field(default=None, description="工作流ID")
    name: str | None = Field(default=None, description="工作流名称")
    description: str | None = Field(default=None, description="工作流描述")
    timer: str | None = Field(default=None, description="定时器")
    trigger_type: str | None = Field(default="timer", description="触发类型：timer-定时触发 event-事件触发 manual-手动触发")
    event_type: str | None = Field(default=None, description="事件类型（当trigger_type为event时使用）")
    event_conditions: dict | None = Field(default_factory=dict, description="事件条件（JSON格式，用于过滤事件）")
    state: str | None = Field(default=None, description="状态")
    current_action: str | None = Field(default=None, description="已执行动作")
    result: str | None = Field(default=None, description="任务执行结果")
    run_count: int | None = Field(default=0, description="已执行次数")
    actions: list | None = Field(default_factory=list, description="任务列表")
    flows: list | None = Field(default_factory=list, description="任务流")
    execution_config: dict | None = Field(default_factory=dict, description="工作流执行配置")
    execution_state: dict | None = Field(default_factory=dict, description="工作流结构化执行状态")
    add_time: str | None = Field(default=None, description="创建时间")
    last_time: str | None = Field(default=None, description="最后执行时间")

    model_config = ConfigDict(from_attributes=True)


class ActionParams(BaseModel):
    """
    动作基础参数
    """

    loop: bool | None = Field(default=False, description="是否需要循环")
    loop_interval: int | None = Field(default=0, description="循环间隔 (秒)")


class Action(BaseModel):
    """
    动作信息
    """

    id: str | None = Field(default=None, description="动作ID")
    type: str | None = Field(default=None, description="动作类型 (类名)")
    name: str | None = Field(default=None, description="动作名称")
    description: str | None = Field(default=None, description="动作描述")
    position: dict | None = Field(default_factory=dict, description="位置")
    data: dict | None = Field(default_factory=dict, description="参数")
    inputs: list[str] | None = Field(default_factory=list, description="动作输入声明")
    outputs: dict | None = Field(default_factory=dict, description="动作输出声明")
    join_policy: str | None = Field(default=None, description="多上游节点汇合策略")
    fail_policy: str | None = Field(default=None, description="动作失败后的工作流处理策略")
    branch_policy: str | None = Field(default=None, description="多出边分支策略")
    concurrency_key: str | None = Field(default=None, description="并发互斥键")
    timeout: int | None = Field(default=None, description="动作执行超时时间（秒）")
    retry: dict | None = Field(default_factory=dict, description="动作重试策略")


class ActionExecution(BaseModel):
    """
    动作执行情况
    """

    action: str | None = Field(default=None, description="当前动作（名称）")
    result: bool | None = Field(default=None, description="执行结果")
    message: str | None = Field(default=None, description="执行消息")


class ActionContext(BaseModel):
    """
    动作基础上下文，各动作通用数据
    """

    content: str | None = Field(default=None, description="文本类内容")
    torrents: list[Context] | None = Field(default_factory=list, description="资源列表")
    medias: list[MediaInfo] | None = Field(default_factory=list, description="媒体列表")
    fileitems: list[FileItem] | None = Field(default_factory=list, description="文件列表")
    downloads: list[DownloadTask] | None = Field(default_factory=list, description="下载任务列表")
    sites: list[Site] | None = Field(default_factory=list, description="站点列表")
    subscribes: list[Subscribe] | None = Field(default_factory=list, description="订阅列表")
    workflow_context: dict | None = Field(default_factory=dict, description="工作流全局上下文")
    node_outputs: dict | None = Field(default_factory=dict, description="节点输出数据")
    runtime_state: dict | None = Field(default_factory=dict, description="运行期状态")
    artifacts: dict | None = Field(default_factory=dict, description="大对象引用与产物数据")
    execute_history: list[ActionExecution] | None = Field(default_factory=list, description="执行历史")
    progress: int | None = Field(default=0, description="执行进度（%）")


class ActionResult(BaseModel):
    """
    动作执行结果。
    """

    success: bool | None = Field(default=True, description="动作是否执行成功")
    message: str | None = Field(default=None, description="动作执行消息")
    context: ActionContext | None = Field(default=None, description="动作执行后的上下文")
    outputs: dict[str, Any] | None = Field(default_factory=dict, description="当前节点显式输出")
    next_policy: str | None = Field(default=None, description="动作完成后的调度策略")
    attempts: int | None = Field(default=1, description="动作实际尝试次数")


class ActionFlow(BaseModel):
    """
    工作流流程
    """

    id: str | None = Field(default=None, description="流程ID")
    source: str | None = Field(default=None, description="源动作")
    target: str | None = Field(default=None, description="目标动作")
    animated: bool | None = Field(default=True, description="是否动画流程")
    data: dict | None = Field(default_factory=dict, description="流程扩展配置")
    condition: str | None = Field(default=None, description="流转条件表达式")
    join_policy: str | None = Field(default=None, description="目标节点汇合策略")
    branch_policy: str | None = Field(default=None, description="源节点分支策略")


class WorkflowShare(BaseModel):
    """
    工作流分享信息
    """

    id: int | None = Field(default=None, description="分享ID")
    share_title: str | None = Field(default=None, description="分享标题")
    share_comment: str | None = Field(default=None, description="分享说明")
    share_user: str | None = Field(default=None, description="分享人")
    share_uid: str | None = Field(default=None, description="分享人唯一ID")
    name: str | None = Field(default=None, description="工作流名称")
    description: str | None = Field(default=None, description="工作流描述")
    timer: str | None = Field(default=None, description="定时器")
    trigger_type: str | None = Field(default=None, description="触发类型")
    event_type: str | None = Field(default=None, description="事件类型")
    event_conditions: str | None = Field(default=None, description="事件条件")
    actions: str | None = Field(default=None, description="任务列表(JSON字符串)")
    flows: str | None = Field(default=None, description="任务流(JSON字符串)")
    context: str | None = Field(default=None, description="执行上下文(JSON字符串)")
    date: str | None = Field(default=None, description="分享时间")
    count: int | None = Field(default=0, description="复用人次")

    model_config = ConfigDict(from_attributes=True)
