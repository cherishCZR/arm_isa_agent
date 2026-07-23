## ADDG
_ARM A64 Instruction_

**Title**: ADDG -- A64 | **Class**: `general` | **XML ID**: `ADDG`

**Architecture**: `FEAT_MTE` (ARMv8.5)

**Summary**: Add with tag

**Description**:
This instruction adds an immediate value scaled by the Tag Granule to the address
in the source register, modifies the Logical Address Tag of the address using
an immediate value, and writes the result to the destination register. Tags
specified in GCR_EL1.Exclude are excluded from the possible outputs when
modifying the Logical Address Tag.

### Variant: `Integer`
- **Assembly**: `ADDG  <Xd|SP>, <Xn|SP>, #<uimm6>, #<uimm4>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  25  21  15  13   9   4  |
|--------------------------------|
| 1   0   0   100 0110 imm6 (0)(0) imm4 Rn  Rd  |
```

#### Decode (A64.dpimm.addsub_immtags.ADDG_64_addsub_immtags)

```
if !IsFeatureImplemented(FEAT_MTE) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant bits(4) tag_offset = imm4;
constant bits(64) offset = LSL(ZeroExtend(imm6, 64), LOG2_TAG_GRANULE);
```

#### Execute (A64.dpimm.addsub_immtags.ADDG_64_addsub_immtags)

```
constant bits(64) operand1 = if n == 31 then SP[64] else X[n, 64];
constant bits(4) start_tag = AArch64.AllocationTagFromAddress(operand1);
constant bits(16) exclude = GCR_EL1.Exclude;
bits(64) result;
bits(4) rtag;

if AArch64.AllocationTagAccessIsEnabled(PSTATE.EL) then
    rtag = AArch64.ChooseNonExcludedTag(start_tag, tag_offset, exclude);
else
    rtag = '0000';

(result, -) = AddWithCarry(operand1, offset, '0');

result = AArch64.AddressWithAllocationTag(result, rtag);

if d == 31 then
    SP[64] = result;
else
    X[d, 64] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_MTE)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xd\|SP>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the destination general-purpose register or stack pointer, encoded in the "Rd" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the source general-purpose register or stack pointer, encoded in the "Rn" field. |
| `<uimm6>` | `immediate` | `imm6` | Is an unsigned immediate, a multiple of 16 in the range 0 to 1008, encoded in the "imm6" field. |
| `<uimm4>` | `immediate` | `imm4` | Is an unsigned immediate, in the range 0 to 15, encoded in the "imm4" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `addg.xml`
</details>