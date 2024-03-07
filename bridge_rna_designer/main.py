import click
import sys
from bridge_rna_designer import errors, run
from bridge_rna_designer.classes import WTBridgeRNA177nt

@click.group(invoke_without_command=True)
@click.option('--target', '-t', required=True)
@click.option('--donor', '-d', required=True)
@click.option('--output-format', '-of', default='stockholm', type=click.Choice(['stockholm', 'fasta']))
@click.pass_context
def cli(ctx, target, donor, output_format):
    if ctx.invoked_subcommand is None:
        ctx.invoke(default_command, target=target, donor=donor, output_format=output_format)

@cli.command()
@click.pass_context
def default_command(ctx, target, donor, output_format):

    target = target.upper()
    donor = donor.upper()

    try:
        WTBridgeRNA177nt.check_target_length(target)
    except errors.TargetLengthError as e:
        print("ERROR:", e)
        print("Exiting...")
        sys.exit()

    try:
        WTBridgeRNA177nt.check_donor_length(donor)
    except errors.DonorLengthError as e:
        print("ERROR:", e)
        print("Exiting...")
        sys.exit()

    try:
        WTBridgeRNA177nt.check_core_match(target, donor)
    except errors.CoreMismatchError as e:
        print("ERROR:", e)
        print("Exiting...")
        sys.exit()

    try:
        WTBridgeRNA177nt.check_target_is_dna(target)
    except errors.TargetNotDNAError as e:
        print("ERROR:", e)
        print("Exiting...")
        sys.exit()

    try:
        WTBridgeRNA177nt.check_donor_is_dna(donor)
    except errors.DonorNotDNAError as e:
        print("ERROR:", e)
        print("Exiting...")
        sys.exit()

    brna = run.design_bridge_rna(target, donor)
    if output_format == "fasta":
        print(brna.format_fasta())
    elif output_format == "stockholm":
        print(brna.format_stockholm())


if __name__ == '__main__':
    cli()
