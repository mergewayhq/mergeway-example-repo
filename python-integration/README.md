# Python Integration Example

This example follows the `mergeway` getting started flow against the
blog-style repository in this workspace.

It does three things:

1. connects to `../mergeway.yaml`
2. generates typed Python models from the Mergeway schema
3. runs a launch retrospective workflow in a temporary copy of the repository

The workflow reads the existing users, posts, tags, and comments, then
demonstrates CRUD and repository operations by:

- creating a new author
- promoting that author with a merge update
- creating a new tag, post, and comment
- validating and formatting the repository
- exporting a summary snapshot
- deleting the temporary objects again

Run it with:

```bash
cd python-integration
uv run main.py
```

If you want to run it inside a managed environment instead, `pyproject.toml`
also points `uv` at the sibling `mergeway-python` checkout directory.
