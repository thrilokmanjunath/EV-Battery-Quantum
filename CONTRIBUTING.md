# Contributing to EV Battery Quantum

Thank you for your interest in contributing to the **EV Battery Quantum** project! We welcome all contributions, from bug reports to new features and documentation improvements.

## 🌿 Branching Strategy

We follow a standard feature-branch workflow:

1. **`main`**: The primary branch. It always contains stable, production-ready code.
2. **Feature branches**: Create a new branch from `main` for your work. Use a descriptive naming convention:
   - `feature/your-feature-name`
   - `bugfix/issue-description`
   - `docs/what-you-documented`

```bash
git checkout -b feature/awesome-new-optimization
```

## ✅ Pull Request Requirements

When you are ready to submit your changes, please open a Pull Request (PR) against the `main` branch. Ensure your PR meets the following criteria:

- **Descriptive Title & Summary**: Clearly explain what the PR does and why it is needed.
- **Pass Continuous Integration (CI)**: All automated tests, type checking, and linting must pass before the PR can be merged.
- **Code Reviews**: At least one approved review from a maintainer is required.
- **Test Coverage**: New features must include appropriate unit or integration tests.

## 🪝 Setting up Pre-Commit Hooks

We use `pre-commit` to ensure code quality and formatting consistency (e.g., using `black`, `ruff`, or `mypy`) before changes are committed.

1. Ensure you have installed the development dependencies.
2. Install the pre-commit hooks:

```bash
pre-commit install
```

Now, every time you run `git commit`, the hooks will automatically check your code. If any checks fail, fix the issues and stage the changes again.
