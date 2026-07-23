## UDF
_ARM A64 Instruction_

**Title**: UDF -- A64 | **Class**: `general` | **XML ID**: `UDF_perm_undef`

**Summary**: Permanently undefined

**Description**:
This instruction generates an Undefined Instruction exception (ESR_ELx.EC = 0b000000).
The encodings for UDF used in this section are defined as permanently UNDEFINED.

### Variant: `Integer`
- **Assembly**: `UDF  #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  15  |
|-----------------|
| 0   00  0000 000000000 imm16 |
```

#### Decode (A64.reserved.perm_undef.UDF_only_perm_undef)

```
// The imm16 field is ignored by hardware.
EndOfDecode(Decode_UNDEF);
```

#### Execute (A64.reserved.perm_undef.UDF_only_perm_undef)

```
// No operation.
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `(never valid)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<imm>` | `immediate` | `imm16` | is a 16-bit unsigned immediate, in the range 0 to 65535, encoded in the "imm16" field. The PE ignores the value of this constant. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `udf_perm_undef.xml`
</details>