## LD2
_ARM A64 Instruction_

**Title**: LD2 (single structure) -- A64 | **Class**: `advsimd` | **XML ID**: `LD2_advsimd_sngl`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Load single 2-element structure to one lane of two registers

**Description**:
This instruction loads a 2-element structure
from memory and writes the result to the corresponding elements of the two
SIMD&FP registers
without affecting the other bits of the registers.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `No offset (LD2_asisdlso_B2_2b)` (8-bit)
- **Condition**: `opcode == 000`
- **Assembly**: `LD2  { <Vt>.B, <Vt2>.B }[<index>], [<Xn|SP>]`
- **Fixed bits**: `opcode`=`00`
- **Bit Pattern**: `??????????????00????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  16 15  12 11   9   4  |
|--------------------------------------|
| 0   Q   0011010 1   1   0000 0   xx0 S   size Rn  Rt  |
```

#### Decode (A64.ldst.asisdlso.LD2_asisdlso_B2_2b)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant integer m = integer UNKNOWN;
constant boolean wback = FALSE;
constant boolean nontemporal = FALSE;
constant boolean tagchecked = wback || n != 31;
```

#### Postdecode (A64.ldst.asisdlso.LD2_asisdlso_B2_2b)

```
bits(2) scale = opcode<2:1>;
constant integer selem = UInt(opcode<0>:R) + 1;
boolean replicate = FALSE;
integer index;

case scale of
    when '11'
        // load and replicate
        if L == '0' || S == '1' then EndOfDecode(Decode_UNDEF);
        scale = size;
        replicate = TRUE;
    when '00'
        index = UInt(Q:S:size);       // B[0-15]
    when '01'
        if size<0> == '1' then EndOfDecode(Decode_UNDEF);
        index = UInt(Q:S:size<1>);    // H[0-7]
    when '10'
        if size<1> == '1' then EndOfDecode(Decode_UNDEF);
        if size<0> == '0' then
            index = UInt(Q:S);        // S[0-3]
        else
            if S == '1' then EndOfDecode(Decode_UNDEF);
            index = UInt(Q);          // D[0-1]
            scale = '11';

constant integer datasize = 64 << UInt(Q);
constant integer esize = 8 << UInt(scale);
```

#### Execute (A64.ldst.asisdlso.LD2_asisdlso_B2_2b)

```
CheckFPAdvSIMDEnabled64();

bits(64) address;
bits(64) eaddr;
bits(64) offs;
bits(128) rval;
bits(esize) element;
constant integer ebytes = esize DIV 8;

constant boolean privileged = PSTATE.EL != EL0;
constant AccessDescriptor accdesc = CreateAccDescASIMD(MemOp_LOAD, nontemporal, tagchecked,
                                                       privileged);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

offs = Zeros(64);

if replicate then
    // load and replicate to all elements
    for s = 0 to selem-1
        eaddr = AddressIncrement(address, offs, accdesc);
        element = Mem[eaddr, ebytes, accdesc];
        // replicate to fill 128- or 64-bit register
        V[t, datasize] = Replicate(element, datasize DIV esize);
        offs = offs + ebytes;
        t = (t + 1) MOD 32;
else
    // load/store one element per register
    for s = 0 to selem-1
        rval = V[t, 128];
        eaddr = AddressIncrement(address, offs, accdesc);
        Elem[rval, index, esize] = Mem[eaddr, ebytes, accdesc];
        V[t, 128] = rval;
        offs = offs + ebytes;
        t = ( t + 1 ) MOD 32;
if wback then
    if m != 31 then
        offs = X[m, 64];
    address = AddressAdd(address, offs, accdesc);
    if n == 31 then
        SP[64] = address;
    else
        X[n, 64] = address;
