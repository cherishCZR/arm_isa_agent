## LDG
_ARM A64 Instruction_

**Title**: LDG -- A64 | **Class**: `general` | **XML ID**: `LDG`

**Architecture**: `FEAT_MTE` (ARMv8.5)

**Summary**: Load Allocation Tag

**Description**:
This instruction loads an Allocation Tag from a memory address,
generates a Logical Address Tag from the Allocation Tag and merges it into
the destination register. The address used for the load is calculated from
the base register and an immediate signed offset scaled by the Tag
Granule.

### Variant: `Integer`
- **Assembly**: `LDG  <Xt>, [<Xn|SP>{, #<simm>}]`
**Encoding Diagram (32-bit)**:

```text
| 31  27 26 25 24 23  21 20  11   9   4  |
|-----------------------------------|
| 1101 1   0   0   1   01  1   imm9 00  Rn  Rt  |
```

#### Decode (A64.ldst.ldsttags.LDG_64Loffset_ldsttags)

```
if !IsFeatureImplemented(FEAT_MTE) then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant bits(64) offset = LSL(SignExtend(imm9, 64), LOG2_TAG_GRANULE);
```

#### Execute (A64.ldst.ldsttags.LDG_64Loffset_ldsttags)

```
bits(64) address;
bits(4) tag;

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

constant boolean stzgm = FALSE;
constant AccessDescriptor accdesc = CreateAccDescLDGSTG(MemOp_LOAD, stzgm);

address = AddressAdd(address, offset, accdesc);
address = Align(address, TAG_GRANULE);

tag = AArch64.MemTag[address, accdesc];
X[t, 64] = AArch64.AddressWithAllocationTag(X[t, 64], tag);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_MTE)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<simm>` | `immediate` | `imm9` | Is the optional signed immediate offset, a multiple of 16 in the range -4096 to 4080, defaulting to 0 and encoded in the "imm9" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `ldg.xml`
</details>