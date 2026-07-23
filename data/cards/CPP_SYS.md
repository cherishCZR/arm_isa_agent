## SYS `[ALIAS]`
_ARM A64 Instruction_ (Alias of sys.xml)

**Title**: CPP -- A64 | **Class**: `system` | **XML ID**: `CPP_SYS`

**Architecture**: `FEAT_SPECRES` (PROFILE_R)

**Summary**: Cache prefetch prediction restriction by context

**Description**:
This instruction prevents
cache allocation predictions that predict execution addresses
based on information gathered from earlier execution within
a particular execution context. The actions of code in the target
execution context or contexts appearing in program order before the
instruction cannot exploitatively control cache prefetch predictions
occurring after the instruction is complete and synchronized.

For more information, see
CPP RCTX, Cache Prefetch Prediction Restriction by Context.

### Variant: `System`
- **Assembly**: `CPP  RCTX, <Xt>`
- **Alias of**: `SYS  #3, C7, C3, #7, <Xt>`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  21 20  18  15  11   7   4  |
|--------------------------------|
| 110 101 0100 0   01  011 0111 0011 111 Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose source register, encoded in the "Rt" field. |

---
<details><summary>Metadata</summary>

- alias_mnemonic: `CPP`
- isa: `A64`
- source: `cpp_sys.xml`
</details>