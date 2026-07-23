## PACIBSPPC
_ARM A64 Instruction_

**Title**: PACIBSPPC -- A64 | **Class**: `general` | **XML ID**: `PACIBSPPC`

**Architecture**: `FEAT_PAuth_LR` (ARMv9.5)

**Summary**: Pointer Authentication Code for return address, using key B

**Description**:
This instruction computes and inserts a Pointer Authentication Code
for an instruction address, using two modifiers and key B.

The address is in X30.

The first modifier is in SP.

The second modifier is the value of PC.

A PACIBSPPC instruction has an implicit BTI instruction. The
implicit BTI instruction of a PACIBSPPC instruction is always
compatible with PSTATE.BTYPE == 0b01
and PSTATE.BTYPE == 0b10.
Controls in SCTLR_ELx configure whether the
implicit BTI instruction of a PACIBSPPC instruction is compatible with
PSTATE.BTYPE == 0b11.
For more information, see PSTATE.BTYPE.

### Variant: `Integer`
- **Assembly**: `PACIBSPPC`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24  20  15   9   4  |
|--------------------------------|
| 1   1   0   1   101 0110 00001 101001 11111 11110 |
```

#### Decode (A64.dpreg.dp_1src.PACIBSPPC_64LR_dp_1src)

```
if !IsFeatureImplemented(FEAT_PAuth_LR) then EndOfDecode(Decode_UNDEF);

constant integer d = 30;
if IsFeatureImplemented(FEAT_BTI) then
    // Check for branch target compatibility between PSTATE.BTYPE
    // and implicit branch target of PACIxSPPC instruction.
    SetBTypeCompatible(BTypeCompatible_PACIXSP());
```

#### Execute (A64.dpreg.dp_1src.PACIBSPPC_64LR_dp_1src)

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
- source: `pacibsppc.xml`
</details>