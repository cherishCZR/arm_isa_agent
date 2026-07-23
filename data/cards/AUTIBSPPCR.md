## AUTIBSPPCR
_ARM A64 Instruction_

**Title**: AUTIBSPPCR -- A64 | **Class**: `general` | **XML ID**: `AUTIBSPPCR`

**Architecture**: `FEAT_PAuth_LR` (ARMv9.5)

**Summary**: Authenticate return address using key B, using a register

**Description**:
This instruction authenticates an instruction address, using two modifiers and key B.

If the authentication passes, the upper bits of the address are
restored to enable subsequent use of the address.
For information on behavior if the authentication fails, see
Faulting on pointer authentication.

The address is in X30.

The first modifier is in SP.

The second modifier is in the general-purpose register that is specified by <Xn>.

### Variant: `Integer`
- **Assembly**: `AUTIBSPPCR  <Xn>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24  20  15   9   4  |
|--------------------------------|
| 1   1   0   1   101 0110 00001 100101 Rn  11110 |
```

#### Decode (A64.dpreg.dp_1src.AUTIBSPPCR_64LRR_dp_1src)

```
if !IsFeatureImplemented(FEAT_PAuth_LR) then EndOfDecode(Decode_UNDEF);

constant integer d = 30;
constant integer n = UInt(Rn);
constant boolean auth_combined = FALSE;
```

#### Execute (A64.dpreg.dp_1src.AUTIBSPPCR_64LRR_dp_1src)

```
X[d, 64] = AuthIB2(X[d, 64], SP[64], X[n, 64], auth_combined);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_PAuth_LR)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose source register, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `autibsppcr.xml`
</details>