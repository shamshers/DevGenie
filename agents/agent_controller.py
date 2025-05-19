from agents.planner_agent import plan
from agents.coder_agent import generate_code
from agents.reviewer_agent import review_code
from agents.explainer_agent import explain_code

def handle_user_request(user_prompt, rag_chain):
    tasks = plan(user_prompt)
    response = {}
    code_for_review = ""
    for task in tasks:
        if task['type'] == 'code_generation':
            code = generate_code(task['content'], rag_chain)
            response['code'] = code
            code_for_review = code
        elif task['type'] == 'review':
            code_to_review = response.get('code', task['content'])
            issues, fixed_code = review_code(code_to_review, rag_chain)
            response['issues'] = issues
            if fixed_code and fixed_code.lower() != 'no change needed':
                response['fixed_code'] = fixed_code
                code_for_review = fixed_code
        elif task['type'] == 'explain':
            code_to_explain = response.get('fixed_code', response.get('code', task['content']))
            explanation = explain_code(code_to_explain, rag_chain)
            response['explanation'] = explanation
    return response
