# Finite Skills rebuild inputs

Inspect the complete input inventory and extract into an empty directory.
Python3 standard library only; no Git, constructor, network or App required.

For the retained local technical view:

    python3 -B implementation/aligned-release/prepare.py --rebuild-from . --output ../aligned-technical

For the owner-approved public1.1.0 legal overlay:

    python3 -B implementation/aligned-release/prepare.py --rebuild-from . --public-release --output ../s-1.1.0-rebuilt

Use a new output outside the input tree, with no symlink ancestors. Compare the
four selected-route S artifacts and SKILLS-SHA256SUMS with the reviewed original.
The technical route retains canonical legal evidence; the public route applies
the exact approved Apache/NOTICE copies and current five-path owner approval.
A combined private App/S SHA256SUMS contains additional private files and differs
from the standalone S checksum list. No App inputs or archives are included here.
These commands build files only; publication, plugin update, installation and
actual host/customer acceptance remain separate operations and evidence.
