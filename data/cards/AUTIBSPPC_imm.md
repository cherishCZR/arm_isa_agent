## AUTIBSPPC
_ARM A64 Instruction_

**Title**: AUTIBSPPC -- A64 | **Class**: `general` | **XML ID**: `AUTIBSPPC_imm`

**Architecture**: `FEAT_PAuth_LR` (ARMv9.5)

**Summary**: Authenticate return address using key B, using an immediate offset

**Description**:
This instruction authenticates an instruction address, using two modifiers and key B.

If the authentication passes, the upper bits of the address are
restored to enable subsequent use of the address.
For information on behavior if the authentication fails, see
Faulting on pointer authentication.

The address is in X30.

The first modifier is in SP.

The second modifier is the address of a program label.

### Variant: `Integer`
- **Assembly**: `AUTIBSPPC  <label>`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  25  22  20   4  |
|-----------------------|
| 1   11  100 111 01  imm16 11111 |
```

#### Decode (A64.dpimm.dp_1src_imm.AUTIBSPPC_only_dp_1src_imm)

```
if !IsFeatureImplemented(FEAT_PAuth_LR) then EndOfDecode(Decode_UNDEF);

constant integer d = 30;
constant bits(64) offset = ZeroExtend(imm16:'00', 64);
constant boolean auth_combined = FALSE;
```

#### Execute (A64.dpimm.dp_1src_imm.AUTIBSPPC_only_dp_1src_imm)

```
constant bits(64) pac_addr = PC64 - offset;

X[d, 64] = AuthIB2(X[d, 64], SP[64], pac_addr, auth_combined);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_PAuth_LR)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<label>` | `label` | `imm16` | Is the program label whose address is to be calculated. Its negative offset from the address of this instruction, a multiple of 4 in the range -262140 |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `autibsppc_imm.xml`
</details>