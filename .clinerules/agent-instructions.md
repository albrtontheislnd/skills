# Agent Instructions for Generating Skills

When generating or executing a Skill, follow these workspace and output rules.

## Save generated files in the workspace root

For each Skill, save every file created during Skill execution in a dedicated subfolder at the **workspace root**—the folder currently open in the Hermes project. Do **not** write generated files into the Skill's source directory or any of its subdirectories.

- Create the output subfolder when it does not already exist.
- Ask the user for the output-subfolder name, or suggest a suitable name and use it once confirmed by the workflow.
- Keep generated reports, data, intermediate artifacts, and other execution outputs in that subfolder.
- Preserve existing output files unless the Skill explicitly requires replacing them.

## Resolve the workspace path

Determine the workspace root from the process working directory. The default workspace path is:

```python
import os

workspace_root = os.getcwd()
```

Use the resolved workspace root—not the Skill directory—as the base for the output subfolder.

## Reject unresolved placeholders

Before creating the output folder or running the Skill, validate the resolved workspace path. If the path still looks like an unfilled placeholder because it contains both `<` and `>`, refuse to run and request a real workspace path.

```python
if "<" in workspace_root and ">" in workspace_root:
    raise ValueError(
        "Refusing to run: the workspace path is an unfilled placeholder."
    )
```

Do not attempt to create files or directories until this validation succeeds.
