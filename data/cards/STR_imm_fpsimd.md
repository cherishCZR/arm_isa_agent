## STR
_ARM A64 Instruction_

**Title**: STR (immediate, SIMD&FP) -- A64 | **Class**: `fpsimd` | **XML ID**: `STR_imm_fpsimd`

**Architecture**: `FEAT_FP` (ARMv8.0)

**Summary**: Store SIMD&FP register (immediate offset)

**Description**:
This instruction stores a single SIMD&FP register to memory. The address that is used
for the store is calculated from a base register value and an immediate offset.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Post-index (STR_B_ldst_immpost)` (8-bit)
- **Condition**: `size == 00 && opc == 00`
- **Assembly**: `STR  <Bt>, [<Xn|SP>], #<simm>`
- **Fixed bits**: `size`=`00`, `opc`=`0`
- **Bit Pattern**: `???????????????????????0??????00`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| size 111 1   00  x0  0   imm9 01  Rn  Rt  |
```

#### Decode (A64.ldst.ldst_immpost.STR_B_ldst_immpost)

```
if !IsFeatureImplemented(FEAT_FP) then EndOfDecode(Decode_UNDEF);
if opc<1> == '1' && size != '00' then EndOfDecode(Decode_UNDEF);
constant integer scale = if opc<1> == '1' then 4 else UInt(size);
constant boolean wback = TRUE;
constant boolean postindex = TRUE;
constant bits(64) offset = SignExtend(imm9, 64);
```

#### Postdecode (A64.ldst.ldst_immpost.STR_B_ldst_immpost)

```
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant integer datasize = 8 << scale;
constant boolean nontemporal = FALSE;
constant boolean tagchecked = wback || n != 31;
```

#### Execute (A64.ldst.ldst_immpost.STR_B_ldst_immpost)

```
CheckFPEnabled64();
bits(64) address;

constant boolean privileged = PSTATE.EL != EL0;
constant AccessDescriptor accdesc = CreateAccDescASIMD(MemOp_STORE, nontemporal, tagchecked,
                                                       privileged);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

if !postindex then
    address = AddressAdd(address, offset, accdesc);

Mem[address, datasize DIV 8, accdesc] = V[t, datasize];

if wback then
    if postindex then
        address = AddressAdd(address, offset, accdesc);
    if n == 31 then
        SP[64] = address;
    else
        X[n, 64] = address;
