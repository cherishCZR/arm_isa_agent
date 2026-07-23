## STZ2G
_ARM A64 Instruction_

**Title**: STZ2G -- A64 | **Class**: `general` | **XML ID**: `STZ2G`

**Architecture**: `FEAT_MTE` (ARMv8.5)

**Summary**: Store Allocation Tags, zeroing

**Description**:
This instruction stores an Allocation Tag to two Tag Granules of
memory, zeroing the associated data locations. The address used for the store
is calculated from the base register and an immediate signed offset scaled
by the Tag Granule. The Allocation Tag is calculated from the Logical Address
Tag in the source register.

This instruction generates an Unchecked access.

### Variant: `Post-index`
- **Assembly**: `STZ2G  <Xt|SP>, [<Xn|SP>], #<simm>`
**Encoding Diagram (32-bit)**:

```text
| 31  27 26 25 24 23  21 20  11   9   4  |
|-----------------------------------|
| 1101 1   0   0   1   11  1   imm9 01  Rn  Rt  |
```

#### Decode (A64.ldst.ldsttags.STZ2G_64Spost_ldsttags)

```
if !IsFeatureImplemented(FEAT_MTE) then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant bits(64) offset = LSL(SignExtend(imm9, 64), LOG2_TAG_GRANULE);
constant boolean writeback = TRUE;
constant boolean postindex = TRUE;
```

#### Execute (A64.ldst.ldsttags.STZ2G_64Spost_ldsttags)

```
bits(64) address;
bits(64) address2;
constant bits(64) data = if t == 31 then SP[64] else X[t, 64];
constant bits(4) tag = AArch64.AllocationTagFromAddress(data);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

constant boolean stzgm = FALSE;
constant AccessDescriptor accdesc = CreateAccDescLDGSTG(MemOp_STORE, stzgm);

if !postindex then
    address = AddressAdd(address, offset, accdesc);

address2 = AddressIncrement(address, TAG_GRANULE, accdesc);

if !IsAligned(address, TAG_GRANULE) then
    constant FaultRecord fault = AlignmentFault(accdesc, address);
    AArch64.Abort(fault);

Mem[address , TAG_GRANULE, accdesc] = Zeros(TAG_GRANULE * 8);
Mem[address2, TAG_GRANULE, accdesc] = Zeros(TAG_GRANULE * 8);

AArch64.MemTag[address , accdesc] = tag;
AArch64.MemTag[address2, accdesc] = tag;

if writeback then
    if postindex then
        address = AddressAdd(address, offset, accdesc);

    if n == 31 then
        SP[64] = address;
    else
        X[n, 64] = address;
```

### Variant: `Pre-index`
- **Assembly**: `STZ2G  <Xt|SP>, [<Xn|SP>, #<simm>]!`
**Encoding Diagram (32-bit)**:

```text
| 31  27 26 25 24 23  21 20  11   9   4  |
|-----------------------------------|
| 1101 1   0   0   1   11  1   imm9 11  Rn  Rt  |
```

#### Decode (A64.ldst.ldsttags.STZ2G_64Spre_ldsttags)

```
if !IsFeatureImplemented(FEAT_MTE) then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant bits(64) offset = LSL(SignExtend(imm9, 64), LOG2_TAG_GRANULE);
constant boolean writeback = TRUE;
constant boolean postindex = FALSE;
```

### Variant: `Signed offset`
- **Assembly**: `STZ2G  <Xt|SP>, [<Xn|SP>{, #<simm>}]`
**Encoding Diagram (32-bit)**:

```text
| 31  27 26 25 24 23  21 20  11   9   4  |
|-----------------------------------|
| 1101 1   0   0   1   11  1   imm9 10  Rn  Rt  |
```

#### Decode (A64.ldst.ldsttags.STZ2G_64Soffset_ldsttags)

```
if !IsFeatureImplemented(FEAT_MTE) then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant bits(64) offset = LSL(SignExtend(imm9, 64), LOG2_TAG_GRANULE);
constant boolean writeback = FALSE;
constant boolean postindex = FALSE;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt\|SP>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose source register or stack pointer, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<simm>` | `immediate` | `imm9` | Is the optional signed immediate offset, a multiple of 16 in the range -4096 to 4080, defaulting to 0 and encoded in the "imm9" field. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_MTE)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `stz2g.xml`
</details>