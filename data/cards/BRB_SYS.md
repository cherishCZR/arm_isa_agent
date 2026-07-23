## SYS `[ALIAS]`
_ARM A64 Instruction_ (Alias of sys.xml)

**Title**: BRB -- A64 | **Class**: `system` | **XML ID**: `BRB_SYS`

**Architecture**: `FEAT_BRBE` (ARMv9.2)

**Summary**: Branch record buffer

**Description**:
For more information, see
op0==0b01, cache maintenance, TLB maintenance, and address translation instructions.

### Variant: `System`
- **Assembly**: `BRB  <brb_op>`
- **Alias of**: `SYS  #1, C7, C2, #<op2>{, <Xt>}`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  21 20  18  15  11   7   4  |
|--------------------------------|
| 110 101 0100 0   01  001 0111 0010 op2 Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<brb_op>` | `unknown` | `op2` | Is a BRB operation name, as listed for the BRB system instruction group, |

**<brb_op> Value Table**:

| bitfield | symbol |
|---|---|
| 100 |  |
| 101 |  |

---
<details><summary>Metadata</summary>

- alias_mnemonic: `BRB`
- isa: `A64`
- source: `brb_sys.xml`
</details>