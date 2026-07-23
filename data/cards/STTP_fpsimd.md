## STTP
_ARM A64 Instruction_

**Title**: STTP (SIMD&FP) -- A64 | **Class**: `fpsimd` | **XML ID**: `STTP_fpsimd`

**Architecture**: `FEAT_FP && FEAT_LSUI` (FEAT_FP && FEAT_LSUI)

**Summary**: Store unprivileged pair of SIMD&FP registers

**Description**:
This instruction stores a pair of SIMD&FP registers to memory.
The address used for the store is
calculated from a base register value and an immediate offset.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

Explicit Memory  effects produced by the instruction behave as if the instruction was
  executed at EL0 if the Effective value of
  PSTATE.UAO is 0 and either:

Otherwise, the Explicit Memory  effects operate with the restrictions determined by
  the Exception level at which the instruction is executed.

### Variant: `Post-index`
- **Assembly**: `STTP  <Qt1>, <Qt2>, [<Xn|SP>], #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24  22 21  14   9   4  |
|-----------------------------------|
| 11  10  1   1   0   01  0   imm7 Rt2 Rn  Rt  |
```

#### Decode (A64.ldst.ldstpair_post.STTP_Q_ldstpair_post)

```
if !IsFeatureImplemented(FEAT_FP) || !IsFeatureImplemented(FEAT_LSUI) then
    EndOfDecode(Decode_UNDEF);

constant boolean wback = TRUE;
constant boolean postindex = TRUE;
```

#### Postdecode (A64.ldst.ldstpair_post.STTP_Q_ldstpair_post)

```
constant integer t = UInt(Rt);
constant integer t2 = UInt(Rt2);
constant integer n = UInt(Rn);
constant boolean nontemporal = FALSE;
constant integer datasize = 128;
constant bits(64) offset = LSL(SignExtend(imm7, 64), 4);
constant boolean tagchecked = wback || n != 31;
```

#### Execute (A64.ldst.ldstpair_post.STTP_Q_ldstpair_post)

```
CheckFPEnabled64();
bits(64) address;
constant integer dbytes = datasize DIV 8;

constant boolean privileged = AArch64.IsUnprivAccessPriv();
constant boolean ispair = IsFeatureImplemented(FEAT_LS64WB) && datasize == 128;
constant AccessDescriptor accdesc = CreateAccDescASIMD(MemOp_STORE, nontemporal,
                                                       tagchecked, privileged, ispair);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

if !postindex then
    address = AddressAdd(address, offset, accdesc);

if accdesc.ispair then
    bits(2*datasize) full_data;
    if BigEndian(accdesc.acctype) then
        full_data = V[t, datasize] : V[t2, datasize];
    else
        full_data = V[t2, datasize] : V[t, datasize];

    Mem[address, 2*dbytes, accdesc] = full_data;
else
    constant bits(64) address2 = AddressIncrement(address, dbytes, accdesc);
    Mem[address , dbytes, accdesc] = V[t , datasize];
    Mem[address2, dbytes, accdesc] = V[t2, datasize];

if wback then
    if postindex then
        address = AddressAdd(address, offset, accdesc);
    if n == 31 then
        SP[64] = address;
    else
        X[n, 64] = address;
```

### Variant: `Pre-index`
- **Assembly**: `STTP  <Qt1>, <Qt2>, [<Xn|SP>, #<imm>]!`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24  22 21  14   9   4  |
|-----------------------------------|
| 11  10  1   1   0   11  0   imm7 Rt2 Rn  Rt  |
```

#### Decode (A64.ldst.ldstpair_pre.STTP_Q_ldstpair_pre)

```
if !IsFeatureImplemented(FEAT_FP) || !IsFeatureImplemented(FEAT_LSUI) then
    EndOfDecode(Decode_UNDEF);

constant boolean wback = TRUE;
constant boolean postindex = FALSE;
```

### Variant: `Signed offset`
- **Assembly**: `STTP  <Qt1>, <Qt2>, [<Xn|SP>{, #<imm>}]`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24  22 21  14   9   4  |
|-----------------------------------|
| 11  10  1   1   0   10  0   imm7 Rt2 Rn  Rt  |
```

#### Decode (A64.ldst.ldstpair_off.STTP_Q_ldstpair_off)

```
if !IsFeatureImplemented(FEAT_FP) || !IsFeatureImplemented(FEAT_LSUI) then
    EndOfDecode(Decode_UNDEF);

constant boolean wback = FALSE;
constant boolean postindex = FALSE;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Qt1>` | `register (128-bit)` | `Rt` | Is the 128-bit name of the first SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<Qt2>` | `register (128-bit)` | `Rt2` | Is the 128-bit name of the second SIMD&FP register to be transferred, encoded in the "Rt2" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<imm>` | `immediate` | `imm7` | For the "Post-index" and "Pre-index" variants: is the signed immediate byte offset, a multiple of 16 in the range -1024 to 1008, encoded in the "imm7" |
| `<imm>` | `immediate` | `imm7` | For the "Signed offset" variant: is the optional signed immediate byte offset, a multiple of 16 in the range -1024 to 1008, defaulting to 0 and encode |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP) && IsFeatureImplemented(FEAT_LSUI)` |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- atomic-ops: `STTP-pair-quadwords`
- isa: `A64`
- offset-type: `off7s_s`
- reg-type: `pair-quadwords`
- source: `sttp_fpsimd.xml`
</details>