```

### Variant: `Post-index (STR_H_ldst_immpost)` (16-bit)
- **Condition**: `size == 01 && opc == 00`
- **Assembly**: `STR  <Ht>, [<Xn|SP>], #<simm>`
- **Fixed bits**: `size`=`01`, `opc`=`0`
- **Bit Pattern**: `???????????????????????0??????10`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| size 111 1   00  x0  0   imm9 01  Rn  Rt  |
```

### Variant: `Post-index (STR_S_ldst_immpost)` (32-bit)
- **Condition**: `size == 10 && opc == 00`
- **Assembly**: `STR  <St>, [<Xn|SP>], #<simm>`
- **Fixed bits**: `size`=`10`, `opc`=`0`
- **Bit Pattern**: `???????????????????????0??????01`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| size 111 1   00  x0  0   imm9 01  Rn  Rt  |
```

### Variant: `Post-index (STR_D_ldst_immpost)` (64-bit)
- **Condition**: `size == 11 && opc == 00`
- **Assembly**: `STR  <Dt>, [<Xn|SP>], #<simm>`
- **Fixed bits**: `size`=`11`, `opc`=`0`
- **Bit Pattern**: `???????????????????????0??????11`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| size 111 1   00  x0  0   imm9 01  Rn  Rt  |
```

### Variant: `Post-index (STR_Q_ldst_immpost)` (128-bit)
- **Condition**: `size == 00 && opc == 10`
- **Assembly**: `STR  <Qt>, [<Xn|SP>], #<simm>`
- **Fixed bits**: `size`=`00`, `opc`=`1`
- **Bit Pattern**: `???????????????????????1??????00`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| size 111 1   00  x0  0   imm9 01  Rn  Rt  |
```

### Variant: `Pre-index (STR_B_ldst_immpre)` (8-bit)
- **Condition**: `size == 00 && opc == 00`
- **Assembly**: `STR  <Bt>, [<Xn|SP>, #<simm>]!`
- **Fixed bits**: `size`=`00`, `opc`=`0`
- **Bit Pattern**: `???????????????????????0??????00`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| size 111 1   00  x0  0   imm9 11  Rn  Rt  |
```

#### Decode (A64.ldst.ldst_immpre.STR_B_ldst_immpre)

```
if !IsFeatureImplemented(FEAT_FP) then EndOfDecode(Decode_UNDEF);
if opc<1> == '1' && size != '00' then EndOfDecode(Decode_UNDEF);
constant integer scale = if opc<1> == '1' then 4 else UInt(size);
constant boolean wback = TRUE;
constant boolean postindex = FALSE;
constant bits(64) offset = SignExtend(imm9, 64);
```

### Variant: `Pre-index (STR_H_ldst_immpre)` (16-bit)
- **Condition**: `size == 01 && opc == 00`
- **Assembly**: `STR  <Ht>, [<Xn|SP>, #<simm>]!`
- **Fixed bits**: `size`=`01`, `opc`=`0`
- **Bit Pattern**: `???????????????????????0??????10`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| size 111 1   00  x0  0   imm9 11  Rn  Rt  |
```

### Variant: `Pre-index (STR_S_ldst_immpre)` (32-bit)
- **Condition**: `size == 10 && opc == 00`
- **Assembly**: `STR  <St>, [<Xn|SP>, #<simm>]!`
- **Fixed bits**: `size`=`10`, `opc`=`0`
- **Bit Pattern**: `???????????????????????0??????01`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| size 111 1   00  x0  0   imm9 11  Rn  Rt  |
```

### Variant: `Pre-index (STR_D_ldst_immpre)` (64-bit)
- **Condition**: `size == 11 && opc == 00`
- **Assembly**: `STR  <Dt>, [<Xn|SP>, #<simm>]!`
- **Fixed bits**: `size`=`11`, `opc`=`0`
- **Bit Pattern**: `???????????????????????0??????11`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| size 111 1   00  x0  0   imm9 11  Rn  Rt  |
```

### Variant: `Pre-index (STR_Q_ldst_immpre)` (128-bit)
- **Condition**: `size == 00 && opc == 10`
- **Assembly**: `STR  <Qt>, [<Xn|SP>, #<simm>]!`
- **Fixed bits**: `size`=`00`, `opc`=`1`
- **Bit Pattern**: `???????????????????????1??????00`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| size 111 1   00  x0  0   imm9 11  Rn  Rt  |
```

### Variant: `Unsigned offset (STR_B_ldst_pos)` (8-bit)
- **Condition**: `size == 00 && opc == 00`
- **Assembly**: `STR  <Bt>, [<Xn|SP>{, #<pimm>}]`
- **Fixed bits**: `size`=`00`, `opc`=`0`
- **Bit Pattern**: `???????????????????????0??????00`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21   9   4  |
|--------------------------|
| size 111 1   01  x0  imm12 Rn  Rt  |
```

#### Decode (A64.ldst.ldst_pos.STR_B_ldst_pos)

```
if !IsFeatureImplemented(FEAT_FP) then EndOfDecode(Decode_UNDEF);
if opc<1> == '1' && size != '00' then EndOfDecode(Decode_UNDEF);
constant integer scale = if opc<1> == '1' then 4 else UInt(size);
constant boolean wback = FALSE;
constant boolean postindex = FALSE;
constant bits(64) offset = LSL(ZeroExtend(imm12, 64), scale);
```

### Variant: `Unsigned offset (STR_H_ldst_pos)` (16-bit)
- **Condition**: `size == 01 && opc == 00`
- **Assembly**: `STR  <Ht>, [<Xn|SP>{, #<pimm>}]`
- **Fixed bits**: `size`=`01`, `opc`=`0`
- **Bit Pattern**: `???????????????????????0??????10`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21   9   4  |
|--------------------------|
| size 111 1   01  x0  imm12 Rn  Rt  |
```

### Variant: `Unsigned offset (STR_S_ldst_pos)` (32-bit)
- **Condition**: `size == 10 && opc == 00`
- **Assembly**: `STR  <St>, [<Xn|SP>{, #<pimm>}]`
- **Fixed bits**: `size`=`10`, `opc`=`0`
- **Bit Pattern**: `???????????????????????0??????01`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21   9   4  |
|--------------------------|
| size 111 1   01  x0  imm12 Rn  Rt  |
```

### Variant: `Unsigned offset (STR_D_ldst_pos)` (64-bit)
- **Condition**: `size == 11 && opc == 00`
- **Assembly**: `STR  <Dt>, [<Xn|SP>{, #<pimm>}]`
- **Fixed bits**: `size`=`11`, `opc`=`0`
- **Bit Pattern**: `???????????????????????0??????11`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21   9   4  |
|--------------------------|
| size 111 1   01  x0  imm12 Rn  Rt  |
```

### Variant: `Unsigned offset (STR_Q_ldst_pos)` (128-bit)
- **Condition**: `size == 00 && opc == 10`
- **Assembly**: `STR  <Qt>, [<Xn|SP>{, #<pimm>}]`
- **Fixed bits**: `size`=`00`, `opc`=`1`
- **Bit Pattern**: `???????????????????????1??????00`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21   9   4  |
|--------------------------|
| size 111 1   01  x0  imm12 Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Bt>` | `register (8-bit)` | `Rt` | Is the 8-bit name of the SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<simm>` | `immediate` | `imm9` | Is the signed immediate byte offset, in the range -256 to 255, encoded in the "imm9" field. |
| `<Ht>` | `register (16-bit)` | `Rt` | Is the 16-bit name of the SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<St>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<Dt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<Qt>` | `register (128-bit)` | `Rt` | Is the 128-bit name of the SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<pimm>` | `immediate` | `imm12` | For the "8-bit" variant: is the optional positive immediate byte offset, in the range 0 to 4095, defaulting to 0 and encoded in the "imm12" field. |
| `<pimm>` | `immediate` | `imm12` | For the "16-bit" variant: is the optional positive immediate byte offset, a multiple of 2 in the range 0 to 8190, defaulting to 0 and encoded in the " |
| `<pimm>` | `immediate` | `imm12` | For the "32-bit" variant: is the optional positive immediate byte offset, a multiple of 4 in the range 0 to 16380, defaulting to 0 and encoded in the  |
| `<pimm>` | `immediate` | `imm12` | For the "64-bit" variant: is the optional positive immediate byte offset, a multiple of 8 in the range 0 to 32760, defaulting to 0 and encoded in the  |
| `<pimm>` | `immediate` | `imm12` | For the "128-bit" variant: is the optional positive immediate byte offset, a multiple of 16 in the range 0 to 65520, defaulting to 0 and encoded in th |

### Encoding Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP)` |
| 🚫 ENCODING_UNDEF | `opc<1> != '1' \|\| size == '00'` |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `str_imm_fpsimd.xml`
</details>