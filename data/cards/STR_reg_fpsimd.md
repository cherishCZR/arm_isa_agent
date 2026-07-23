## STR
_ARM A64 Instruction_

**Title**: STR (register, SIMD&FP) -- A64 | **Class**: `fpsimd` | **XML ID**: `STR_reg_fpsimd`

**Architecture**: `FEAT_FP` (ARMv8.0)

**Summary**: Store SIMD&FP register (register offset)

**Description**:
This instruction stores a single SIMD&FP register to memory.
The address that is used for the store is
calculated from a base register value and an offset register value.
The offset can be optionally shifted and extended.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `SIMD&FP registers (STR_B_ldst_regoff)` (8-bit)
- **Condition**: `size == 00 && opc == 00 && option != 011`
- **Assembly**: `STR  <Bt>, [<Xn|SP>, (<Wm>|<Xm>), <extend> {<amount>}]`
- **Fixed bits**: `size`=`00`, `opc`=`0`, `option`=`ZNN`
- **Bit Pattern**: `???????????????????????0??????00`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  15  12 11   9   4  |
|--------------------------------------|
| size 111 1   00  x0  1   Rm  option S   10  Rn  Rt  |
```

#### Decode (A64.ldst.ldst_regoff.STR_B_ldst_regoff)

```
if !IsFeatureImplemented(FEAT_FP) then EndOfDecode(Decode_UNDEF);
if option<1> == '0' then EndOfDecode(Decode_UNDEF);             // sub-word index
if opc<1> == '1' && size != '00' then EndOfDecode(Decode_UNDEF);
constant integer scale = if opc<1> == '1' then 4 else UInt(size);
constant ExtendType extend_type = DecodeRegExtend(option);
constant integer shift = if S == '1' then scale else 0;
```

#### Postdecode (A64.ldst.ldst_regoff.STR_B_ldst_regoff)

```
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer datasize = 8 << scale;
constant boolean nontemporal = FALSE;
constant boolean tagchecked = TRUE;
```

#### Execute (A64.ldst.ldst_regoff.STR_B_ldst_regoff)

```
CheckFPEnabled64();
constant bits(64) offset = ExtendReg(m, extend_type, shift, 64);
bits(64) address;

constant boolean privileged = PSTATE.EL != EL0;
constant AccessDescriptor accdesc = CreateAccDescASIMD(MemOp_STORE, nontemporal, tagchecked,
                                                       privileged);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

address = AddressAdd(address, offset, accdesc);

Mem[address, datasize DIV 8, accdesc] = V[t, datasize];
```

#### Constraints
_2× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP)` |
| 🚫 ENCODING_UNDEF | `option<1> != '0'` |
| 🚫 ENCODING_UNDEF | `opc<1> != '1' \|\| size == '00'` |

### Variant: `SIMD&FP registers (STR_BL_ldst_regoff)` (8-bit)
- **Condition**: `size == 00 && opc == 00 && option == 011`
- **Assembly**: `STR  <Bt>, [<Xn|SP>, <Xm>{, LSL <amount>}]`
- **Fixed bits**: `size`=`00`, `opc`=`0`, `option`=`011`
- **Bit Pattern**: `?????????????110???????0??????00`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  15  12 11   9   4  |
|--------------------------------------|
| size 111 1   00  x0  1   Rm  option S   10  Rn  Rt  |
```

### Variant: `SIMD&FP registers (STR_H_ldst_regoff)` (16-bit)
- **Condition**: `size == 01 && opc == 00`
- **Assembly**: `STR  <Ht>, [<Xn|SP>, (<Wm>|<Xm>){, <extend> {<amount>}}]`
- **Fixed bits**: `size`=`01`, `opc`=`0`
- **Bit Pattern**: `???????????????????????0??????10`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  15  12 11   9   4  |
|--------------------------------------|
| size 111 1   00  x0  1   Rm  option S   10  Rn  Rt  |
```

