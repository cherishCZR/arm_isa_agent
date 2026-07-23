## MOVT
_ARM A64 Instruction_

**Title**: MOVT (table to scalar) -- A64 | **Class**: `mortlach2` | **XML ID**: `movt_r_zt`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Move 8 bytes from ZT0 to general-purpose register

**Description**:
This instruction moves 8 bytes to a general-purpose register from the ZT0 register at the byte offset
specified by the immediate index. This instruction is UNDEFINED in Non-debug state.

**Attributes**: SM Policy: `SM_0_or_1`

### Variant: `SME2`
- **Assembly**: `MOVT  <Xt>, ZT0[<offs>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  17 16  14  11   4  |
|-----------------------------|
| 1   10  0000 0010011 0   00  off3 0011111 Rt  |
```

#### Decode (A64.sme.mortlach_mov_zt.mortlach_extract_zt.movt_r_zt_)

```
if !IsFeatureImplemented(FEAT_SME2) || !Halted() then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer offset = UInt(off3);
```

#### Execute (A64.sme.mortlach_mov_zt.mortlach_extract_zt.movt_r_zt_)

```
CheckSMEEnabled();
CheckSMEZT0Enabled();
constant bits(512) operand = ZT0[512];

X[t, 64] = Elem[operand, offset, 64];
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2) && !Halted()` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |
| `<offs>` | `unknown` | `off3` | Is the immediate byte offset, a multiple of 8 in the range of 0 to 56, encoded in the "off3" field as <offs>/8. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `movt_r_zt.xml`
</details>