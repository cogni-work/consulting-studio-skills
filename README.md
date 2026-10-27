# Consulting Studio Skills

> **🧪 Testing phase has started**
>
> Try a small task with fictional or sanitized material and tell us what works or
> needs improvement in [GitHub issues](https://github.com/cogni-work/consulting-studio-skills/issues).
> See the [testing status and limitations](AUDIT.md#testing-status-and-limitations).

Consulting Studio helps consultants turn a client need into a clear proposal,
an evidence-based answer and a useful deliverable. It provides reusable methods
for understanding buyers, planning engagements, researching questions, checking
claims, communicating findings and learning from completed work. You keep the
business decisions and review the results.

Use it to turn interview notes into a buyer brief, test the evidence behind a
recommendation, draft a proposal with clear scope and inputs, or shape findings
for a board presentation. The aim is more time for understanding clients,
exercising judgement and helping people make sound decisions.

This free, open-source **skills-only plugin** includes **27 consulting methods**
and three supporting entries: **Setup**, **Workspace Librarian** and **Resume**.

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

**[Download the 0.1.0 plugin ZIP](https://github.com/cogni-work/consulting-studio-skills/releases/download/v0.1.0/consulting-studio-skills-0.1.0-plugin.zip)**
or browse the [release and source packages](https://github.com/cogni-work/consulting-studio-skills/releases/tag/v0.1.0).
Use the plugin ZIP for upload; the repository ZIP contains source and rebuild
material.

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

Saved settings and continuity need an accessible storage tool and your permission.
If earlier work is unavailable, provide it again; the plugin does not create
automatic memory or a shared document store. Keep client material, personal notes
and firm knowledge within their permitted audiences.

## Updates and help

Check [releases](https://github.com/cogni-work/consulting-studio-skills/releases)
for updates. Keep your previous package and your settings or adaptations. For a
manually uploaded plugin, OpenAI documents **Upload new version** on the plugin's
details when available and permitted. Review the changes and try affected work
in a fresh conversation. Automatic updates and restoration of an earlier version
are not guaranteed; replacing a package cannot undo work already sent or saved.

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

## Need a GUI, managed setup or custom adaptations?

The free package includes the consulting methods and their resources for direct
use. If you want a project interface, guided installation and training, or
adaptations for your firm, [visit cogni-work.ai](https://www.cogni-work.ai/)
to discuss the scope and prerequisites.
