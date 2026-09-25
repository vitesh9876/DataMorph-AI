from typing import Dict, Any

TEMPLATES_CONFIG: Dict[str, Dict[str, Any]] = {
    "professional": {
        "name": "Professional",
        "primary_color": "#1E3A8A", # Deep Navy
        "accent_color": "#3B82F6",  # Royal Blue
        "font_family": "Inter, sans-serif",
        "header_bg": "#F8FAFC",
        "card_border": "1px solid #E2E8F0"
    },
    "minimal": {
        "name": "Minimal",
        "primary_color": "#0F172A", # Slate 900
        "accent_color": "#64748B",  # Slate 500
        "font_family": "system-ui, -apple-system, sans-serif",
        "header_bg": "#FFFFFF",
        "card_border": "1px solid #F1F5F9"
    },
    "modern": {
        "name": "Modern",
        "primary_color": "#6366F1", # Indigo
        "accent_color": "#8B5CF6",  # Violet
        "font_family": "Outfit, sans-serif",
        "header_bg": "linear-gradient(135deg, #EEF2FF 0%, #F5F3FF 100%)",
        "card_border": "1px solid #E0E7FF"
    },
    "corporate": {
        "name": "Corporate",
        "primary_color": "#0369A1", # Sky Blue
        "accent_color": "#0284C7",
        "font_family": "Arial, Helvetica, sans-serif",
        "header_bg": "#F0F9FF",
        "card_border": "1px solid #BAE6FD"
    },
    "research": {
        "name": "Research",
        "primary_color": "#334155", # Academic Charcoal
        "accent_color": "#0D9488",  # Teal
        "font_family": "Georgia, serif",
        "header_bg": "#F8FAFC",
        "card_border": "1px solid #CBD5E1"
    }
}
