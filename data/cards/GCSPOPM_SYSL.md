## SYSL `[ALIAS]`
_ARM A64 Instruction_ (Alias of sysl.xml)

**Title**: GCSPOPM -- A64 | **Class**: `system` | **XML ID**: `GCSPOPM_SYSL`

**Architecture**: `FEAT_GCS` (ARMv9.4)

**Summary**: Guarded Control Stack pop

**Description**:
This instruction loads the 64-bit doubleword that is pointed to
by the current Guarded Control Stack pointer, writes it to the destination
register, and increments the current Guarded Control Stack pointer register by
the size of a Guarded Control Stack procedure return record.

### Variant: `System`
- **Assembly**: `GCSPOPM    {<Xt>}`
- **Alias of**: `SYSL  <Xt>, #3, C7, C7, #1`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  21 20  18  15  11   7   4  |
|--------------------------------|
| 110 101 0100 1   01  011 0111 0111 001 Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the optional general-purpose destination register, encoded in the "Rt" field. Defaults to XZR if absent. |

---
<details><summary>Metadata</summary>

- alias_mnemonic: `GCSPOPM`
- isa: `A64`
- source: `gcspopm_sysl.xml`
</details>