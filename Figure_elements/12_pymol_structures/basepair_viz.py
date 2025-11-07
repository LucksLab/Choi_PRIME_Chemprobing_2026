from pymol import cmd

def show_base_pair(res1, res2, res3=None, chain='A', show_stack = False):
    """
    Highlights up to 3 residues involved in base pairing in PyMOL.

    Args:
        res1 (int or str): First residue number
        res2 (int or str): Second residue number
        res3 (int or str, optional): Optional third residue number
        chain (str): Chain ID (default = 'A')
    """

    cmd.delete(all)
    cmd.reinitialize()
    cmd.fetch("1gid")
    

    # Build selection string
    res_list = [str(res1), str(res2)]
    if res3 is not None:
        res_list.append(str(res3))
    res_str = "+".join(res_list)
    selection = f"(resi {res_str} and chain {chain})"
    cmd.select("bp", selection)

    # Display styles\
    cmd.hide("everything", "all")
    cmd.show("sticks", "bp")

    # Color each base
    colors = ['skyblue', 'deepsalmon', 'gold']
    for i, res in enumerate(res_list):
        cmd.color(colors[i], f"resi {res} and chain {chain}")

    # Optional: draw H-bonds between all pairs
    if len(res_list) >= 2:
        cmd.dist("hbonds1", f"resi {res_list[0]} and chain {chain}", f"resi {res_list[1]} and chain {chain}", mode=2)
    if len(res_list) == 3:
        cmd.dist("hbonds2", f"resi {res_list[0]} and chain {chain}", f"resi {res_list[2]} and chain {chain}", mode=2)
        cmd.dist("hbonds3", f"resi {res_list[1]} and chain {chain}", f"resi {res_list[2]} and chain {chain}", mode=2)
    cmd.hide("labels", "hbonds*")
    cmd.set("dash_width", 2)


    # Show stacked neighbors (res ±1)
    if show_stack:
        stack_residues = set()
        for r in res_list:
            try:
                r_int = int(r)
                stack_residues.add(str(r_int - 1))
                stack_residues.add(str(r_int + 1))
            except ValueError:
                continue
        stack_str = "+".join(stack_residues)
        cmd.select("stacking_sel", f"chain {chain} and resi {stack_str}")
        cmd.show("sticks", "stacking_sel")
        cmd.color("wheat", "stacking_sel")


    # Label with offset using C1' for cleaner placement
    cmd.set("label_position", [2.0, 1.0, 0.0])  # Adjust vector as needed
    for res in res_list:
        cmd.label(f"resi {res} and chain {chain} and name O5'", f'"{res}"')
    # Final styling
    cmd.bg_color("white")
    cmd.orient("bp")
    cmd.zoom("bp", 2)

def highlight_base_atoms(chain='A'):
    """
    Highlights N1 of adenines and N3 of cytosines with spheres.
    """

    # Select and show N1 of adenines
    cmd.select("N1_A", f"(bp and chain {chain} and resn A and name N1)")
    cmd.color("orange", "N1_A")

    # Select and show N3 of cytosines
    cmd.select("N3_C", f"(bp and chain {chain} and resn C and name N3)")
    cmd.color("cyan", "N3_C")


def render_ray(out="basepair_render.png", width=1200, height=900, dpi=300):
    """
    Renders the current PyMOL scene using ray tracing and saves it as a PNG.

    Parameters:
        out (str): Output filename (should end in .png)
        width (int): Width in pixels
        height (int): Height in pixels
        dpi (int): Dots per inch (for high-res figures)
    """
    cmd.bg_color("white")           # Ensure white background
    cmd.set("ray_opaque_background", 0)  # Transparent background if desired
    cmd.set("antialias", 2)
    cmd.set("ray_trace_mode", 1)    # Smooth rendering
    cmd.set("ray_trace_fog", 0)     # No fog for clarity
    cmd.set("ambient", 0.5)         # Softer shading

    cmd.ray(width, height)
    cmd.png(out, dpi=dpi)
    print(f"Rendered image saved as {out}")