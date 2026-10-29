# Rebuild the unpublished S candidate

Python standard library only. Extract into an empty directory, then run:

    python3 -B implementation/skill-presentation/prepare.py --rebuild-from . --output ../rebuilt

Compare every output with SHA256SUMS. No Git, network, App source or credentials
are required. This rebuild does not authorize publication or installation.
