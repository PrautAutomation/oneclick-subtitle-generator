---
name: Bug report
about: Create a report to help us improve
title: ''
labels: ''
assignees: ''

---

name: 🐛 Bug Report
description: Create a report to help us improve
title: "[BUG] <Brief description of bug>"
labels: ["bug", "triage"]
assignees: ''
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report! Please provide as much detail as possible.
  - type: textarea
    id: what-happened
    attributes:
      label: Describe the bug
      description: A clear and concise description of what the bug is.
      placeholder: Tell us what you see!
    validations:
      required: true
  - type: textarea
    id: steps-to-reproduce
    attributes:
      label: Steps to Reproduce
      description: How can we reproduce this bug? Please provide clear steps.
      placeholder: |
        1. Go to '...'
        2. Click on '....'
        3. Scroll down to '....'
        4. See error
    validations:
      required: true
  - type: textarea
    id: expected-behavior
    attributes:
      label: Expected Behavior
      description: A clear and concise description of what you expected to happen.
    validations:
      required: true
  - type: textarea
    id: actual-behavior
    attributes:
      label: Actual Behavior
      description: A clear and concise description of what actually happened.
    validations:
      required: true
  - type: textarea
    id: screenshots
    attributes:
      label: Screenshots
      description: If applicable, add screenshots to help explain your problem.
      placeholder: You can drag and drop images here.
    validations:
      required: false
  - type: input
    id: app-version
    attributes:
      label: OneClick Subtitle Generator Version
      description: Which version of the application are you using?
      placeholder: e.g., 1.0.0-beta, or commit hash
    validations:
      required: true
  - type: dropdown
    id: os
    attributes:
      label: Operating System
      description: What operating system are you using?
      options:
        - Windows
        - macOS
        - Linux
      multiple: false
    validations:
      required: true
  - type: textarea
    id: additional-context
    attributes:
      label: Additional Context
      description: Add any other context about the problem here (e.g., Python version, specific hardware like GPU model if relevant).
    validations:
      required: false
  - type: checkboxes
    id: terms
    attributes:
      label: Code of Conduct
      description: By submitting this issue, you agree to follow our [Code of Conduct](LINK_TO_CODE_OF_CONDUCT.md) (doplň odkaz, pokud máš CoC).
      options:
        - label: I agree to follow this project's Code of Conduct
          required: true
