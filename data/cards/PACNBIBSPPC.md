## PACNBIBSPPC
_ARM A64 Instruction_

**Title**: PACNBIBSPPC -- A64 | **Class**: `general` | **XML ID**: `PACNBIBSPPC`

**Architecture**: `FEAT_PAuth_LR` (ARMv9.5)

**Summary**: Pointer Authentication Code for return address, using key B, not a branch target

**Description**:
This instruction computes and inserts a Pointer Authentication Code
for an instruction address, using two modifiers and key B.

The address is in X30.

The first modifier is in SP.

The second modifier is the value of PC.

### Variant: `Integer`
- **Assembly**: `PACNBIBSPPC`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24  20  15   9   4  |
|--------------------------------|
| 1   1   0   1   101 0110 00001 100001 11111 11110 |
```

#### Decode (A64.dpreg.dp_1src.PACNBIBSPPC_64LR_dp_1src)

```
if !IsFeatureImplemented(FEAT_PAuth_LR) then EndOfDecode(Decode_UNDEF);

constant integer d = 30;
```

#### Execute (A64.dpreg.dp_1src.PACNBIBSPPC_64LR_dp_1src)

```
X[d, 64] = AddPACIB2(X[d, 64], SP[64], PC64);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_PAuth_LR)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `pacnbibsppc.xml`
</details>