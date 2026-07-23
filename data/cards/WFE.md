## WFE
_ARM A64 Instruction_

**Title**: WFE -- A64 | **Class**: `system` | **XML ID**: `WFE`

**Summary**: Wait for event

**Description**:
This instruction is a hint instruction that indicates that the PE can
enter a low-power state and remain there until a wakeup event
occurs. Wakeup events include the event signaled as a result of
executing the SEV instruction on any PE in the multiprocessor
system.
For more information, see Wait For Event
mechanism and Send event.

As described in Wait For Event mechanism and Send event, the
execution of a WFE instruction that would otherwise cause entry to a low-power
state can be trapped to a higher Exception level.

### Variant: `System`
- **Assembly**: `WFE`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7   4  |
|--------------------|
| 110 101 01000000110010 0000 010 11111 |
```

#### Decode (A64.control.hints.WFE_HI_hints)

```
// Empty.
```

#### Execute (A64.control.hints.WFE_HI_hints)

```
Hint_WFE();
```

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `wfe.xml`
</details>