from flask import request, url_for
from markupsafe import Markup

# Minimal line-icon set (20x20, stroke-based) so the sidebar has no icon
# library dependency. Keys match the third argument passed to nav_link().
_ICONS = {
    "grid": '<path stroke-linecap="round" stroke-linejoin="round" d="M4 4h5v5H4V4zm7 0h5v5h-5V4zM4 11h5v5H4v-5zm7 0h5v5h-5v-5z"/>',
    "user": '<path stroke-linecap="round" stroke-linejoin="round" d="M10 10a3 3 0 100-6 3 3 0 000 6zm-6 7c0-3 2.5-5 6-5s6 2 6 5"/>',
    "calendar": '<path stroke-linecap="round" stroke-linejoin="round" d="M4 5h12v11H4V5zm0 3h12M7 3v3m6-3v3"/>',
    "receipt": '<path stroke-linecap="round" stroke-linejoin="round" d="M5 3h10v14l-2-1.3L11 17l-2-1.3L7 17l-2-1.3V3zM7 7h6M7 10h6"/>',
    "tag": '<path stroke-linecap="round" stroke-linejoin="round" d="M11 3H5a2 2 0 00-2 2v6l8 8 6-6-8-8z"/><circle cx="7" cy="7" r="1"/>',
    "bed": '<path stroke-linecap="round" stroke-linejoin="round" d="M3 16v-6a2 2 0 012-2h10a2 2 0 012 2v6M3 16v1M17 16v1M3 12h14M6 9V6"/>',
    "pill": '<path stroke-linecap="round" stroke-linejoin="round" d="M6.5 13.5l7-7a3.5 3.5 0 114.95 4.95l-7 7a3.5 3.5 0 01-4.95-4.95zM9 11l4-4"/>',
    "flask": '<path stroke-linecap="round" stroke-linejoin="round" d="M8 3h4M8.5 3v5L5 15a1.5 1.5 0 001.3 2.2h7.4A1.5 1.5 0 0015 15l-3.5-7V3"/>',
    "users": '<path stroke-linecap="round" stroke-linejoin="round" d="M13 17c0-2.2-1.8-4-4-4s-4 1.8-4 4M9 10a2.5 2.5 0 100-5 2.5 2.5 0 000 5zm5.5 7c0-1.7-1.3-3.2-3-3.7M13.5 9.7A2.5 2.5 0 1012 5.2"/>',
    "chart": '<path stroke-linecap="round" stroke-linejoin="round" d="M4 16V9m4.5 7V4m4.5 12v-5m4.5 5V7"/>',
    "vitals": '<path stroke-linecap="round" stroke-linejoin="round" d="M2 10h3l1.5-4L9 15l2-9 1.5 4H18"/>',
    "queue": '<circle cx="6" cy="6" r="1.6"/><circle cx="6" cy="14" r="1.6"/><path stroke-linecap="round" stroke-linejoin="round" d="M10 6h6M10 10h6M10 14h6"/>',
    "ledger": '<path stroke-linecap="round" stroke-linejoin="round" d="M5 3h10v14H5V3zm3 4h4m-4 3h4m-4 3h2"/>',
}


def nav_link(endpoint, label, icon):
    is_active = request.blueprint == endpoint.split(".")[0]
    base_classes = "nav-item flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors"
    state_classes = (
        "bg-brand-50 text-brand-700"
        if is_active
        else "text-muted hover:bg-canvas hover:text-ink"
    )
    icon_svg = (
        f'<svg class="w-5 h-5 shrink-0" viewBox="0 0 20 20" fill="none" '
        f'stroke="currentColor" stroke-width="1.75">{_ICONS.get(icon, "")}</svg>'
    )
    return Markup(
        f'<a href="{url_for(endpoint)}" class="{base_classes} {state_classes}">'
        f'{icon_svg}<span class="nav-label whitespace-nowrap">{label}</span></a>'
    )
