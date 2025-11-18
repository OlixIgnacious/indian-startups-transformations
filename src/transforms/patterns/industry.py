INDUSTRY_PATTERNS_ORDERED = [
    (r"\bed[\s\-]?tech\b", "edtech"),
    (r"\b(edutech|edutech|edu tech)\b", "edtech"),  # extra safety
    (r"\bfin[\s\-]?tech\b|\bfinancial\b|\bfinance\b", "fintech"),
    (r"\bb2b[\s\-]?e[\s\-]?commerce\b|\be[\s\-]?commerce\b", "ecommerce"),
    # SaaS/Tech must be specific: match 'saas' or 'technology provider' or 'tech provider' NOT bare 'tech'
    (r"\bsaas\b|\btechnology\s*provider\b|\btech\s*provider\b", "saas_tech"),
    (r"\bfood\b|\bbeverage\b", "food_beverage"),
    (r"\bagri[\s\-]?tech\b|\bagritech\b", "agritech"),
    (r"\bhealth\b", "healthtech"),
    (r"\btransport(ation)?\b", "transport"),
    (r"\blifestyle\b", "lifestyle"),
    (r"\bhospital\b|\bhospitality\b", "hospitality"),
    (r"\badvertis", "advertising"),
    (r"\bdigital\b", "digital"),
    (r"\bdairy\b", "dairytech"),
    (r"\bsupply\s*chain\b", "supply_chain"),
] 