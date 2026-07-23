## SYS `[ALIAS]`
_ARM A64 Instruction_ (Alias of sys.xml)

**Title**: APAS -- A64 | **Class**: `system` | **XML ID**: `APAS_SYS`

**Architecture**: `FEAT_RME_GPC3` (ARMv9.6)

**Summary**: Associate physical address space

**Description**:
This instruction associates a physical address space with a memory-mapped location
that is protected by a memory-side physical address space filter.

### Variant: `System`
- **Assembly**: `APAS  <Xt>`
- **Alias of**: `SYS  #6, C7, C0, #0, <Xt>`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  21 20  18  15  11   7   4  |
|--------------------------------|
| 110 101 0100 0   01  110 0111 0000 000 Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose source register, encoded in the "Rt" field. |

---
<details><summary>Metadata</summary>

- alias_mnemonic: `APAS`
- isa: `A64`
- source: `apas_sys.xml`
</details>