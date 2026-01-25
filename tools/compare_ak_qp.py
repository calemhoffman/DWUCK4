#!/usr/bin/env python3.11
"""
Compare DWUCK4 calculations using AK vs QP optical model parameters.
CORRECTED VERSION with proper conversion factors.
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

# Parse both output files
angles_ak, xsec_ak = parse_dwuck4_output('outputs/DW_36S_DP_AK_GS_corrected.out')
angles_qp, xsec_qp = parse_dwuck4_output('outputs/DW_36S_DP_QP_GS_corrected.out')
angles_old_ak, xsec_old_ak = parse_dwuck4_output('outputs/DW_36S_DP_AK_GS.out')
angles_old_qp, xsec_old_qp = parse_dwuck4_output('outputs/DW_36S_DP_QP_GS.out')

print(f"AK Corrected: {len(angles_ak)} points, range {angles_ak.min():.1f}° to {angles_ak.max():.1f}°")
print(f"QP Corrected: {len(angles_qp)} points, range {angles_qp.min():.1f}° to {angles_qp.max():.1f}°")

# Create comparison plot
fig = make_subplots(
    rows=2, cols=1,
    row_heights=[0.7, 0.3],
    vertical_spacing=0.1,
    subplot_titles=(
        'Cross Section Comparison (Corrected Conversion Factors)',
        'Ratio AK/QP'
    )
)

# Top panel: Corrected cross sections
fig.add_trace(
    go.Scatter(
        x=angles_ak,
        y=xsec_ak,
        mode='lines',
        name='AK Corrected (Wsᵢ×4asᵢ, Vso×4)',
        line=dict(color='#FFD700', width=3),
        legendgroup='ak'
    ),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(
        x=angles_qp,
        y=xsec_qp,
        mode='lines',
        name='QP Corrected (Wsᵢ×4asᵢ, Vso×4)',
        line=dict(color='#00CED1', width=3, dash='dash'),
        legendgroup='qp'
    ),
    row=1, col=1
)

# Add old (wrong) values for comparison
fig.add_trace(
    go.Scatter(
        x=angles_old_ak,
        y=xsec_old_ak,
        mode='lines',
        name='AK Old (WRONG factors)',
        line=dict(color='#FFD700', width=1, dash='dot'),
        opacity=0.4,
        showlegend=True
    ),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(
        x=angles_old_qp,
        y=xsec_old_qp,
        mode='lines',
        name='QP Old (WRONG factors)',
        line=dict(color='#00CED1', width=1, dash='dot'),
        opacity=0.4,
        showlegend=True
    ),
    row=1, col=1
)

# Bottom panel: Ratio
xsec_qp_interp = np.interp(angles_ak, angles_qp, xsec_qp)
ratio = xsec_ak / xsec_qp_interp

fig.add_trace(
    go.Scatter(
        x=angles_ak,
        y=ratio,
        mode='lines',
        name='Ratio',
        line=dict(color='#9370DB', width=2),
        showlegend=False
    ),
    row=2, col=1
)

# Add horizontal line at ratio=1
fig.add_hline(y=1.0, line_dash="dot", line_color="gray", opacity=0.5, row=2, col=1)

# Update layout
fig.update_xaxes(title_text="Angle (degrees)", row=2, col=1, range=[0, 90])
fig.update_xaxes(range=[0, 90], row=1, col=1)
fig.update_yaxes(title_text="dσ/dΩ (mb/sr)", type="log", row=1, col=1)
fig.update_yaxes(title_text="Ratio", row=2, col=1)

fig.update_layout(
    title={
        'text': '³⁶S(d,p)³⁷S @ 16 MeV - Ground State (0f₇/₂)<br><sub>Corrected Optical Model Comparison</sub>',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 20}
    },
    height=900,
    width=1100,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(size=14),
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bgcolor='rgba(255,255,255,0.9)',
        bordercolor='black',
        borderwidth=1
    )
)

# Update grid
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

# Save
fig.write_image('outputs/AK_vs_QP_comparison_CORRECTED.png', width=1100, height=900, scale=2)
fig.write_html('outputs/AK_vs_QP_comparison_CORRECTED.html')

print("\nPlot saved to:")
print("  - outputs/AK_vs_QP_comparison_CORRECTED.png")
print("  - outputs/AK_vs_QP_comparison_CORRECTED.html")

# Print statistics
print(f"\n=== CORRECTED VERSION ===")
print(f"AK: min={xsec_ak.min():.4e}, max={xsec_ak.max():.4e}, mean={xsec_ak.mean():.4e}")
print(f"QP: min={xsec_qp.min():.4e}, max={xsec_qp.max():.4e}, mean={xsec_qp.mean():.4e}")
print(f"Ratio: min={ratio.min():.3f}, max={ratio.max():.3f}, mean={ratio.mean():.3f}")

print(f"\n=== OLD (WRONG) VERSION ===")
print(f"AK: min={xsec_old_ak.min():.4e}, max={xsec_old_ak.max():.4e}, mean={xsec_old_ak.mean():.4e}")
print(f"QP: min={xsec_old_qp.min():.4e}, max={xsec_old_qp.max():.4e}, mean={xsec_old_qp.mean():.4e}")
ratio_old = xsec_old_ak / np.interp(angles_old_ak, angles_old_qp, xsec_old_qp)
print(f"Ratio: min={ratio_old.min():.3f}, max={ratio_old.max():.3f}, mean={ratio_old.mean():.3f}")

print(f"\n=== IMPACT OF CORRECTION ===")
print(f"AK change factor: {(xsec_ak.mean() / xsec_old_ak.mean()):.3f}x")
print(f"QP change factor: {(xsec_qp.mean() / xsec_old_qp.mean()):.3f}x")
