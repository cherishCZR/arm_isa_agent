## WFI
_ARM A64 Instruction_

**Title**: WFI -- A64 | **Class**: `system` | **XML ID**: `WFI`

**Summary**: Wait for interrupt

**Description**:
This instruction is a hint instruction that indicates that the PE
can enter a low-power state and remain there until a wakeup event
occurs.
For more information, see Wait For Interrupt.

As described in Wait For Interrupt, the execution
of a WFI instruction that would otherwise cause entry to a low-power
state can be trapped to a higher Exception level.

### Variant: `System`
- **Assembly**: `WFI`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7   4  |
|--------------------|
| 110 101 01000000110010 0000 011 11111 |
```

#### Decode (A64.control.hints.WFI_HI_hints)

```
// Empty.
```

#### Execute (A64.control.hints.WFI_HI_hints)

```
Hint_WFI();
```

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `wfi.xml`
</details>