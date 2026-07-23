## STP
_ARM A64 Instruction_

**Title**: STP (SIMD&FP) -- A64 | **Class**: `fpsimd` | **XML ID**: `STP_fpsimd`

**Architecture**: `FEAT_FP` (ARMv8.0)

**Summary**: Store pair of SIMD&FP registers

**Description**:
This instruction stores a pair of SIMD&FP registers to memory.
The address used for the store is
calculated from a base register value and an immediate offset.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Post-index (STP_S_ldstpair_post)` (32-bit)
- **Condition**: `opc == 00`
- **Assembly**: `STP  <St1>, <St2>, [<Xn|SP>], #<imm>`
- **Fixed bits**: `opc`=`00`
- **Bit Pattern**: `??????????????????????????????00`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  22 21  14   9   4  |
|-----------------------------|
| opc 101 1   001 0   imm7 Rt2 Rn  Rt  |
```

#### Decode (A64.ldst.ldstpair_post.STP_S_ldstpair_post)

```
if !IsFeatureImplemented(FEAT_FP) then EndOfDecode(Decode_UNDEF);

constant boolean wback = TRUE;
constant boolean postindex = TRUE;
```

#### Postdecode (A64.ldst.ldstpair_post.STP_S_ldstpair_post)

```
constant integer t = UInt(Rt);
constant integer t2 = UInt(Rt2);
constant integer n = UInt(Rn);
constant boolean nontemporal = FALSE;
constant integer scale = 2 + (UInt(opc));
constant integer datasize = 8 << scale;
constant bits(64) offset = LSL(SignExtend(imm7, 64), scale);
constant boolean tagchecked = wback || n != 31;
```

#### Execute (A64.ldst.ldstpair_post.STP_S_ldstpair_post)

```
CheckFPEnabled64();
bits(64) address;
constant integer dbytes = datasize DIV 8;

constant boolean privileged = PSTATE.EL != EL0;
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

