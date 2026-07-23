## STGP
_ARM A64 Instruction_

**Title**: STGP -- A64 | **Class**: `general` | **XML ID**: `STGP`

**Architecture**: `FEAT_MTE` (ARMv8.5)

**Summary**: Store Allocation Tag and pair of registers

**Description**:
This instruction stores an Allocation Tag and two
64-bit doublewords to memory, from two registers. The address used for the
store is calculated from the base register and an immediate signed offset
scaled by the Tag Granule. The Allocation Tag is calculated from the Logical
Address Tag in the base register.

This instruction generates an Unchecked access.

### Variant: `Post-index`
- **Assembly**: `STGP  <Xt1>, <Xt2>, [<Xn|SP>], #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24  22 21  14   9   4  |
|-----------------------------------|
| 01  10  1   0   0   01  0   simm7 Rt2 Rn  Rt  |
```

#### Decode (A64.ldst.ldstpair_post.STGP_64_ldstpair_post)

```
if !IsFeatureImplemented(FEAT_MTE) then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer t2 = UInt(Rt2);
constant integer n = UInt(Rn);
constant bits(64) offset = LSL(SignExtend(simm7, 64), LOG2_TAG_GRANULE);
constant boolean writeback = TRUE;
constant boolean postindex = TRUE;
```

#### Execute (A64.ldst.ldstpair_post.STGP_64_ldstpair_post)

```
bits(64) address;
bits(64) address2;

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

constant boolean stzgm = FALSE;
constant AccessDescriptor accdesc = CreateAccDescLDGSTG(MemOp_STORE, stzgm);

if !postindex then
    address = AddressAdd(address, offset, accdesc);

if !IsAligned(address, TAG_GRANULE) then
    constant FaultRecord fault = AlignmentFault(accdesc, address);
    AArch64.Abort(fault);

address2 = AddressIncrement(address, 8, accdesc);
Mem[address , 8, accdesc] = X[t, 64];
Mem[address2, 8, accdesc] = X[t2, 64];

AArch64.MemTag[address, accdesc] = AArch64.AllocationTagFromAddress(address);

if writeback then
    if postindex then
        address = AddressAdd(address, offset, accdesc);

    if n == 31 then
        SP[64] = address;
    else
        X[n, 64] = address;
```

### Variant: `Pre-index`
- **Assembly**: `STGP  <Xt1>, <Xt2>, [<Xn|SP>, #<imm>]!`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24  22 21  14   9   4  |
|-----------------------------------|
| 01  10  1   0   0   11  0   simm7 Rt2 Rn  Rt  |
```

#### Decode (A64.ldst.ldstpair_pre.STGP_64_ldstpair_pre)

```
if !IsFeatureImplemented(FEAT_MTE) then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer t2 = UInt(Rt2);
constant integer n = UInt(Rn);
constant bits(64) offset = LSL(SignExtend(simm7, 64), LOG2_TAG_GRANULE);
constant boolean writeback = TRUE;
constant boolean postindex = FALSE;
```

### Variant: `Signed offset`
- **Assembly**: `STGP  <Xt1>, <Xt2>, [<Xn|SP>{, #<imm>}]`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24  22 21  14   9   4  |
|-----------------------------------|
| 01  10  1   0   0   10  0   simm7 Rt2 Rn  Rt  |
```

#### Decode (A64.ldst.ldstpair_off.STGP_64_ldstpair_off)

```
if !IsFeatureImplemented(FEAT_MTE) then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer t2 = UInt(Rt2);
constant integer n = UInt(Rn);
constant bits(64) offset = LSL(SignExtend(simm7, 64), LOG2_TAG_GRANULE);
constant boolean writeback = FALSE;
constant boolean postindex = FALSE;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt1>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the first general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xt2>` | `register (64-bit)` | `Rt2` | Is the 64-bit name of the second general-purpose register to be transferred, encoded in the "Rt2" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<imm>` | `immediate` | `simm7` | For the "Post-index" and "Pre-index" variants: is the signed immediate offset, a multiple of 16 in the range -1024 to 1008, encoded in the "simm7" fie |
| `<imm>` | `immediate` | `simm7` | For the "Signed offset" variant: is the optional signed immediate offset, a multiple of 16 in the range -1024 to 1008, defaulting to 0 and encoded in  |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_MTE)` |

---
<details><summary>Metadata</summary>

- atomic-ops: `STGP-pair-64`
- isa: `A64`
- offset-type: `off7s_s`
- reg-type: `pair-64`
- source: `stgp.xml`
</details>