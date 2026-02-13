#!/usr/bin/env python3.11
"""
Plot DWUCK4 cross sections for energy scan (Ex=3,4,5,6 MeV) using AK optical models
"""

import numpy as np
import plotly.graph_objects as go
import re

def parse_dwuck4_output(filename):
    """Parse DWUCK4 output file to extract cross sections"""
    angles = []
    cross_sections = []
    
    with open(filename, 'r') as f:
        content = f.read()
    
    # Find the cross section data block
    # Look for lines with angle data after "Theta Inelsig"
    in_data = False
    for line in content.split('\n'):
        if 'Theta Inelsig' in line:
            in_data = True
            continue
        if in_data:
            # Data lines have format: angle, cross_section, ...
            parts = line.split()
            if len(parts) >= 2:
                try:
                    angle = float(parts[0])
                    xs = float(parts[1])
                    # Check if it's scientific notation
                    if 'E' in parts[1] or 'e' in parts[1]:
                        angles.append(angle)
                        cross_sections.append(xs)
                    else:
                        # Regular number
                        angles.append(angle)
                        cross_sections.append(xs)
                except (ValueError, IndexError):
                    # End of data or invalid line
                    if len(angles) > 0:
                        break
    
    return np.array(angles), np.array(cross_sections)

# Parse all AK output files
files = {
    'Ex=3.0 MeV': 'outputs/DW_36S_DP_AK_ex300_0f52.out',
    'Ex=4.0 MeV': 'outputs/DW_36S_DP_AK_ex400_0f52.out',
    'Ex=5.0 MeV': 'outputs/DW_36S_DP_AK_ex500_0f52.out',
    'Ex=6.0 MeV': 'outputs/DW_36S_DP_AK_ex600_0f52.out',
}

colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']

fig = go.Figure()

for (label, filename), color in zip(files.items(), colors):
    angles, xs = parse_dwuck4_output(filename)
    
    if len(angles) > 0:
        fig.add_trace(go.Scatter(
            x=angles,
            y=xs,
            mode='lines',
            name=label,
            line=dict(width=2.5, color=color),
            hovertemplate='<b>%{fullData.name}</b><br>' +
                         'θ = %{x:.1f}°<br>' +
                         'σ = %{y:.3e} mb/sr<br>' +
                         '<extra></extra>'
        ))
        print(f"{label}: {len(angles)} data points, range {angles[0]:.1f}° to {angles[-1]:.1f}°")

# Update layout
fig.update_layout(
    title=dict(
        text='<b>³⁶S(d,p)³⁷S Cross Sections: Excitation Energy Scan</b><br>' +
             '<sub>0f₅/₂ orbital, AK optical models (An & Cai + Koning & Delaroche)</sub>',
        x=0.5,
        xanchor='center',
        font=dict(size=18)
    ),
    xaxis=dict(
        title='<b>Angle (degrees)</b>',
        titlefont=dict(size=14),
        showgrid=True,
        gridcolor='lightgray',
        range=[0, 60]
    ),
    yaxis=dict(
        title='<b>Cross Section (mb/sr)</b>',
        titlefont=dict(size=14),
        type='log',
        showgrid=True,
        gridcolor='lightgray'
    ),
    plot_bgcolor='white',
    width=1000,
    height=700,
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bgcolor='rgba(255,255,255,0.8)',
        bordercolor='gray',
        borderwidth=1,
        font=dict(size=12)
    ),
    hovermode='closest'
)

# Save plot
output_html = 'outputs/energy_scan_AK_0f52.html'
output_png = 'outputs/energy_scan_AK_0f52.png'

fig.write_html(output_html)
fig.write_image(output_png, width=1000, height=700)

print(f"\nPlot saved to:")
print(f"  - {output_html}")
print(f"  - {output_png}")