### Variant: `Post-index (STP_D_ldstpair_post)` (64-bit)
- **Condition**: `opc == 01`
- **Assembly**: `STP  <Dt1>, <Dt2>, [<Xn|SP>], #<imm>`
- **Fixed bits**: `opc`=`01`
- **Bit Pattern**: `??????????????????????????????10`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  22 21  14   9   4  |
|-----------------------------|
| opc 101 1   001 0   imm7 Rt2 Rn  Rt  |
```

### Variant: `Post-index (STP_Q_ldstpair_post)` (128-bit)
- **Condition**: `opc == 10`
- **Assembly**: `STP  <Qt1>, <Qt2>, [<Xn|SP>], #<imm>`
- **Fixed bits**: `opc`=`10`
- **Bit Pattern**: `??????????????????????????????01`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  22 21  14   9   4  |
|-----------------------------|
| opc 101 1   001 0   imm7 Rt2 Rn  Rt  |
```

### Variant: `Pre-index (STP_S_ldstpair_pre)` (32-bit)
- **Condition**: `opc == 00`
- **Assembly**: `STP  <St1>, <St2>, [<Xn|SP>, #<imm>]!`
- **Fixed bits**: `opc`=`00`
- **Bit Pattern**: `??????????????????????????????00`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  22 21  14   9   4  |
|-----------------------------|
| opc 101 1   011 0   imm7 Rt2 Rn  Rt  |
```

#### Decode (A64.ldst.ldstpair_pre.STP_S_ldstpair_pre)

```
if !IsFeatureImplemented(FEAT_FP) then EndOfDecode(Decode_UNDEF);

constant boolean wback = TRUE;
constant boolean postindex = FALSE;
```

### Variant: `Pre-index (STP_D_ldstpair_pre)` (64-bit)
- **Condition**: `opc == 01`
- **Assembly**: `STP  <Dt1>, <Dt2>, [<Xn|SP>, #<imm>]!`
- **Fixed bits**: `opc`=`01`
- **Bit Pattern**: `??????????????????????????????10`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  22 21  14   9   4  |
|-----------------------------|
| opc 101 1   011 0   imm7 Rt2 Rn  Rt  |
```

### Variant: `Pre-index (STP_Q_ldstpair_pre)` (128-bit)
- **Condition**: `opc == 10`
- **Assembly**: `STP  <Qt1>, <Qt2>, [<Xn|SP>, #<imm>]!`
- **Fixed bits**: `opc`=`10`
- **Bit Pattern**: `??????????????????????????????01`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  22 21  14   9   4  |
|-----------------------------|
| opc 101 1   011 0   imm7 Rt2 Rn  Rt  |
```

### Variant: `Signed offset (STP_S_ldstpair_off)` (32-bit)
- **Condition**: `opc == 00`
- **Assembly**: `STP  <St1>, <St2>, [<Xn|SP>{, #<imm>}]`
- **Fixed bits**: `opc`=`00`
- **Bit Pattern**: `??????????????????????????????00`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  22 21  14   9   4  |
|-----------------------------|
| opc 101 1   010 0   imm7 Rt2 Rn  Rt  |
```

#### Decode (A64.ldst.ldstpair_off.STP_S_ldstpair_off)

```
if !IsFeatureImplemented(FEAT_FP) then EndOfDecode(Decode_UNDEF);

constant boolean wback = FALSE;
constant boolean postindex = FALSE;
```

### Variant: `Signed offset (STP_D_ldstpair_off)` (64-bit)
- **Condition**: `opc == 01`
- **Assembly**: `STP  <Dt1>, <Dt2>, [<Xn|SP>{, #<imm>}]`
- **Fixed bits**: `opc`=`01`
- **Bit Pattern**: `??????????????????????????????10`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  22 21  14   9   4  |
|-----------------------------|
| opc 101 1   010 0   imm7 Rt2 Rn  Rt  |
```

### Variant: `Signed offset (STP_Q_ldstpair_off)` (128-bit)
- **Condition**: `opc == 10`
- **Assembly**: `STP  <Qt1>, <Qt2>, [<Xn|SP>{, #<imm>}]`
- **Fixed bits**: `opc`=`10`
- **Bit Pattern**: `??????????????????????????????01`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  22 21  14   9   4  |
|-----------------------------|
| opc 101 1   010 0   imm7 Rt2 Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<St1>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the first SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<St2>` | `register (32-bit)` | `Rt2` | Is the 32-bit name of the second SIMD&FP register to be transferred, encoded in the "Rt2" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<imm>` | `immediate` | `imm7` | For the "32-bit Post-index" and "32-bit Pre-index" variants: is the signed immediate byte offset, a multiple of 4 in the range -256 to 252, encoded in |
| `<imm>` | `immediate` | `imm7` | For the "64-bit Post-index" and "64-bit Pre-index" variants: is the signed immediate byte offset, a multiple of 8 in the range -512 to 504, encoded in |
| `<imm>` | `immediate` | `imm7` | For the "128-bit Post-index" and "128-bit Pre-index" variants: is the signed immediate byte offset, a multiple of 16 in the range -1024 to 1008, encod |
| `<imm>` | `immediate` | `imm7` | For the "32-bit Signed offset" variant: is the optional signed immediate byte offset, a multiple of 4 in the range -256 to 252, defaulting to 0 and en |
| `<imm>` | `immediate` | `imm7` | For the "64-bit Signed offset" variant: is the optional signed immediate byte offset, a multiple of 8 in the range -512 to 504, defaulting to 0 and en |
| `<imm>` | `immediate` | `imm7` | For the "128-bit Signed offset" variant: is the optional signed immediate byte offset, a multiple of 16 in the range -1024 to 1008, defaulting to 0 an |
| `<Dt1>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the first SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<Dt2>` | `register (64-bit)` | `Rt2` | Is the 64-bit name of the second SIMD&FP register to be transferred, encoded in the "Rt2" field. |
| `<Qt1>` | `register (128-bit)` | `Rt` | Is the 128-bit name of the first SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<Qt2>` | `register (128-bit)` | `Rt2` | Is the 128-bit name of the second SIMD&FP register to be transferred, encoded in the "Rt2" field. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP)` |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- isa: `A64`
- offset-type: `off7s_s`
- source: `stp_fpsimd.xml`
</details>