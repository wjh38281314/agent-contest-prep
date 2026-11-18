"""
第 1 周练习：不用任何框架，手写一个最小的 ReAct 循环。

ReAct 的意思：先想（Thought）→ 再动手（Action）→ 看结果（Observation），
一轮一轮往下走，直到信息够回答为止。

运行方法（在项目根目录执行）：
    py week-01/react_loop.py

特点：只用 Python 自带的标准库，不用装第三方包，不用 API key，不联网。
"""

from datetime import date
from pathlib import Path

# 第 1 步：找到数据文件
# 用 __file__ 定位，保证不管从哪个目录运行脚本，都能找到同目录的 tasks.txt
TASK_FILE = Path(__file__).parent / "tasks.txt"


# 第 2 步：定义两个「工具」
# 智能体自己不会算，它只会调用这些函数。以后加新工具，就在这里加一个函数。
def lookup_deadline(keyword: str) -> str:
    """作用：在 tasks.txt 里按关键词找一条安排，返回 '日期,事项'。"""
    for line in TASK_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        day, item = line.split(",", 1)
        if keyword in item:
            return f"{day.strip()},{item.strip()}"
    return "没找到"


def days_until(day_text: str) -> str:
    """作用：算出某个日期距离今天还有几天。"""
    target = date.fromisoformat(day_text)
    return str((target - date.today()).days)


# 工具登记表：名字 → 函数。想加工具，加一行就行。
TOOLS = {
    "查安排": lookup_deadline,
    "算天数": days_until,
}


# 第 3 步：跑一个最小循环
def run() -> None:
    question = "蓝桥杯报名截止还有几天？"
    print("问题：", question)

    # 第 1 周故意把「计划」写死：先看清循环长什么样。
    # 第 4 周再改成由规则或模型动态决定下一步用哪个工具。
    plan = [
        ("要回答这个问题，得先知道报名截止是哪天", "查安排", "蓝桥杯报名"),
        ("拿到日期了，接下来算还剩几天", "算天数", "上一轮的日期"),
    ]

    memory = {}  # 存每一轮看到的结果，下一轮可以接着用

    for round_no, (thought, tool_name, arg) in enumerate(plan, start=1):
        print(f"\n第 {round_no} 轮")
        print("  Thought     ：", thought)

        if arg == "上一轮的日期":
            arg = memory["日期"]  # 用上一轮的结果当这一轮的输入

        print(f"  Action      ：{tool_name}('{arg}')")
        observation = TOOLS[tool_name](arg)
        print("  Observation ：", observation)

        if tool_name == "查安排":
            if observation == "没找到":
                print("\n  Answer      ：没查到这条安排，请检查 tasks.txt")
                return
            memory["日期"] = observation.split(",")[0]
        else:
            memory["天数"] = observation
            print("\n  Thought     ：信息够了，可以回答了")
            break

    print(
        "\n  Answer      ：",
        f"蓝桥杯报名截止是 {memory['日期']}，还有 {memory['天数']} 天。",
    )


if __name__ == "__main__":
    run()
