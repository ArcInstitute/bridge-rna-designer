from bridge_rna_designer.classes import WTBridgeRNA177nt
from bridge_rna_designer import errors

def design_bridge_rna(target: str, donor: str) -> WTBridgeRNA177nt:
    """
    Design a bridge RNA from a target and donor sequence.
    Args:
        target: The target sequence (14 bp).
        donor: The donor sequence (14 bp).
    Returns:
        WTBridgeRNA177nt: A bridge RNA object.
    """
    # Convert input sequences to uppercase
    target = target.upper()
    donor = donor.upper()

    # Check input
    WTBridgeRNA177nt.check_target_length(target)
    WTBridgeRNA177nt.check_donor_length(donor)
    WTBridgeRNA177nt.check_core_match(target, donor)
    WTBridgeRNA177nt.check_target_is_dna(target)
    WTBridgeRNA177nt.check_donor_is_dna(donor)

    # Design bridge RNA
    brna = WTBridgeRNA177nt()
    brna.update_target(target)
    brna.update_donor(donor)
    brna.update_hsg()

    return brna

