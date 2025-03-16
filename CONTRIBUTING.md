# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/shoumikchow/bbox-visualizer/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

### Write Documentation

bbox-visualizer could always use more documentation, whether as part of the
official bbox_visualizer docs, in docstrings, or even on the web in blog posts,
articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/shoumikchow/bbox-visualizer/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

## Get Started!

Ready to contribute? Here's how to set up `bbox_visualizer` for local development.

1. Fork the `bbox_visualizer` repo on GitHub.

2. Clone your fork locally:
    ```bash
    git clone git@github.com:your_name_here/bbox_visualizer.git
    ```

3. Install uv if you haven't already:
    ```bash
    pip install uv
    ```

4. Set up your development environment:
    ```bash
    cd bbox_visualizer
    uv venv
    uv pip install -e ".[dev]"
    ```

5. Create a branch for local development:
    ```bash
    git checkout -b name-of-your-bugfix-or-feature
    ```

6. Make your changes. Don't forget to add tests!

7. Format and lint your code:
    ```bash
    # Format with ruff
    uv run ruff format .
    
    # Run linting checks with ruff
    uv run ruff check .
    
    # Auto-fix ruff issues where possible
    uv run ruff check --fix .
    
    # Run tests
    uv run pytest
    ```

8. Commit your changes and push your branch to GitHub:
    ```bash
    git add .
    git commit -m "Your detailed description of your changes."
    git push origin name-of-your-bugfix-or-feature
    ```

9. Submit a pull request through the GitHub website.

## Git Workflow

### Feature Development

1. Create feature branch from dev:
    ```bash
    git checkout dev
    git pull origin dev
    git checkout -b name-of-your-bugfix-or-feature
    ```

2. Make your changes and follow the code quality steps above (formatting, linting, testing)

3. Create a Pull Request from your feature branch to dev

4. After your feature PR is merged to dev, create a PR from dev to master:
   - Always use "Rebase and merge" option when merging to master
   - This keeps the history clean and linear

### Syncing Branches

If GitHub shows that branches are out of sync or you can't use "Rebase and merge":

1. Create a PR from master to dev on GitHub:
   - Base branch: `dev`
   - Compare branch: `master`
   - Title: "Sync dev with master"

2. If there are conflicts, resolve them locally:
    ```bash
    # Switch to dev branch
    git checkout dev
    
    # Get latest changes
    git fetch origin
    
    # Try to merge master (this will show conflicts)
    git merge origin/master
    
    # Resolve conflicts in your editor
    # Then commit the resolved changes
    git add .
    git commit -m "Resolve conflicts from master sync"
    git push origin dev
    ```

3. Merge the PR on GitHub once conflicts are resolved

This workflow:
- Maintains PR history for all changes
- Makes branch synchronization trackable
- Provides clear context for conflict resolutions
- Keeps main development in dev branch
- Maintains clean history in master

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated:
   * Add your new functionality into a function with a docstring
   * Update the README.md with any new usage instructions
3. The pull request should work for Python 3.8 and above.
4. Make sure all tests pass and the code is formatted and linted with ruff.

## Development Tools

This project uses modern Python development tools:

* **uv**: Fast Python package installer and resolver
* **ruff**: Fast Python linter and formatter
* **pytest**: Testing framework

All development dependencies are specified in the `pyproject.toml` file and will be installed when you install the package with the `[dev]` extra.