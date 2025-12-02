#!/usr/bin/env python3
"""
Create DWUCK4-style .DAT input files (single or multiple cases).

Features:
- Interactive mode to prompt for case fields
- JSON config input with one or more cases
- --sample writes a reasonable example case

Usage examples:
  python tools/make_dat.py --out inputs/custom.DAT --sample
  python tools/make_dat.py --out inputs/custom.DAT --interactive
  python tools/make_dat.py --out inputs/custom.DAT --json mycases.json

JSON format:
[{
  "code": "1011000030000000",
  "title": "O16(D,P)O17  D3/2+   ...",
  "angles": {"n":55, "start":0.0, "step":3.3334},
  "l_line": [16,1,2,3],
  "drf_rmax": {"drf": 0.10, "rmax": 15.0},
  "body_lines": ["+12.    +02.    +01.", "+01.    -85.3  +01.25  +00.606"]
}]

The script produces a DW4-style block for each case; body_lines should contain the remaining card lines specific to your case.
"""

from pathlib import Path
import argparse
import json


def format_header(code: str, title: str) -> str:
    # code (16 chars) then 4 spaces then title padded
    code = code.strip()
    code = code[:16].ljust(16)
    title = title.strip()
    return f"{code}    {title}\n"


def format_angles(n: float, start: float, step: float) -> str:
    # Use F8.4 fixed-width fields so Fortran formatted reads (F8.4) succeed
    return f"{float(n):8.4f}{float(start):8.4f}{float(step):8.4f}\n"


def format_l_line(nums) -> str:
    # Format as 18I3: up to 18 integers, each width 3 (right-justified)
    parts = []
    for v in nums:
        parts.append(f"{int(v):3d}")
    # pad to a reasonable length if needed
    return ''.join(parts) + "\n"


def format_drf_rmax(drf: float, rmax: float) -> str:
    # Use F8.4 fixed-width fields for floats (matches many DWUCK card formats)
    return f"{float(drf):8.4f}{float(rmax):8.4f}\n"


def build_case(case: dict) -> str:
    out = ''
    out += format_header(case.get('code', '0000000000000000'), case.get('title', 'DWUCK4 CASE'))
    ang = case.get('angles', {})
    out += format_angles(ang.get('n', 55), ang.get('start', 0.0), ang.get('step', 3.3334))
    # L line
    l_line = case.get('l_line')
    if l_line:
        out += format_l_line(l_line)
    # DRF and RMAX
    dr = case.get('drf_rmax')
    if dr:
        out += format_drf_rmax(dr.get('drf', 0.1), dr.get('rmax', 15.0))
    # Optional additional body lines
    for line in case.get('body_lines', []):
        out += line.rstrip() + '\n'
    # blank line separator
    out += '\n'
    return out


def interactive_case():
    print('Interactive DWUCK4 .DAT case creator — press enter to accept defaults')
    code = input('Case code (16 digits) [1011000030000000]: ') or '1011000030000000'
    title = input('Title/description [O16(D,P)O17  D3/2+ UNBOUND STRIPPING]: ') or 'O16(D,P)O17  D3/2+ UNBOUND STRIPPING'
    n = input('Number of theta points (n) [55]: ') or '55'
    start = input('Theta start [0.0]: ') or '0.0'
    step = input('Theta step [3.3334]: ') or '3.3334'
    lnums = input('L line numbers separated by commas (e.g. 16,1,2,3) [16,1,2,3]: ') or '16,1,2,3'
    drf = input('DRF [0.10]: ') or '0.10'
    rmax = input('RMAX [15.0]: ') or '15.0'
    print('Enter additional card lines for the case body. Enter a blank line to finish.')
    body = []
    while True:
        line = input()
        if line.strip() == '':
            break
        body.append(line)
    try:
        lnums_list = [int(x) for x in lnums.split(',') if x.strip()]
    except Exception:
        lnums_list = [16,1,2,3]
    case = {
        'code': code,
        'title': title,
        'angles': {'n': float(n), 'start': float(start), 'step': float(step)},
        'l_line': lnums_list,
        'drf_rmax': {'drf': float(drf), 'rmax': float(rmax)},
        'body_lines': body
    }
    return case


def load_json(path: Path):
    raw = json.loads(path.read_text())
    # if it's a single dict, wrap
    if isinstance(raw, dict):
        raw = [raw]
    return raw


def sample_case():
    # Provide a fully runnable example (taken from the bundled test cases).
    return {
        'code': '1011000030000000',
        'title': 'FE56(P,P)FE56* L=3-     SPIN ORBIT = OPTION 4',
        'angles': {'n': 37.0, 'start': 0.0, 'step': 5.0},
        'l_line': [15,2,3,3],
        'drf_rmax': {'drf': 0.1000, 'rmax': 15.0},
        'body_lines': [
            '+22.5000+01.0078+01.0000+56.0000+26.0000+01.2500+00.0000+00.0000+01.0000',
            '+04.    -28.2   +01.25  +00.735 +00.    +00.    +01.25  +00.735 +00.',
            '+01.0000-46.3800+01.2500+00.7350+00.    +00.0000+01.2500+00.7350+00.0000',
            '-02.0000+00.0000+01.2500+00.4370+00.0000+61.4000+01.2500+00.4370+00.0000',
            '-04.4999+01.0078+01.0000+56.0000+26.0000+01.2500+00.0000+00.0000+01.0000',
            '+04.    -28.2   +01.25  +00.735 +00.    +00.    +01.25  +00.735 +00.',
            '+01.0000-46.3800+01.2500+00.7350+00.    +00.0000+01.2500+00.7350+00.0000',
            '-02.0000+00.0000+01.2500+00.4370+00.0000+61.4000+01.2500+00.4370+00.0000',
            '+00.0000+01.0000+00.0000+56.0000+26.0000+01.2500+00.0000+00.0000+00.0000',
            '+02.0000-46.3800+01.2500+00.7350+00.    +00.0000+01.2500+00.7350+00.0000',
            '-03.0000+00.0000+01.2500+00.4370+00.0000+61.4000+01.2500+00.4370+00.0000',
            '+00.0000+01.0000+00.0000+56.0000+26.0000+01.2500+00.0000+00.0000+00.0000',
            '+11.0000-46.3800+01.2500+00.7350+00.    +00.0000+01.2500+00.7350+00.0000',
            '+00.10    +03.',
            '-12.0000+00.0000+01.2500+00.4370+00.0000+61.4000+01.2500+00.4370+00.0000',
            '+00.10  +03.'
        ]
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out', '-o', default='inputs/custom.DAT', help='Output .DAT file')
    p.add_argument('--interactive', action='store_true', help='Run interactive prompt to build a case')
    p.add_argument('--json', help='JSON file with one or more case specs')
    p.add_argument('--sample', action='store_true', help='Write a sample case (non-interactive)')
    p.add_argument('--append', action='store_true', help='Append to existing file instead of overwriting')
    args = p.parse_args()

    cases = []
    if args.sample:
        cases.append(sample_case())
    elif args.json:
        cases = load_json(Path(args.json))
    elif args.interactive:
        cases.append(interactive_case())
    else:
        print('No input mode selected. Use --sample, --json FILE, or --interactive. Exiting.')
        return

    out_path = Path(args.out)
    if not args.append:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text('')

    mode = 'a' if args.append else 'w'
    with out_path.open(mode) as f:
        for c in cases:
            block = build_case(c)
            f.write(block)

    print(f'Wrote {len(cases)} case(s) to {out_path}')

if __name__ == '__main__':
    main()
