# Codebase design

## Principles

- **Depth is a property of the interface, not the implementation.** A deep module can be internally composed of small, mockable, swappable parts; they just aren't part of the interface. A module can have **internal seams** (private to its implementation, used by its own tests) as well as the **external seam** at its interface.
- **The deletion test.** Imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep.
- **The interface is the test surface.** Callers and tests cross the same seam. If you want to test *past* the interface, the module is probably the wrong shape.
- **One adapter means a hypothetical seam. Two adapters means a real one.** Don't introduce a seam unless something actually varies across it.

Choose the relevant depth:

- Defining module depth or interface vocabulary: [vocabulary](references/vocabulary.md).
- Testing seam, controlled dependency or behavioral testability: [testability](references/testability.md).
- Comparing related principles or needing a worked prompt: [relationships](references/relationships.md).

Use the smallest interface that hides real complexity. Do not create an abstract seam without a real boundary; preserve the current repository structure and public behavior. Read the chosen reference only, not all three.
