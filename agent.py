import re
from typing import List

def normalize_metric(metric: str, company: str) -> str:
    m = metric.lower()
    if m in ["r&d", "rd"]:
        return "research and development expenses"
    if m == "cloud":
        if company.lower() == "microsoft":
            return "intelligent cloud revenue"
        elif company.lower() == "google":
            return "google cloud revenue"
        else:
            return "data center revenue"
    if m == "operating margin":
        return "operating income as a percentage of revenue"
    return metric

def decompose_query(query: str) -> List[str]:
    q = query.lower()
    companies = ["Microsoft", "Google", "NVIDIA"]

    years = re.findall(r"(20\d{2})", q)
    year_nums = [int(y) for y in years]

    metric_match = re.search(
        r"(operating margin|gross margin|revenue|r&d|cloud|data center|ai)",
        q,
    )
    metric = metric_match.group(1) if metric_match else "financials"

    subqs = []

    # Multi-company, multi-year
    if "each company" in q or "all three" in q or "across" in q:
        if len(year_nums) >= 2:
            y1, y2 = year_nums[0], year_nums[-1]
            for c in companies:
                for y in range(y1, y2 + 1):
                    m = normalize_metric(metric, c)
                    subqs.append(f"{c} {m} {y}")
            return subqs
        elif len(year_nums) == 1:
            for c in companies:
                m = normalize_metric(metric, c)
                subqs.append(f"{c} {m} {year_nums[0]}")
            return subqs

    # Single company growth
    company_match = re.search(r"(microsoft|google|nvidia)", q)
    if company_match and len(year_nums) >= 2:
        c = company_match.group(1).capitalize()
        y1, y2 = year_nums[0], year_nums[1]
        m = normalize_metric(metric, c)
        return [f"{c} {m} {y1}", f"{c} {m} {y2}"]

    # Cross-company comparison
    if "compare" in q or "which company" in q:
        if year_nums:
            for c in companies:
                m = normalize_metric(metric, c)
                subqs.append(f"{c} {m} {year_nums[0]}")
        else:
            for c in companies:
                m = normalize_metric(metric, c)
                subqs.append(f"{c} {m}")
        return subqs

    return [query]
