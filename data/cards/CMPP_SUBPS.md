## SUBPS `[ALIAS]`
_ARM A64 Instruction_ (Alias of subps.xml)

**Title**: CMPP -- A64 | **Class**: `general` | **XML ID**: `CMPP_SUBPS`

**Architecture**: `FEAT_MTE` (ARMv8.5)

**Summary**: Compare with tag

**Description**:
This instruction subtracts the 56-bit address held in the second source
register from the 56-bit address held in the first source register,
updates the condition flags based on the result of the subtraction,
and discards the result.

### Variant: `Integer`
- **Assembly**: `CMPP  <Xn|SP>, <Xm|SP>`
- **Alias of**: `SUBPS  XZR, <Xn|SP>, <Xm|SP>`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24  20  15   9   4  |
|--------------------------------|
| 1   0   1   1   101 0110 Rm  000000 Rn  11111 |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the first source general-purpose register or stack pointer, encoded in the "Rn" field. |
| `<Xm\|SP>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the second general-purpose source register or stack pointer, encoded in the "Rm" field. |

---
<details><summary>Metadata</summary>

- alias_mnemonic: `CMPP`
- isa: `A64`
- source: `cmpp_subps.xml`
</details>