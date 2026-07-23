## YIELD
_ARM A64 Instruction_

**Title**: YIELD -- A64 | **Class**: `system` | **XML ID**: `YIELD`

**Summary**: Yield

**Description**:
This instruction is a hint instruction. Software with a multithreading capability can use a YIELD
instruction to indicate to the PE that it is performing a task, for example a spin-lock,
that could be swapped out to improve overall system performance. The PE can use this hint
to suspend and resume multiple software threads if it supports the capability.

For more information about the recommended use of this instruction, see The YIELD instruction.

### Variant: `System`
- **Assembly**: `YIELD`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7   4  |
|--------------------|
| 110 101 01000000110010 0000 001 11111 |
```

#### Decode (A64.control.hints.YIELD_HI_hints)

```
// Empty.
```

#### Execute (A64.control.hints.YIELD_HI_hints)

```
Hint_Yield();
```

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `yield.xml`
</details>