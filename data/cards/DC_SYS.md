## SYS `[ALIAS]`
_ARM A64 Instruction_ (Alias of sys.xml)

**Title**: DC -- A64 | **Class**: `system` | **XML ID**: `DC_SYS`

**Summary**: Data cache operation

**Description**:
For more information, see
op0==0b01, cache maintenance, TLB maintenance, and address translation instructions.

### Variant: `System`
- **Assembly**: `DC  <dc_op>, <Xt>`
- **Alias of**: `SYS  #<op1>, C7, <Cm>, #<op2>, <Xt>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  21 20  18  15  11   7   4  |
|--------------------------------|
| 110 101 0100 0   01  op1 0111 CRm op2 Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<dc_op>` | `unknown` | `op1:CRm:op2` | Is a DC operation name, as listed for the DC system instruction group, |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose source register, encoded in the "Rt" field. |

**<dc_op> Value Table**:

| bitfield | symbol |
|---|---|
| 001 |  |
| 010 |  |
| 011 |  |
| 100 |  |
| 101 |  |
| 110 |  |
| 010 |  |
| 100 |  |
| 110 |  |
| 010 |  |
| 100 |  |
| 110 |  |
| 001 |  |
| 101 |  |
| 001 |  |
| 011 |  |
| 100 |  |
| 001 |  |
| 011 |  |
| 101 |  |
| 000 |  |
| 001 |  |
| 111 |  |
| 001 |  |
| 011 |  |
| 101 |  |
| 001 |  |
| 011 |  |
| 101 |  |
| 001 |  |
| 011 |  |
| 101 |  |
| 000 |  |
| 111 |  |
| 000 |  |
| 111 |  |
| 001 |  |
| 101 |  |

---
<details><summary>Metadata</summary>

- alias_mnemonic: `DC`
- isa: `A64`
- source: `dc_sys.xml`
</details>