#!/usr/bin/env python3
"""
Parse DWUCK4 run output and create interactive Plotly plots.
Usage:
  python tools/plot_dwuck.py --input outputs/run_output.txt --out outputs/dwuck_plot.html
  python tools/plot_dwuck.py --input outputs/run_output.txt --out outputs/dwuck_plot.html --ref reference.csv --fit

Reference CSV expected columns: theta, obs (comma-separated, header optional)
Fit option: simple linear fit obs = a*model + b (least-squares)
"""
import re
import argparse
import csv
from pathlib import Path
import numpy as np


def parse_output(path):
    """Parse the DWUCK4 textual output and return a list of data series.
    Each series is a dict: { 'title': str, 'theta': np.array, 'y': np.array }
    The parser searches for table headers containing 'Theta' and then numeric rows.
    """
    series = []
    header_re = re.compile(r'Theta', re.IGNORECASE)
    data_re = re.compile(r'^\s*([+-]?[0-9]+(?:\.[0-9]*)?)\s+([+-]?[0-9Ee.+-]+)')

    text = Path(path).read_text()
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if header_re.search(line):
            # collect subsequent lines that look like data rows
            j = i+1
            thetas = []
            ys = []
            # sometimes header is followed by a label row we should skip; scan until numeric lines
            while j < len(lines):
                m = data_re.match(lines[j])
                if m:
                    # parse repeatedly until we hit a non-data line or blank
                    while j < len(lines):
                        m2 = data_re.match(lines[j])
                        if not m2:
                            break
                        try:
                            theta = float(m2.group(1))
                            y = float(m2.group(2))
                        except Exception:
                            break
                        thetas.append(theta)
                        ys.append(y)
                        j += 1
                    break
                else:
                    j += 1
            if thetas:
                # build a title from the nearest preceding non-empty line that looks like a case label
                title = ''
                # search backward for a descriptive line (e.g., that contains reaction name) up to 6 lines
                for k in range(max(0, i-6), i):
                    if lines[k].strip() and not lines[k].strip().startswith('0'):
                        title = lines[k].strip()
                        break
                if not title:
                    title = f'Series starting line {i+1}'
                series.append({'title': title, 'theta': np.array(thetas), 'y': np.array(ys)})
                i = j
                continue
        i += 1
    return series


def read_reference_csv(path):
    p = Path(path)
    thetas = []
    obs = []
    with p.open() as f:
        reader = csv.reader(f)
        # try to detect header: if first row has non-numeric entries, skip
        first = next(reader, None)
        if first is None:
            return np.array([]), np.array([])
        def is_numeric(s):
            try:
                float(s)
                return True
            except Exception:
                return False
        if not is_numeric(first[0]):
            # header; attempt to use remaining rows
            for row in reader:
                if not row: continue
                thetas.append(float(row[0]))
                obs.append(float(row[1]))
        else:
            # first row numeric
            thetas.append(float(first[0]))
            obs.append(float(first[1]))
            for row in reader:
                if not row: continue
                thetas.append(float(row[0]))
                obs.append(float(row[1]))
    return np.array(thetas), np.array(obs)


def fit_model(model_theta, model_y, ref_theta, ref_y):
    """Fit a simple linear transform ref = a*model + b using least squares.
    Interpolate model to reference theta points, then solve for a,b.
    Returns (a,b), and fitted_model_at_ref
    """
    from scipy.interpolate import interp1d
    from numpy.linalg import lstsq
    interp = interp1d(model_theta, model_y, kind='linear', bounds_error=False, fill_value='extrapolate')
    model_at_ref = interp(ref_theta)
    A = np.vstack([model_at_ref, np.ones_like(model_at_ref)]).T
    x, *_ = lstsq(A, ref_y, rcond=None)
    a, b = x[0], x[1]
    fitted = a * model_at_ref + b
    return (a, b), model_at_ref, fitted


def plot_series(series_list, out_html, ref_file=None, do_fit=False):
    import plotly.graph_objects as go
    fig = go.Figure()
    colors = [None] * len(series_list)

    for idx, s in enumerate(series_list):
        theta = s['theta']
        y = s['y']
        name = s['title']
        fig.add_trace(go.Scatter(x=theta, y=y, mode='markers+lines', name=name))

    fit_results = None
    if ref_file:
        ref_theta, ref_y = read_reference_csv(ref_file)
        fig.add_trace(go.Scatter(x=ref_theta, y=ref_y, mode='markers', name='Reference', marker=dict(symbol='x', size=8, color='black')))
        if do_fit and series_list:
            # fit the first series by default; user can change
            model = series_list[0]
            (a, b), model_at_ref, fitted = fit_model(model['theta'], model['y'], ref_theta, ref_y)
            fig.add_trace(go.Scatter(x=ref_theta, y=fitted, mode='lines', name=f'Fit (a={a:.4g}, b={b:.4g})', line=dict(dash='dash')))
            fit_results = {'a': float(a), 'b': float(b)}

    fig.update_layout(title='DWUCK4 Results', xaxis_title='Theta (deg)', yaxis_title='Value', template='plotly_white')
    Path(out_html).parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(out_html, include_plotlyjs='cdn')
    return fit_results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', required=True, help='DWUCK4 output text file')
    parser.add_argument('--out', '-o', default='outputs/dwuck_plot.html', help='Output HTML file')
    parser.add_argument('--ref', '-r', help='Reference CSV file (theta,obs)')
    parser.add_argument('--fit', action='store_true', help='Fit model to reference data (linear scaling + offset)')
    args = parser.parse_args()

    series = parse_output(args.input)
    if not series:
        print('No series found in input. Exiting.')
        return
    print(f'Found {len(series)} series; plotting first {min(5,len(series))} series.')
    fit_res = plot_series(series[:5], args.out, ref_file=args.ref, do_fit=args.fit)
    print('Plot saved to', args.out)
    if fit_res:
        print('Fit results:', fit_res)


if __name__ == '__main__':
    main()