```

#### Constraints
_4× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `L != '0' && S != '1'` |
| 🚫 ENCODING_UNDEF | `size<0> != '1'` |
| 🚫 ENCODING_UNDEF | `size<1> != '1'` |
| 🚫 ENCODING_UNDEF | `S != '1'` |

### Variant: `No offset (LD2_asisdlso_H2_2h)` (16-bit)
- **Condition**: `opcode == 010 && size == x0`
- **Assembly**: `LD2  { <Vt>.H, <Vt2>.H }[<index>], [<Xn|SP>]`
- **Fixed bits**: `opcode`=`01`, `size`=`x0`
- **Bit Pattern**: `??????????0???10????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  16 15  12 11   9   4  |
|--------------------------------------|
| 0   Q   0011010 1   1   0000 0   xx0 S   size Rn  Rt  |
```

### Variant: `No offset (LD2_asisdlso_S2_2s)` (32-bit)
- **Condition**: `opcode == 100 && size == 00`
- **Assembly**: `LD2  { <Vt>.S, <Vt2>.S }[<index>], [<Xn|SP>]`
- **Fixed bits**: `opcode`=`10`, `size`=`00`
- **Bit Pattern**: `??????????00??01????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  16 15  12 11   9   4  |
|--------------------------------------|
| 0   Q   0011010 1   1   0000 0   xx0 S   size Rn  Rt  |
```

### Variant: `No offset (LD2_asisdlso_D2_2d)` (64-bit)
- **Condition**: `opcode == 100 && S == 0 && size == 01`
- **Assembly**: `LD2  { <Vt>.D, <Vt2>.D }[<index>], [<Xn|SP>]`
- **Fixed bits**: `opcode`=`10`, `S`=`0`, `size`=`01`
- **Bit Pattern**: `??????????100?01????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  16 15  12 11   9   4  |
|--------------------------------------|
| 0   Q   0011010 1   1   0000 0   xx0 S   size Rn  Rt  |
```

### Variant: `Post-index (LD2_asisdlsop_B2_i2b)` (8-bit, immediate offset)
- **Condition**: `Rm == 11111 && opcode == 000`
- **Assembly**: `LD2  { <Vt>.B, <Vt2>.B }[<index>], [<Xn|SP>], #2`
- **Fixed bits**: `Rm`=`11111`, `opcode`=`00`
- **Bit Pattern**: `??????????????0011111???????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  12 11   9   4  |
|-----------------------------------|
| 0   Q   0011011 1   1   Rm  xx0 S   size Rn  Rt  |
```

#### Decode (A64.ldst.asisdlsop.LD2_asisdlsop_B2_i2b)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant boolean wback = TRUE;
constant boolean nontemporal = FALSE;
constant boolean tagchecked = wback || n != 31;
```

### Variant: `Post-index (LD2_asisdlsop_BX2_r2b)` (8-bit, register offset)
- **Condition**: `Rm != 11111 && opcode == 000`
- **Assembly**: `LD2  { <Vt>.B, <Vt2>.B }[<index>], [<Xn|SP>], <Xm>`
- **Fixed bits**: `Rm`=`NNNNN`, `opcode`=`00`
- **Bit Pattern**: `??????????????00????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  12 11   9   4  |
|-----------------------------------|
| 0   Q   0011011 1   1   Rm  xx0 S   size Rn  Rt  |
```

### Variant: `Post-index (LD2_asisdlsop_H2_i2h)` (16-bit, immediate offset)
- **Condition**: `Rm == 11111 && opcode == 010 && size == x0`
- **Assembly**: `LD2  { <Vt>.H, <Vt2>.H }[<index>], [<Xn|SP>], #4`
- **Fixed bits**: `Rm`=`11111`, `opcode`=`01`, `size`=`x0`
- **Bit Pattern**: `??????????0???1011111???????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  12 11   9   4  |
|-----------------------------------|
| 0   Q   0011011 1   1   Rm  xx0 S   size Rn  Rt  |
```

