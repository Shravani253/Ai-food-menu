"""
alerts_embeddings.py

This module runs AFTER:
    database/embeddings.py  (knowledge creation + embeddings)

And BEFORE:
    llm/llm_function.py     (LLM reasoning)

Purpose:
- Convert raw freshness & quantity knowledge into visual risk signals
- Provide RED / YELLOW / GREEN safety indicators
- Provide dish-level risk summary
- Provide system-level dashboard summary
"""

# ============================
# Visual Color Logic
# ============================

def freshness_color(freshness):
    total = freshness["total_days"]
    life = freshness["life_span"]

    ratio = total / life

    if ratio <= 0.7:
        return "GREEN", "🟢 Fresh"
    elif ratio <= 1.0:
        return "YELLOW", "🟡 Near Expiry"
    else:
        return "RED", "🔴 Expired / Harmful"


# ============================
# Ingredient Visual Wrapper
# ============================

def build_visual_alert(knowledge):
    color, label = freshness_color(knowledge["freshness"])

    return {
        "ingredient_id": knowledge["ingredient_id"],
        "name": knowledge["name"],
        "color": color,
        "label": label,
        "alerts": knowledge["alerts"],
        "freshness": knowledge["freshness"],
        "quantity": knowledge["quantity"]
    }


# ============================
# Dish Level Risk Aggregation
# ============================

def dish_risk_summary(ingredient_visuals):
    red = sum(1 for i in ingredient_visuals if i["color"] == "RED")
    yellow = sum(1 for i in ingredient_visuals if i["color"] == "YELLOW")
    green = sum(1 for i in ingredient_visuals if i["color"] == "GREEN")

    if red > 0:
        status = "🔴 Unsafe"
    elif yellow > 0:
        status = "🟡 Warning"
    else:
        status = "🟢 Safe"

    return {
        "dish_status": status,
        "red": red,
        "yellow": yellow,
        "green": green
    }


# ============================
# System Wide Dashboard Summary
# ============================

def system_dashboard_summary(all_knowledge):
    overused = 0
    expired = 0
    qc_failures = 0
    unsafe_batches = 0

    for k in all_knowledge:
        freshness = k["freshness"]
        quantity = k["quantity"]

        if freshness["status"] == "Expired":
            expired += 1
            unsafe_batches += 1

        if quantity["status"] == "Overused":
            overused += 1

    return {
        "Total Overused Ingredients": overused,
        "Expired Stock": expired,
        "Unsafe Batches": unsafe_batches,
        "QC Failures": qc_failures
    }


# ============================
# Pretty Output Helpers
# ============================

def visual_to_text(v):
    return f"""
Ingredient: {v['name']}
Status: {v['label']}
Quantity: {v['quantity']['status']}
Alerts: {', '.join(v['alerts']) if v['alerts'] else 'None'}
""".strip()


def dashboard_to_text(d):
    return f"""
📊 SYSTEM SAFETY DASHBOARD

Total Overused Ingredients: {d['Total Overused Ingredients']}
Expired Stock: {d['Expired Stock']}
Unsafe Batches: {d['Unsafe Batches']}
QC Failures: {d['QC Failures']}
""".strip()


# ============================
# Main Public API for this Module
# ============================

def generate_visual_alerts(all_knowledge):
    """
    Called after embeddings are built.

    Input:
        all_knowledge -> list of knowledge dictionaries from embeddings.py

    Output:
        visuals   -> list of ingredient-level visual alerts
        dashboard -> system-level safety summary
    """
    visuals = [build_visual_alert(k) for k in all_knowledge]
    dashboard = system_dashboard_summary(all_knowledge)

    return visuals, dashboard
