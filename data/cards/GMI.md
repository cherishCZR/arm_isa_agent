## GMI
_ARM A64 Instruction_

**Title**: GMI -- A64 | **Class**: `general` | **XML ID**: `GMI`

**Architecture**: `FEAT_MTE` (ARMv8.5)

**Summary**: Tag mask insert

**Description**:
This instruction inserts the tag in the first source register into the excluded
set specified in the second source register, writing the new excluded set to
the destination register.

### Variant: `Integer`
- **Assembly**: `GMI  <Xd>, <Xn|SP>, <Xm>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24  20  15   9   4  |
|--------------------------------|
| 1   0   0   1   101 0110 Rm  000101 Rn  Rd  |
```

#### Decode (A64.dpreg.dp_2src.GMI_64G_dp_2src)

```
if !IsFeatureImplemented(FEAT_MTE) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
```

#### Execute (A64.dpreg.dp_2src.GMI_64G_dp_2src)

```
constant bits(64) address = if n == 31 then SP[64] else X[n, 64];
bits(64) mask = X[m, 64];
constant bits(4) tag = AArch64.AllocationTagFromAddress(address);

mask<UInt(tag)> = '1';
X[d, 64] = mask;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_MTE)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the first source general-purpose register or stack pointer, encoded in the "Rn" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the second general-purpose source register, encoded in the "Rm" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `gmi.xml`
</details>