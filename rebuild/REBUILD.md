# Finite S1.2.1 release rebuild inputs

Python 3 standard library only; no Git, network, constructor or App is required.
Inspect the finite input inventory, extract into an empty directory, then run:

    python3 -B implementation/aligned-release/prepare.py --rebuild-from . --public-release --output ../s-1.2.1-rebuilt

Compare plugin ZIP, rebuild ZIP, distribution.json and selection.json against
SKILLS-SHA256SUMS. The supplied public generator is a recorded release adaptation
of the byte-exact candidate generator under provenance/. The93 canonical inputs,
selection and six reused packaging inputs remain exact. It applies existing
operative Apache-2.0 S terms and current release authority, preserving historical
legal evidence. Publication and actual installation/native/customer acceptance
are separately observed operations; issue228 remains open.
