import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

LLM_CACHE = {}

def _cache_key(prefix:str, payload:dict) -> str:
    return prefix + ":" + json.dumps(payload, sort_keys=True)

def generate_reconciliation_reasoning(patient_context: dict, best_source: dict, all_sources: list) -> str:
    payload = {
        'patient_context': patient_context,
        'best_source': best_source,
        'all_sources': all_sources
    }
    key = _cache_key("reconcile", payload)

    if key in LLM_CACHE:
        return LLM_CACHE[key]
    
    prompt = f"""
You are a clinical data reconciliation assistant.

A rule-based system has already selected the most likely medication record.
Your job is to explain the decision clearly and cautiously.

- Avoid definitive clinical recommendations
- Use cautious language when interpreting patient context
- Do not infer treatment decisions beyond the data provided
- Avoid implying dosing guidance unless explicitly supported by the provided data

Patient context:
{json.dumps(patient_context, indent=2)}

Selected record:
{json.dumps(best_source, indent=2)}

All conflicting records:
{json.dumps(all_sources, indent=2)}

Write 2-4 sentences explaining:
1. why the selected record is reasonable
2. how recency and source reliability influenced the choice
3. any uncertainty or follow-up that would still be appropriate

Do not invent facts.
Keep it concise and readable for a clinician.
"""
    try: 
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
        )
        text = response.output_text.strip()
        LLM_CACHE[key] = text
        return text
    except Exception as e:
        print("OpenAI API error:", e)
        fallback = (
            f"AI reasoning is temporarily unavailable: {str(e)}."
            "The result was still produced using rule-based reconciliation logic."
        )
        LLM_CACHE[key] = fallback
        return fallback
    
def review_data_quality_with_llm(record: dict, rule_issues: list) -> dict:
    payload = {
        'record': record,
        'rule_issues': rule_issues
    }
    key = _cache_key("validate", payload)

    if key in LLM_CACHE:
        return LLM_CACHE[key]
    
    prompt = f"""
You are a clinical data quality review assistant.

A rule-based system has already identified potential issues.
Your role is to explain these findings clearly and cautiously.

IMPORTANT:
- Do NOT assume missing data is incorrect
- Use cautious language such as "may indicate", "could suggest", or "should be verified"
- Do NOT make definitive clinical claims
- Do NOT provide medical advice
- Focus only on data quality, not treatment decisions

Patient record:
{json.dumps(record, indent=2)}

Rule-detected issues:
{json.dumps(rule_issues, indent=2)}

Write a short summary (2–4 sentences) that:
1. Explains the most important issues
2. Highlights any potential concerns
3. Emphasizes uncertainty and need for verification

Then return JSON in this format:
{{
  "summary": "your summary here",
  "additional_issues": []
}}

Only include additional_issues if clearly supported by the data.
"""
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
        )
        text = response.output_text.strip()
        parsed = json.loads(text)
        LLM_CACHE[key] = parsed
        return parsed
    except Exception:
        fallback = {
            "summary": "AI review is temporarily unavailable. Rule-based validation was still completed successfully.",
            "additional_issues": []
        }
        LLM_CACHE[key] = fallback
        return fallback