### Variant: `Post-index (LD2_asisdlsop_HX2_r2h)` (16-bit, register offset)
- **Condition**: `Rm != 11111 && opcode == 010 && size == x0`
- **Assembly**: `LD2  { <Vt>.H, <Vt2>.H }[<index>], [<Xn|SP>], <Xm>`
- **Fixed bits**: `Rm`=`NNNNN`, `opcode`=`01`, `size`=`x0`
- **Bit Pattern**: `??????????0???10????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  12 11   9   4  |
|-----------------------------------|
| 0   Q   0011011 1   1   Rm  xx0 S   size Rn  Rt  |
```

### Variant: `Post-index (LD2_asisdlsop_S2_i2s)` (32-bit, immediate offset)
- **Condition**: `Rm == 11111 && opcode == 100 && size == 00`
- **Assembly**: `LD2  { <Vt>.S, <Vt2>.S }[<index>], [<Xn|SP>], #8`
- **Fixed bits**: `Rm`=`11111`, `opcode`=`10`, `size`=`00`
- **Bit Pattern**: `??????????00??0111111???????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  12 11   9   4  |
|-----------------------------------|
| 0   Q   0011011 1   1   Rm  xx0 S   size Rn  Rt  |
```

### Variant: `Post-index (LD2_asisdlsop_SX2_r2s)` (32-bit, register offset)
- **Condition**: `Rm != 11111 && opcode == 100 && size == 00`
- **Assembly**: `LD2  { <Vt>.S, <Vt2>.S }[<index>], [<Xn|SP>], <Xm>`
- **Fixed bits**: `Rm`=`NNNNN`, `opcode`=`10`, `size`=`00`
- **Bit Pattern**: `??????????00??01????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  12 11   9   4  |
|-----------------------------------|
| 0   Q   0011011 1   1   Rm  xx0 S   size Rn  Rt  |
```

### Variant: `Post-index (LD2_asisdlsop_D2_i2d)` (64-bit, immediate offset)
- **Condition**: `Rm == 11111 && opcode == 100 && S == 0 && size == 01`
- **Assembly**: `LD2  { <Vt>.D, <Vt2>.D }[<index>], [<Xn|SP>], #16`
- **Fixed bits**: `Rm`=`11111`, `opcode`=`10`, `S`=`0`, `size`=`01`
- **Bit Pattern**: `??????????100?0111111???????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  12 11   9   4  |
|-----------------------------------|
| 0   Q   0011011 1   1   Rm  xx0 S   size Rn  Rt  |
```

### Variant: `Post-index (LD2_asisdlsop_DX2_r2d)` (64-bit, register offset)
- **Condition**: `Rm != 11111 && opcode == 100 && S == 0 && size == 01`
- **Assembly**: `LD2  { <Vt>.D, <Vt2>.D }[<index>], [<Xn|SP>], <Xm>`
- **Fixed bits**: `Rm`=`NNNNN`, `opcode`=`10`, `S`=`0`, `size`=`01`
- **Bit Pattern**: `??????????100?01????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  12 11   9   4  |
|-----------------------------------|
| 0   Q   0011011 1   1   Rm  xx0 S   size Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vt>` | `register (128-bit)` | `Rt` | Is the name of the first or only SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<Vt2>` | `register (128-bit)` | `Rt` | Is the name of the second SIMD&FP register to be transferred, encoded as "Rt" plus 1 modulo 32. |
| `<index>` | `unknown` | `Q:S:size` | For the "8-bit", "8-bit, immediate offset", and "8-bit, register offset" variants: is the element index, encoded in "Q:S:size". |
| `<index>` | `unknown` | `Q:S:size` | For the "16-bit", "16-bit, immediate offset", and "16-bit, register offset" variants: is the element index, encoded in "Q:S:size<1>". |
| `<index>` | `unknown` | `Q:S` | For the "32-bit", "32-bit, immediate offset", and "32-bit, register offset" variants: is the element index, encoded in "Q:S". |
| `<index>` | `unknown` | `Q` | For the "64-bit", "64-bit, immediate offset", and "64-bit, register offset" variants: is the element index, encoded in "Q". |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the general-purpose post-index register, excluding XZR, encoded in the "Rm" field. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `ld2_advsimd_sngl.xml`
</details>