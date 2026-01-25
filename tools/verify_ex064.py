#!/usr/bin/env python3.11
"""
Verify ex064 input files and create comparison plots.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def parse_dwuck4_output(filename):
    """Extract angle and cross section from DWUCK4 output."""
    angles = []
    cross_sections = []
    
    with open(filename, 'r') as f:
        for line in f:
            if len(line.strip()) > 0:
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        angle = float(parts[0])
                        if 'E' in parts[1] or 'e' in parts[1]:
                            xsec = float(parts[1])
                            angles.append(angle)
                            cross_sections.append(xsec)
                    except (ValueError, IndexError):
                        continue
    
    return np.array(angles), np.array(cross_sections)

# Parse ex064 outputs
angles_ak_ex064, xsec_ak_ex064 = parse_dwuck4_output('outputs/DW_36S_DP_AK_EX064.out')
angles_qp_ex064, xsec_qp_ex064 = parse_dwuck4_output('outputs/DW_36S_DP_QP_EX064.out')

# Parse GS outputs for comparison
angles_ak_gs, xsec_ak_gs = parse_dwuck4_output('outputs/DW_36S_DP_AK_GS_corrected.out')
angles_qp_gs, xsec_qp_gs = parse_dwuck4_output('outputs/DW_36S_DP_QP_GS_corrected.out')

print(f"Ex064 AK: {len(angles_ak_ex064)} points, range {angles_ak_ex064.min():.1f}° to {angles_ak_ex064.max():.1f}°")
print(f"Ex064 QP: {len(angles_qp_ex064)} points, range {angles_qp_ex064.min():.1f}° to {angles_qp_ex064.max():.1f}°")

# Create comparison plot
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        'Ex064 (645 keV, 1p₃/₂) - AK vs QP',
        'Ground State (0 keV, 0f₇/₂) - AK vs QP',
        'Ratio AK/QP - Ex064',
        'Ratio AK/QP - GS'
    ),
    vertical_spacing=0.12,
    horizontal_spacing=0.10
)

# Ex064 cross sections
fig.add_trace(
    go.Scatter(
        x=angles_ak_ex064, y=xsec_ak_ex064,
        mode='lines', name='AK',
        line=dict(color='#FFD700', width=2.5),
        legendgroup='ak', showlegend=True
    ),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(
        x=angles_qp_ex064, y=xsec_qp_ex064,
        mode='lines', name='QP',
        line=dict(color='#00CED1', width=2.5, dash='dash'),
        legendgroup='qp', showlegend=True
    ),
    row=1, col=1
)

# GS cross sections (truncated to 60°)
mask_gs = angles_ak_gs <= 60
fig.add_trace(
    go.Scatter(
        x=angles_ak_gs[mask_gs], y=xsec_ak_gs[mask_gs],
        mode='lines', name='AK',
        line=dict(color='#FFD700', width=2.5),
        legendgroup='ak', showlegend=False
    ),
    row=1, col=2
)

mask_gs_qp = angles_qp_gs <= 60
fig.add_trace(
    go.Scatter(
        x=angles_qp_gs[mask_gs_qp], y=xsec_qp_gs[mask_gs_qp],
        mode='lines', name='QP',
        line=dict(color='#00CED1', width=2.5, dash='dash'),
        legendgroup='qp', showlegend=False
    ),
    row=1, col=2
)

# Ratios
xsec_qp_ex064_interp = np.interp(angles_ak_ex064, angles_qp_ex064, xsec_qp_ex064)
ratio_ex064 = xsec_ak_ex064 / xsec_qp_ex064_interp

xsec_qp_gs_interp = np.interp(angles_ak_gs, angles_qp_gs, xsec_qp_gs)
ratio_gs = xsec_ak_gs / xsec_qp_gs_interp

fig.add_trace(
    go.Scatter(
        x=angles_ak_ex064, y=ratio_ex064,
        mode='lines', line=dict(color='#9370DB', width=2),
        showlegend=False
    ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
        x=angles_ak_gs, y=ratio_gs,
        mode='lines', line=dict(color='#9370DB', width=2),
        showlegend=False
    ),
    row=2, col=2
)

# Add horizontal lines at ratio=1
fig.add_hline(y=1.0, line_dash="dot", line_color="gray", opacity=0.5, row=2, col=1)
fig.add_hline(y=1.0, line_dash="dot", line_color="gray", opacity=0.5, row=2, col=2)

# Update axes
for col in [1, 2]:
    fig.update_xaxes(title_text="Angle (degrees)", range=[0, 60], row=2, col=col)
    fig.update_xaxes(range=[0, 60], row=1, col=col)
    fig.update_yaxes(title_text="dσ/dΩ (mb/sr)", type="log", row=1, col=col)
    fig.update_yaxes(title_text="Ratio", row=2, col=col)

fig.update_layout(
    title={
        'text': '³⁶S(d,p)³⁷S @ 16 MeV - Ex064 vs Ground State Comparison',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 18}
    },
    height=900,
    width=1400,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(size=13),
    legend=dict(
        x=0.98, y=0.98,
        xanchor='right', yanchor='top',
        bgcolor='rgba(255,255,255,0.9)',
        bordercolor='black', borderwidth=1
    )
)

fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

# Save
fig.write_image('outputs/ex064_vs_GS_comparison.png', width=1400, height=900, scale=2)
fig.write_html('outputs/ex064_vs_GS_comparison.html')

print("\nPlot saved to:")
print("  - outputs/ex064_vs_GS_comparison.png")
print("  - outputs/ex064_vs_GS_comparison.html")

# Statistics
print(f"\n=== EX064 (645 keV, 1p₃/₂) ===")
print(f"AK: min={xsec_ak_ex064.min():.4e}, max={xsec_ak_ex064.max():.4e}, mean={xsec_ak_ex064.mean():.4e}")
print(f"QP: min={xsec_qp_ex064.min():.4e}, max={xsec_qp_ex064.max():.4e}, mean={xsec_qp_ex064.mean():.4e}")
print(f"Ratio: min={ratio_ex064.min():.3f}, max={ratio_ex064.max():.3f}, mean={ratio_ex064.mean():.3f}")

print(f"\n=== GROUND STATE (0 keV, 0f₇/₂) - 0-60° only ===")
print(f"AK: min={xsec_ak_gs[mask_gs].min():.4e}, max={xsec_ak_gs[mask_gs].max():.4e}, mean={xsec_ak_gs[mask_gs].mean():.4e}")
print(f"QP: min={xsec_qp_gs[mask_gs_qp].min():.4e}, max={xsec_qp_gs[mask_gs_qp].max():.4e}, mean={xsec_qp_gs[mask_gs_qp].mean():.4e}")
print(f"Ratio: min={ratio_gs[mask_gs].min():.3f}, max={ratio_gs[mask_gs].max():.3f}, mean={ratio_gs[mask_gs].mean():.3f}")

print(f"\n=== COMPARISON ===")
print(f"Ex064 mean cross section (AK): {xsec_ak_ex064.mean():.4e} mb/sr")
print(f"GS mean cross section (AK, 0-60°): {xsec_ak_gs[mask_gs].mean():.4e} mb/sr")
print(f"Ratio Ex064/GS (AK): {xsec_ak_ex064.mean() / xsec_ak_gs[mask_gs].mean():.3f}")
