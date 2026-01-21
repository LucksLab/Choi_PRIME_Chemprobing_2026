def set_transparency_except(res_list):
    """
    Set transparency to 0.7 for chain A except for specified residues (set to 0).
    If res_list is empty, reset all transparency in chain A to 0.
    """

    chain_sel = "chain A"

    # If empty → reset all to 0 for chain A
    if len(res_list) == 0:
        cmd.set("transparency", 0, chain_sel)
        cmd.set("cartoon_transparency", 0, chain_sel)
        cmd.set("sphere_transparency", 0, chain_sel)
        cmd.set("stick_transparency", 0, chain_sel)
        print("Reset all transparency to 0 for chain A.")
        return

    # 1. Set entire chain A to 0.7
    cmd.set("transparency", 0.7, chain_sel)
    cmd.set("cartoon_transparency", 0.7, chain_sel)
    cmd.set("sphere_transparency", 0.7, chain_sel)
    cmd.set("stick_transparency", 0.7, chain_sel)

    # 2. Set selected residues back to opacity (0)
    for r in res_list:
        sel = f"chain A and resi {r}"
        cmd.set("transparency", 0, sel)
        cmd.set("cartoon_transparency", 0, sel)
        cmd.set("sphere_transparency", 0, sel)
        cmd.set("stick_transparency", 0, sel)

    print(f"Set chain A transparency to 0.7; residues {res_list} set to 0.")

def show_basepair_hbonds(res1, res2, chain='A'):
    """
    Draw H-bond (distance) lines between two residues in a nucleic acid.
    
    Usage:
        show_basepair_hbonds(165, 200)              # same chain A
        show_basepair_hbonds(24, 43, chain='B')     # both in chain B
        show_basepair_hbonds(10, 50, chain='A')
    """

    sel1 = f"chain {chain} and resi {res1} and name N*+O*"
    sel2 = f"chain {chain} and resi {res2} and name N*+O*"

    obj_name = f"hb_{chain}_{res1}_{res2}"

    cmd.dist(obj_name, sel1, sel2, mode=2, cutoff=3.6)

    # optional styling
    cmd.hide("labels", obj_name)
    cmd.set("dash_width", 2.0, obj_name)
    cmd.set("dash_gap", 0.3, obj_name)
    cmd.set("dash_color", "yellow", obj_name)

    print(f"Added base-pair H-bonds between residues {res1} and {res2} in chain {chain}.")

def clear_all_hbonds():
    """
    Deletes all H-bond distance objects created by show_basepair_hbonds().
    Looks for objects with names starting with 'hb_'.
    """

    obj_list = cmd.get_names("objects")

    removed = 0
    for obj in obj_list:
        if obj.startswith("hb_"):
            cmd.delete(obj)
            removed += 1

    print(f"Removed {removed} H-bond objects.")