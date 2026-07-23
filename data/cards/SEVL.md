## SEVL
_ARM A64 Instruction_

**Title**: SEVL -- A64 | **Class**: `system` | **XML ID**: `SEVL`

**Summary**: Send event local

**Description**:
This instruction is a hint instruction that causes an event to be
signaled locally without requiring the event to be signaled to
other PEs in the multiprocessor system. It can prime a wait-loop
that starts with a WFE instruction.

### Variant: `System`
- **Assembly**: `SEVL`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7   4  |
|--------------------|
| 110 101 01000000110010 0000 101 11111 |
```

#### Decode (A64.control.hints.SEVL_HI_hints)

```
// Empty.
```

#### Execute (A64.control.hints.SEVL_HI_hints)

```
SendEventLocal();
```

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sevl.xml`
</details>