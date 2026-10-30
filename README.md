# Consulting Studio Skills

> **S1.2.2 is owner-tested and accepted for the documented scope.**
>
> The owner successfully used Setup and a bounded problem-framing workflow with
> Astra, including fresh reads of settings and required references, and accepted S
> as ready for use. See [tested scope and remaining unknowns](AUDIT.md#testing-status-and-limitations).
> Feedback and improvements continue through [GitHub issues](https://github.com/cogni-work/consulting-studio-skills/issues).

Consulting Studio helps consultants turn a client need into a clear proposal,
an evidence-based answer and a useful deliverable. It provides reusable methods
for understanding buyers, planning engagements, researching questions, checking
claims, communicating findings and learning from completed work. You keep the
business decisions and review the results.

Use it to turn interview notes into a buyer brief, test the evidence behind a
recommendation, draft a proposal with clear scope and inputs, or shape findings
for a board presentation. The aim is more time for understanding clients,
exercising judgement and helping people make sound decisions.

Consulting Studio combines **9 consulting processes**, **27 reusable business
skills** and **37 data types**. Together, they provide practical methods and a
shared structure for clients, projects, knowledge and decisions, from client needs
and proposals through delivery and learning. Learn more here:
[cogni-work.ai](https://cogni-work.ai/).

## Who it is for

Consultants and consulting firms comfortable installing and maintaining their own
AI tools. For the installation route below, you need a ChatGPT workspace that
supports plugins and plugin ZIP uploads, with upload access or an eligible owner
or administrator who can help you.

You can begin with notes or documents you are allowed to use. Saved firm settings
are optional. Web research, access to stored files, saving work and creating or
inspecting artifacts depend on the tools available in your ChatGPT workspace;
this plugin does not supply those tools or grant access to your data. The model
must be able to read each selected skill's bundled instructions and resources.

## Download and install

**[Download the 1.2.2 plugin ZIP](https://github.com/cogni-work/consulting-studio-skills/releases/download/v1.2.2/consulting-studio-skills.zip)**
or browse the [release and source packages](https://github.com/cogni-work/consulting-studio-skills/releases/tag/v1.2.2).
Upload `consulting-studio-skills.zip` without unpacking or renaming it. The
repository ZIP contains source and documentation; the rebuild ZIP contains finite
build inputs. Before upload, compare the downloaded installer with the release's
`SHA256SUMS`. Its SHA-256 is:

```text
b929d367b7c1a9e96a9eaffbc6fbc2815d75bd488e581416873816219ae09ded
```

For example, run `shasum -a 256 consulting-studio-skills.zip` on macOS or
`sha256sum consulting-studio-skills.zip` on Linux from the download directory.

OpenAI documents this route for eligible owners and administrators on **ChatGPT
web**, when the upload option is available:

1. Open **Admin console**, select the intended workspace and open **Plugins**.
2. Select **Add**, then **Upload plugin**, and upload the plugin ZIP.
3. Make the plugin available to its intended users under your workspace's plugin
   policy.
4. In ChatGPT's **Plugins** directory, open your workspace's Consulting Studio
   entry and select **Install plugin** if shown.
5. Select Consulting Studio in a conversation using an **@ mention** or the
   composer's **Plugins** control.

See OpenAI's [plugin upload and workspace instructions](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt).
If the upload option is missing, ask your workspace administrator about
availability and access. A GitHub download alone does not install the plugin.

This repository distributes a plugin package; it is not a listing in OpenAI's
public plugin directory. It contains no marketplace catalog, so importing this
repository as a GitHub marketplace is not the installation route for this release.

## Try it

After selecting Consulting Studio in a conversation, try this with fictional
material:

> Help me frame a consulting question from these notes: a transit operator's
> ridership has fallen; the sponsor thinks unreliable service is the cause;
> the board wants options in ten weeks. Separate facts from assumptions, suggest
> a manageable scope and list the evidence we need next. Use only these notes.

You can then ask for a research brief, proposal, delivery plan or review of a
draft. Supply the relevant material and say who the output is for. You do not
need to know method names or complete a setup project first. Check sources,
assumptions and recommendations before using the result with a client.

## Optional setup and returning to work

These three entries have different jobs. Ask for the one you need in plain
language:

| Entry | Use it to |
| --- | --- |
| Setup | Agree firm preferences, methods, templates, output styles and where work belongs. Start with existing standards and choose any changes. |
| Workspace Librarian | Find the authoritative source or destination for the current task using accessible locations and permissions. |
| Resume | Read accessible saved work, explain what is present and still open, and suggest one next step. It does not restart actions or save changes. |

To get started with firm preferences, ask: “Set up Consulting Studio for our
work. Read our existing standards first and propose only the choices still
missing.” You can also begin ordinary work directly with the example above.

To check the selected installation, ask: “Run Installation prüfen for this
Consulting Studio installation. Agree one small fictional workflow and report
which installed instructions, required references and settings you could read.”
This is a bounded check of your installation; it does not test all methods or
other users' access. See [the qualification plan](INSTALL-TEST-PLAN.md) for broader
checks when needed.

To return to saved work, provide its link or accessible file and ask: “Resume
this work: explain what is present, what is open and one useful next step.” Resume
reads and proposes; continuing or saving work requires the relevant instruction.

Saved settings and continuity need an accessible storage tool and your permission.
If earlier work is unavailable, provide it again; the plugin does not create
automatic memory or a shared document store. Keep client material, personal notes
and firm knowledge within their permitted audiences.

## Updates and help

Check [releases](https://github.com/cogni-work/consulting-studio-skills/releases)
for updates. Future candidates may be supplied separately as ZIPs; a candidate
delivery does not promise or automatically trigger a public release. Each public
release is a deliberate maintainer decision.

Keep your previous package and your settings or adaptations. Compare the new
version, release notes and checksums before adopting it. For a manually uploaded
plugin, OpenAI documents [**Upload new version**](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt)
on the plugin's details when available and permitted. After an authorized update,
start a fresh conversation, run Installation prüfen and try the affected work.
Check that the changed instructions and required resources are actually readable;
a displayed version alone is insufficient. Update and recovery have not yet been
qualified by the documented owner test. Automatic updates and restoration of an
earlier version are not guaranteed; replacing a package cannot undo work already
sent or saved.

Report bugs or ask questions in [GitHub issues](https://github.com/cogni-work/consulting-studio-skills/issues)
using a fictional or sanitized example. For suspected vulnerabilities, contact
**stephan@cogni-work.ai** privately. Do not include client data or credentials.
This free package includes no personal support commitment or response deadline.

## License and technical notes

Distributed under [Apache License 2.0](https://github.com/cogni-work/consulting-studio-skills/blob/main/LICENSE).
Retain the license and [NOTICE attribution](https://github.com/cogni-work/consulting-studio-skills/blob/main/NOTICE)
when redistributing. The license's warranty and liability terms apply.

For package structure, source attribution, reproducible builds and release history,
see the [technical notes](AUDIT.md).

## Open S methods and controlled M workflows

Free S is useful on its own: open consulting methods, complete required resources
and provider-neutral handoffs for direct use with your available, authorized tools.
Source fidelity, visible limitations and basic correctness are requirements for
both S and M. Necessary resources and known critical corrections are not withheld
to encourage a paid upgrade.

M includes everything in S, plus programmatic checks for more reliable execution
and centrally maintained Excel calculations. Maintain assumptions centrally,
trace calculations and check results before reuse.

These capabilities support controlled workflows with inspectable check evidence,
a project interface, integration and scoped care. The included capabilities and
their availability must be agreed and demonstrated for the selected workflow and
environment. Guided installation and training support that use; firm-specific
adaptations are separately scoped as L.

The public S1.2.2 package does not contain the separately developed executable
validator, project-model adapters or workbook. A private test candidate or a
successful local check is not a public release, a native ChatGPT delivery gate or
proof of an integrated M workflow. See [known limits](KNOWN-LIMITS.md).

Existing Apache-2.0 rights remain unchanged. Rights and terms for any separately
delivered commercial components require their own review and agreement.
[Visit cogni-work.ai](https://www.cogni-work.ai/) to discuss the scope,
prerequisites and currently available support.