### Variant: `SIMD&FP registers (STR_S_ldst_regoff)` (32-bit)
- **Condition**: `size == 10 && opc == 00`
- **Assembly**: `STR  <St>, [<Xn|SP>, (<Wm>|<Xm>){, <extend> {<amount>}}]`
- **Fixed bits**: `size`=`10`, `opc`=`0`
- **Bit Pattern**: `???????????????????????0??????01`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  15  12 11   9   4  |
|--------------------------------------|
| size 111 1   00  x0  1   Rm  option S   10  Rn  Rt  |
```

### Variant: `SIMD&FP registers (STR_D_ldst_regoff)` (64-bit)
- **Condition**: `size == 11 && opc == 00`
- **Assembly**: `STR  <Dt>, [<Xn|SP>, (<Wm>|<Xm>){, <extend> {<amount>}}]`
- **Fixed bits**: `size`=`11`, `opc`=`0`
- **Bit Pattern**: `???????????????????????0??????11`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  15  12 11   9   4  |
|--------------------------------------|
| size 111 1   00  x0  1   Rm  option S   10  Rn  Rt  |
```

### Variant: `SIMD&FP registers (STR_Q_ldst_regoff)` (128-bit)
- **Condition**: `size == 00 && opc == 10`
- **Assembly**: `STR  <Qt>, [<Xn|SP>, (<Wm>|<Xm>){, <extend> {<amount>}}]`
- **Fixed bits**: `size`=`00`, `opc`=`1`
- **Bit Pattern**: `???????????????????????1??????00`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  15  12 11   9   4  |
|--------------------------------------|
| size 111 1   00  x0  1   Rm  option S   10  Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Bt>` | `register (8-bit)` | `Rt` | Is the 8-bit name of the SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<Wm>` | `register (32-bit)` | `Rm` | When option<0> is set to 0, is the 32-bit name of the general-purpose index register, encoded in the "Rm" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | When option<0> is set to 1, is the 64-bit name of the general-purpose index register, encoded in the "Rm" field. |
| `<extend>` | `shift` | `option` | For the "8-bit" variant: is the index extend specifier, |
| `<extend>` | `shift` | `option` | For the "128-bit", "16-bit", "32-bit", and "64-bit" variants: is the index extend/shift specifier, defaulting to LSL, and which must be omitted for th |
| `<amount>` | `unknown` | `S` | For the "8-bit" variant: is the index shift amount, it must be #0, encoded in "S" as 0 if omitted, or as 1 if present. |
| `<amount>` | `unknown` | `S` | For the "16-bit" variant: is the index shift amount, optional only when <extend> is not LSL. Where it is permitted to be optional, it defaults to #0.  |
| `<amount>` | `unknown` | `S` | For the "32-bit" variant: is the index shift amount, optional only when <extend> is not LSL. Where it is permitted to be optional, it defaults to #0.  |
| `<amount>` | `unknown` | `S` | For the "64-bit" variant: is the index shift amount, optional only when <extend> is not LSL. Where it is permitted to be optional, it defaults to #0.  |
| `<amount>` | `unknown` | `S` | For the "128-bit" variant: is the index shift amount, optional only when <extend> is not LSL. Where it is permitted to be optional, it defaults to #0. |
| `<Ht>` | `register (16-bit)` | `Rt` | Is the 16-bit name of the SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<St>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<Dt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<Qt>` | `register (128-bit)` | `Rt` | Is the 128-bit name of the SIMD&FP register to be transferred, encoded in the "Rt" field. |

**<extend> Value Table**:

| bitfield | symbol |
|---|---|
| 010 | UXTW |
| 110 | SXTW |
| 111 | SXTX |

**<extend> Value Table**:

| bitfield | symbol |
|---|---|
| 010 | UXTW |
| 011 | LSL |
| 110 | SXTW |
| 111 | SXTX |

**<amount> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | #0 |
| 1 | #1 |

**<amount> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | #0 |
| 1 | #2 |

**<amount> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | #0 |
| 1 | #3 |

**<amount> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | #0 |
| 1 | #4 |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- isa: `A64`
- offset-type: `off-reg`
- source: `str_reg_fpsimd.xml`
</details>