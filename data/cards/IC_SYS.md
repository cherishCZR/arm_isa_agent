## SYS `[ALIAS]`
_ARM A64 Instruction_ (Alias of sys.xml)

**Title**: IC -- A64 | **Class**: `system` | **XML ID**: `IC_SYS`

**Summary**: Instruction cache operation

**Description**:
For more information, see
op0==0b01, cache maintenance, TLB maintenance, and address translation instructions.

### Variant: `System`
- **Assembly**: `IC  <ic_op>{, <Xt>}`
- **Alias of**: `SYS  #<op1>, C7, <Cm>, #<op2>{, <Xt>}`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  21 20  18  15  11   7   4  |
|--------------------------------|
| 110 101 0100 0   01  op1 0111 CRm op2 Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<ic_op>` | `unknown` | `op1:CRm:op2` | Is an IC operation name, as listed for the IC system instruction pages, |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the optional general-purpose source register, defaulting to '11111', encoded in the "Rt" field. |

**<ic_op> Value Table**:

| bitfield | symbol |
|---|---|
| 000 | IALLUIS |
| 000 | IALLU |
| 001 | IVAU |

---
<details><summary>Metadata</summary>

- alias_mnemonic: `IC`
- isa: `A64`
- source: `ic_sys.xml`
</details>