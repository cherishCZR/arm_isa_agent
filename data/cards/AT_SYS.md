## SYS `[ALIAS]`
_ARM A64 Instruction_ (Alias of sys.xml)

**Title**: AT -- A64 | **Class**: `system` | **XML ID**: `AT_SYS`

**Summary**: Address translate

**Description**:
For more information, see
op0==0b01, cache maintenance, TLB maintenance, and address translation instructions.

### Variant: `System`
- **Assembly**: `AT  <at_op>, <Xt>`
- **Alias of**: `SYS  #<op1>, C7, <Cm>, #<op2>, <Xt>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  21 20  18  15  11   7   4  |
|--------------------------------|
| 110 101 0100 0   01  op1 0111 100x op2 Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<at_op>` | `unknown` | `op1:CRm:op2` | Is an AT operation name, as listed for the AT system instruction group, |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose source register, encoded in the "Rt" field. |

**<at_op> Value Table**:

| bitfield | symbol |
|---|---|
| 000 |  |
| 001 |  |
| 010 |  |
| 011 |  |
| 000 |  |
| 001 |  |
| 010 |  |
| 000 |  |
| 001 |  |
| 100 |  |
| 101 |  |
| 110 |  |
| 111 |  |
| 010 |  |
| 000 |  |
| 001 |  |
| 010 |  |

---
<details><summary>Metadata</summary>

- alias_mnemonic: `AT`
- isa: `A64`
- source: `at_sys.xml`
</details>