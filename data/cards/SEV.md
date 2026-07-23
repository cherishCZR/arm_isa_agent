## SEV
_ARM A64 Instruction_

**Title**: SEV -- A64 | **Class**: `system` | **XML ID**: `SEV`

**Summary**: Send event

**Description**:
This instruction is a hint instruction that causes an event to be signaled
to all PEs in the multiprocessor system. For more information, see
Wait for Event mechanism and Send event.

### Variant: `System`
- **Assembly**: `SEV`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7   4  |
|--------------------|
| 110 101 01000000110010 0000 100 11111 |
```

#### Decode (A64.control.hints.SEV_HI_hints)

```
// Empty.
```

#### Execute (A64.control.hints.SEV_HI_hints)

```
SendEvent();
```

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sev.xml`
</details>