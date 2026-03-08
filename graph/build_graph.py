from langgraph.graph import StateGraph, END
from graph.state import AgentState
from graph.nodes import (
    supervisor_node,
    planner_node,
    data_node,
    feature_node,
    ml_node,
    evaluation_node,
    deployment_node,
    debug_node,
    monitoring_node,   # ✅ Make sure this exists
)
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3


def build_graph():

    workflow = StateGraph(AgentState)

    # -------------------------
    # Add ALL nodes FIRST
    # -------------------------
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("data", data_node)
    workflow.add_node("feature", feature_node)
    workflow.add_node("ml", ml_node)
    workflow.add_node("evaluation", evaluation_node)
    workflow.add_node("deployment", deployment_node)
    workflow.add_node("debug", debug_node)
    workflow.add_node("monitoring", monitoring_node)  # ✅ REQUIRED

    # -------------------------
    # Entry Point (ONLY ONE)
    # -------------------------
    workflow.set_entry_point("supervisor")

    # -------------------------
    # Core Flow
    # -------------------------
    workflow.add_edge("supervisor", "planner")
    workflow.add_edge("planner", "data")
    workflow.add_edge("data", "feature")
    workflow.add_edge("feature", "ml")

    # -------------------------
    # ML → Debug or Evaluation
    # -------------------------
    def route_after_ml(state):
        if state.get("error_trace"):
            return "debug"
        return "evaluation"

    workflow.add_conditional_edges("ml", route_after_ml)

    # -------------------------
    # Debug Loop
    # -------------------------
    def route_after_debug(state):
        if state.get("retry_count", 0) > 3:
            return END
        return "ml"

    workflow.add_conditional_edges("debug", route_after_debug)

    # -------------------------
    # Performance Loop
    # -------------------------
    def route_after_eval(state):
        status = state.get("deployment_status")

        if status == "approved":
            return "deployment"

        if status == "improve":
            return "feature"

        return END

    workflow.add_conditional_edges("evaluation", route_after_eval)

    # -------------------------
    # Deployment → Monitoring
    # -------------------------
    workflow.add_edge("deployment", "monitoring")

    # -------------------------
    # Drift → Retrain Loop
    # -------------------------
    def route_after_monitor(state):
        if state.get("drift_detected"):
            return "ml"
        return END

    workflow.add_conditional_edges("monitoring", route_after_monitor)

    conn = sqlite3.connect("agent_memory.db", check_same_thread=False)
    checkpointer = SqliteSaver(conn)



    graph = workflow.compile(checkpointer=checkpointer)

    # Optional: save graph image
    #graph.get_graph().draw_png("agent_graph.png")

    return graph