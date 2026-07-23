## SYS `[ALIAS]`
_ARM A64 Instruction_ (Alias of sys.xml)

**Title**: TLBI -- A64 | **Class**: `system` | **XML ID**: `TLBI_SYS`

**Summary**: TLB invalidate operation

**Description**:
For more information, see
op0==0b01, cache maintenance, TLB maintenance, and address translation instructions.

### Variant: `System`
- **Assembly**: `TLBI  <tlbi_op>{, <Xt>}`
- **Alias of**: `SYS  #<op1>, <Cn>, <Cm>, #<op2>{, <Xt>}`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  21 20  18  15  11   7   4  |
|--------------------------------|
| 110 101 0100 0   01  op1 100x CRm op2 Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<tlbi_op>` | `unknown` | `op1:CRn:CRm:op2` | Is a TLBI operation name, as listed for the TLBI system instruction group, |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the optional general-purpose source register, defaulting to '11111', encoded in the "Rt" field. |

**<tlbi_op> Value Table**:

| bitfield | symbol |
|---|---|
| 000 |  |
| 001 |  |
| 010 |  |
| 011 |  |
| 101 |  |
| 111 |  |
| 001 |  |
| 011 |  |
| 101 |  |
| 111 |  |
| 000 |  |
| 001 |  |
| 010 |  |
| 011 |  |
| 101 |  |
| 111 |  |
| 001 |  |
| 011 |  |
| 101 |  |
| 111 |  |
| 001 |  |
| 011 |  |
| 101 |  |
| 111 |  |
| 000 |  |
| 001 |  |
| 010 |  |
| 011 |  |
| 101 |  |
| 111 |  |
| 000 |  |
| 001 |  |
| 010 |  |
| 011 |  |
| 101 |  |
| 111 |  |
| 001 |  |
| 011 |  |
| 101 |  |
| 111 |  |
| 000 |  |
| 001 |  |
| 010 |  |
| 011 |  |
| 101 |  |
| 111 |  |
| 001 |  |
| 011 |  |
| 101 |  |
| 111 |  |
| 001 |  |
| 011 |  |
| 101 |  |
| 111 |  |
| 000 |  |
| 001 |  |
| 010 |  |
| 011 |  |
| 101 |  |
| 111 |  |
| 001 |  |
| 010 |  |
| 101 |  |
| 110 |  |
| 000 |  |
| 001 |  |
| 100 |  |
| 101 |  |
| 110 |  |
| 001 |  |
| 010 |  |
| 101 |  |
| 000 |  |
| 001 |  |
| 100 |  |
| 101 |  |
| 110 |  |
| 000 |  |
| 001 |  |
| 010 |  |
| 011 |  |
| 100 |  |
| 101 |  |
| 110 |  |
| 111 |  |
| 001 |  |
| 010 |  |
| 101 |  |
| 001 |  |
| 010 |  |
| 101 |  |
| 000 |  |
| 001 |  |
| 100 |  |
| 101 |  |
| 110 |  |
| 001 |  |
| 010 |  |
| 101 |  |
| 110 |  |
| 000 |  |
| 001 |  |
| 100 |  |
| 101 |  |
| 110 |  |
| 001 |  |
| 010 |  |
| 101 |  |
| 000 |  |
| 001 |  |
| 100 |  |
| 101 |  |
| 110 |  |
| 000 |  |
| 001 |  |
| 010 |  |
| 011 |  |
| 100 |  |
| 101 |  |
| 110 |  |
| 111 |  |
| 001 |  |
| 010 |  |
| 101 |  |
| 001 |  |
| 010 |  |
| 101 |  |
| 000 |  |
| 001 |  |
| 100 |  |
| 101 |  |
| 110 |  |
| 000 |  |
| 001 |  |
| 100 |  |
| 101 |  |
| 001 |  |
| 101 |  |
| 000 |  |
| 001 |  |
| 101 |  |
| 011 |  |
| 111 |  |
| 001 |  |
| 101 |  |
| 001 |  |
| 101 |  |
| 000 |  |
| 001 |  |
| 100 |  |
| 101 |  |
| 000 |  |
| 001 |  |
| 101 |  |
| 001 |  |
| 101 |  |
| 000 |  |
| 001 |  |
| 101 |  |
| 001 |  |
| 101 |  |
| 001 |  |
| 101 |  |
| 000 |  |
| 001 |  |
| 101 |  |

---
<details><summary>Metadata</summary>

- alias_mnemonic: `TLBI`
- isa: `A64`
- source: `tlbi_sys.xml`
</details>