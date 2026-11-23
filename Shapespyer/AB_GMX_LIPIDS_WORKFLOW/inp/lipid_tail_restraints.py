#!/usr/bin/env python3
"""
Add 'tail-alignment' restraints to a diacyl phospholipid topology (Gromacs .itp).

Usage:
    python lipid_tail_restraints.py <lipid.itp> <lipid_PRB.itp>

The two acyl tails are found from the molecular graph (the [ bonds ] section), so
the result does not depend on atom order or atom names in the input topology:

  * N        - the (single) nitrogen atom of the choline head-group;
  * 'tail'   - the chain of heavy atoms from an ester carbonyl C to a terminal CH3;
  * position - the index of a tail atom counted from its carbonyl C (carbonyl C = 1).

Restraints (bonded type 10 'restraint potential': low, up1, up2, k - in nm and
kJ/mol/nm^2) are appended at the end of the [ bonds ] section:

  1. N - terminal C of each tail;          2.4-2.6 nm for a 16-carbon tail,
                                           +0.125 nm per extra carbon
  2. terminal C - terminal C of the tails; 0.4-0.6 nm
  3. same-position tail atoms (positions 16, 14, 12, 10) 0.4-0.6 nm,
     skipping the pair already restrained by (2).

For DPPC (two 16-carbon tails) this reproduces exactly the six restraints
in ../../GMX_DPPC_Tails/toppar/DPPC_PRB.itp.
"""

import re
import sys
from collections import deque

# element by rounded mass (the .itp [ atoms ] section has no element column)
ELEMENTS = {1: "H", 12: "C", 14: "N", 16: "O", 31: "P"}

NTAIL_BOUNDS = (2.4, 2.6)  # N - terminal C, 16-carbon tail (nm)
NTAIL_EXTRA = 0.125  # per extra carbon beyond 16 (nm)
PAIR_BOUNDS = (0.4, 0.6)  # tail - tail (nm)
UPPER2, FORCE = 1000.00, 1000.00
POSITIONS = (16, 14, 12, 10)


def read_itp(lines):
    """Return atoms {nr: (name, element)} and bonds [(i, j)] from the topology lines."""
    atoms, bonds, section = {}, [], ""
    for line in lines:
        text = line.split(";")[0].split()
        if not text:
            continue
        if text[0].startswith("["):
            section = line.split(";")[0].strip("[] \n")
            continue
        if section == "atoms":
            atoms[int(text[0])] = (text[4], ELEMENTS.get(round(float(text[7])), "X"))
        elif section == "bonds" and text[2] == "1":
            bonds.append((int(text[0]), int(text[1])))
    return atoms, bonds


def find_tails(atoms, bonds):
    """Return N atom number and two tails (lists of atom numbers, carbonyl C first)."""
    heavy = {nr for nr, (_, el) in atoms.items() if el != "H"}
    nbrs = {nr: set() for nr in heavy}
    for i, j in bonds:
        if i in heavy and j in heavy:
            nbrs[i].add(j)
            nbrs[j].add(i)
    elem = {nr: atoms[nr][1] for nr in heavy}

    nitrogens = [nr for nr in heavy if elem[nr] == "N"]
    # terminal CH3 on a tail: one heavy neighbour and not an N-methyl of the head-group
    ends = sorted(
        nr for nr in heavy
        if elem[nr] == "C" and len(nbrs[nr]) == 1 and elem[next(iter(nbrs[nr]))] != "N"
    )
    # ester carbonyl C: bonded to a terminal (=O) oxygen
    carbonyls = {
        nr for nr in heavy
        if elem[nr] == "C" and any(elem[k] == "O" and len(nbrs[k]) == 1 for k in nbrs[nr])
    }
    if len(nitrogens) != 1 or len(ends) != 2 or len(carbonyls) != 2:
        raise ValueError(
            f"Expected 1 N, 2 terminal CH3 and 2 carbonyl C, found N={nitrogens}, "
            f"CH3={ends}, C=O={sorted(carbonyls)} - not a diacyl phospholipid?"
        )

    tails = []
    for end in ends:  # shortest path from the terminal C to the nearest carbonyl C
        prev, queue = {end: None}, deque([end])
        while queue:
            nr = queue.popleft()
            if nr in carbonyls:
                break
            for k in sorted(nbrs[nr]):
                if k not in prev:
                    prev[k] = nr
                    queue.append(k)
        path = []  # following the BFS parents leads from the carbonyl C to the terminal C
        while nr is not None:
            path.append(nr)
            nr = prev[nr]
        tails.append(path)
    return nitrogens[0], tails


def restraint_lines(atoms, nitrogen, tails):
    """Format the restraints as [ bonds ] entries (type 10) with atom names as comments."""
    def line(i, j, low, up1):
        return (f"{i:7d}{j:7d}   10     {low:g}  {up1:g}  {UPPER2:.2f}  {FORCE:.2f}"
                f"  ; {atoms[i][0]} - {atoms[j][0]}")

    out = []
    for tail in tails:  # N - terminal C, longer tails are allowed a larger distance
        shift = NTAIL_EXTRA * (len(tail) - 16)
        out.append(line(nitrogen, tail[-1], round(NTAIL_BOUNDS[0] + shift, 3),
                        round(NTAIL_BOUNDS[1] + shift, 3)))
    out.append(line(tails[0][-1], tails[1][-1], *PAIR_BOUNDS))
    for pos in POSITIONS:
        if pos <= min(len(tails[0]), len(tails[1])):
            pair = (tails[0][pos - 1], tails[1][pos - 1])
            if pair != (tails[0][-1], tails[1][-1]):
                out.append(line(*pair, *PAIR_BOUNDS))
    return out


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 1
    with open(argv[1]) as fin:
        lines = fin.readlines()
    atoms, bonds = read_itp(lines)
    nitrogen, tails = find_tails(atoms, bonds)
    block = [
        "; Tail-alignment restraints (bonded type 10 'restraint potential': low up1 up2 k)\n"
    ] + [text + "\n" for text in restraint_lines(atoms, nitrogen, tails)] + ["\n"]

    # insert at the end of [ bonds ], i.e. before the next directive
    start = next(i for i, ln in enumerate(lines) if re.match(r"\s*\[\s*bonds\s*\]", ln))
    stop = next(
        (i for i in range(start + 1, len(lines)) if lines[i].lstrip().startswith("[")),
        len(lines),
    )
    while lines[stop - 1].strip() == "":  # keep the block attached to the last bond
        stop -= 1
    lines[stop:stop] = ["\n"] + block[:-1]
    with open(argv[2], "w") as fout:
        fout.writelines(lines)

    print(f"{argv[1]}: tails of {len(tails[0])} and {len(tails[1])} carbons, "
          f"{len(block) - 2} restraints written to {argv[2]}")
    print("".join(block[1:-1]), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
