## SYSP `[ALIAS]`
_ARM A64 Instruction_ (Alias of sysp.xml)

**Title**: TLBIP -- A64 | **Class**: `system` | **XML ID**: `TLBIP_SYSP`

**Architecture**: `FEAT_D128 && FEAT_SYSINSTR128` (FEAT_D128 && FEAT_SYSINSTR128)

**Summary**: TLB invalidate pair operation

**Description**:
TLB invalidate pair operation.

### Variant: `System`
- **Assembly**: `TLBIP  <tlbip_op>{, <Xt1>, <Xt2>}`
- **Alias of**: `SYSP  #<op1>, <Cn>, <Cm>, #<op2>{, <Xt1>, <Xt2>}`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  21 20  18  15  11   7   4  |
|--------------------------------|
| 110 101 0101 0   01  op1 100x CRm op2 Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<tlbip_op>` | `unknown` | `op1:CRn:CRm:op2` | Is a TLBIP operation name, as listed for the TLBIP system pair instruction group, |
| `<Xt1>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the first optional general-purpose source register, defaulting to '11111', encoded in the "Rt" field. |
| `<Xt2>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the second optional general-purpose source register, defaulting to '11111', encoded as "Rt" +1. Defaults to '11111' if "Rt" = '1 |

**<tlbip_op> Value Table**:

| bitfield | symbol |
|---|---|
| 001 |  |
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
| 001 |  |
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
| 001 |  |
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
| 001 |  |
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
| 001 |  |
| 010 |  |
| 101 |  |
| 110 |  |
| 001 |  |
| 101 |  |
| 001 |  |
| 101 |  |
| 001 |  |
| 101 |  |
| 000 |  |
| 001 |  |
| 010 |  |
| 011 |  |
| 100 |  |
| 101 |  |
| 110 |  |
| 111 |  |
| 001 |  |
| 101 |  |
| 001 |  |
| 101 |  |
| 001 |  |
| 101 |  |
| 001 |  |
| 010 |  |
| 101 |  |
| 110 |  |
| 001 |  |
| 101 |  |
| 001 |  |
| 101 |  |
| 001 |  |
| 101 |  |
| 000 |  |
| 001 |  |
| 010 |  |
| 011 |  |
| 100 |  |
| 101 |  |
| 110 |  |
| 111 |  |
| 001 |  |
| 101 |  |
| 001 |  |
| 101 |  |
| 001 |  |
| 101 |  |
| 001 |  |
| 101 |  |
| 001 |  |
| 101 |  |
| 001 |  |
| 101 |  |
| 001 |  |
| 101 |  |
| 001 |  |
| 101 |  |
| 001 |  |
| 101 |  |
| 001 |  |
| 101 |  |
| 001 |  |
| 101 |  |
| 001 |  |
| 101 |  |
| 001 |  |
| 101 |  |
| 001 |  |
| 101 |  |
| 001 |  |
| 101 |  |

---
<details><summary>Metadata</summary>

- alias_mnemonic: `TLBIP`
- isa: `A64`
- source: `tlbip_sysp.xml`
</details>