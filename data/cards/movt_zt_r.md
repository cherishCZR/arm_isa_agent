## MOVT
_ARM A64 Instruction_

**Title**: MOVT (scalar to table) -- A64 | **Class**: `mortlach2` | **XML ID**: `movt_zt_r`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Move 8 bytes from general-purpose register to ZT0

**Description**:
This instruction moves 8 bytes to the ZT0 register at the byte offset specified by the immediate index from
a general-purpose register. This instruction is UNDEFINED in Non-debug state.

**Attributes**: SM Policy: `SM_0_or_1`

### Variant: `SME2`
- **Assembly**: `MOVT  ZT0[<offs>], <Xt>`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  17 16  14  11   4  |
|-----------------------------|
| 1   10  0000 0010011 1   00  off3 0011111 Rt  |
```

#### Decode (A64.sme.mortlach_mov_zt.mortlach_insert_zt.movt_zt_r_)

```
if !IsFeatureImplemented(FEAT_SME2) || !Halted() then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer offset = UInt(off3);
```

#### Execute (A64.sme.mortlach_mov_zt.mortlach_insert_zt.movt_zt_r_)

```
CheckSMEEnabled();
CheckSMEZT0Enabled();
bits(512) result = ZT0[512];

Elem[result, offset, 64] = X[t, 64];
ZT0[512] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2) && !Halted()` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<offs>` | `unknown` | `off3` | Is the immediate byte offset, a multiple of 8 in the range of 0 to 56, encoded in the "off3" field as <offs>/8. |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `movt_zt_r.xml`
</details>