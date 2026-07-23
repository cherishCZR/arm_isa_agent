## PACGA
_ARM A64 Instruction_

**Title**: PACGA -- A64 | **Class**: `general` | **XML ID**: `PACGA`

**Architecture**: `FEAT_PAuth` (ARMv8.3)

**Summary**: Pointer Authentication Code, using generic key

**Description**:
This instruction computes the Pointer Authentication Code for a 64-bit value
in the first source register, using a modifier in the second
source register, and the generic key.
The computed Pointer Authentication Code is written to the most significant
32 bits of the destination register, and the least significant 32 bits of the
destination register are set to zero.

### Variant: `Integer`
- **Assembly**: `PACGA  <Xd>, <Xn>, <Xm|SP>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24  20  15   9   4  |
|--------------------------------|
| 1   0   0   1   101 0110 Rm  001100 Rn  Rd  |
```

#### Decode (A64.dpreg.dp_2src.PACGA_64P_dp_2src)

```
if !IsFeatureImplemented(FEAT_PAuth) then EndOfDecode(Decode_UNDEF);

boolean source_is_sp = FALSE;
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);

if m == 31 then source_is_sp = TRUE;
```

#### Execute (A64.dpreg.dp_2src.PACGA_64P_dp_2src)

```
if source_is_sp then
    X[d, 64] = AddPACGA(X[n, 64], SP[64]);
else
    X[d, 64] = AddPACGA(X[n, 64], X[m, 64]);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_PAuth)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the first general-purpose source register, encoded in the "Rn" field. |
| `<Xm\|SP>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the second general-purpose source register or stack pointer, encoded in the "Rm" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `pacga.xml`
</details>