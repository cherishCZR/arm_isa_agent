## ST4
_ARM A64 Instruction_

**Title**: ST4 (single structure) -- A64 | **Class**: `advsimd` | **XML ID**: `ST4_advsimd_sngl`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Store single 4-element structure from one lane of four registers

**Description**:
This instruction stores a 4-element structure to memory from
corresponding elements of four SIMD&FP registers.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `No offset (ST4_asisdlso_B4_4b)` (8-bit)
- **Condition**: `opcode == 001`
- **Assembly**: `ST4  { <Vt>.B, <Vt2>.B, <Vt3>.B, <Vt4>.B }[<index>], [<Xn|SP>]`
- **Fixed bits**: `opcode`=`00`
- **Bit Pattern**: `??????????????00????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  16 15  12 11   9   4  |
|--------------------------------------|
| 0   Q   0011010 0   1   0000 0   xx1 S   size Rn  Rt  |
```

#### Decode (A64.ldst.asisdlso.ST4_asisdlso_B4_4b)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant integer m = integer UNKNOWN;
constant boolean wback = FALSE;
constant boolean nontemporal = FALSE;
constant boolean tagchecked = wback || n != 31;
```

#### Postdecode (A64.ldst.asisdlso.ST4_asisdlso_B4_4b)

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

#### Execute (A64.ldst.asisdlso.ST4_asisdlso_B4_4b)

```
CheckFPAdvSIMDEnabled64();

bits(64) address;
bits(64) eaddr;
bits(64) offs;
bits(128) rval;
bits(esize) element;
constant integer ebytes = esize DIV 8;

constant boolean privileged = PSTATE.EL != EL0;
constant AccessDescriptor accdesc = CreateAccDescASIMD(MemOp_STORE, nontemporal, tagchecked,
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
        // extract from one lane of 128-bit register
        Mem[eaddr, ebytes, accdesc] = Elem[rval, index, esize];
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

### Variant: `No offset (ST4_asisdlso_H4_4h)` (16-bit)
- **Condition**: `opcode == 011 && size == x0`
- **Assembly**: `ST4  { <Vt>.H, <Vt2>.H, <Vt3>.H, <Vt4>.H }[<index>], [<Xn|SP>]`
- **Fixed bits**: `opcode`=`01`, `size`=`x0`
- **Bit Pattern**: `??????????0???10????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  16 15  12 11   9   4  |
|--------------------------------------|
| 0   Q   0011010 0   1   0000 0   xx1 S   size Rn  Rt  |
```

### Variant: `No offset (ST4_asisdlso_S4_4s)` (32-bit)
- **Condition**: `opcode == 101 && size == 00`
- **Assembly**: `ST4  { <Vt>.S, <Vt2>.S, <Vt3>.S, <Vt4>.S }[<index>], [<Xn|SP>]`
- **Fixed bits**: `opcode`=`10`, `size`=`00`
- **Bit Pattern**: `??????????00??01????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  16 15  12 11   9   4  |
|--------------------------------------|
| 0   Q   0011010 0   1   0000 0   xx1 S   size Rn  Rt  |
```

### Variant: `No offset (ST4_asisdlso_D4_4d)` (64-bit)
- **Condition**: `opcode == 101 && S == 0 && size == 01`
- **Assembly**: `ST4  { <Vt>.D, <Vt2>.D, <Vt3>.D, <Vt4>.D }[<index>], [<Xn|SP>]`
- **Fixed bits**: `opcode`=`10`, `S`=`0`, `size`=`01`
- **Bit Pattern**: `??????????100?01????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  16 15  12 11   9   4  |
|--------------------------------------|
| 0   Q   0011010 0   1   0000 0   xx1 S   size Rn  Rt  |
```

### Variant: `Post-index (ST4_asisdlsop_B4_i4b)` (8-bit, immediate offset)
- **Condition**: `Rm == 11111 && opcode == 001`
- **Assembly**: `ST4  { <Vt>.B, <Vt2>.B, <Vt3>.B, <Vt4>.B }[<index>], [<Xn|SP>], #4`
- **Fixed bits**: `Rm`=`11111`, `opcode`=`00`
- **Bit Pattern**: `??????????????0011111???????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  12 11   9   4  |
|-----------------------------------|
| 0   Q   0011011 0   1   Rm  xx1 S   size Rn  Rt  |
```

#### Decode (A64.ldst.asisdlsop.ST4_asisdlsop_B4_i4b)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant boolean wback = TRUE;
constant boolean nontemporal = FALSE;
constant boolean tagchecked = wback || n != 31;
```

### Variant: `Post-index (ST4_asisdlsop_BX4_r4b)` (8-bit, register offset)
- **Condition**: `Rm != 11111 && opcode == 001`
- **Assembly**: `ST4  { <Vt>.B, <Vt2>.B, <Vt3>.B, <Vt4>.B }[<index>], [<Xn|SP>], <Xm>`
- **Fixed bits**: `Rm`=`NNNNN`, `opcode`=`00`
- **Bit Pattern**: `??????????????00????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  12 11   9   4  |
|-----------------------------------|
| 0   Q   0011011 0   1   Rm  xx1 S   size Rn  Rt  |
```

### Variant: `Post-index (ST4_asisdlsop_H4_i4h)` (16-bit, immediate offset)
- **Condition**: `Rm == 11111 && opcode == 011 && size == x0`
- **Assembly**: `ST4  { <Vt>.H, <Vt2>.H, <Vt3>.H, <Vt4>.H }[<index>], [<Xn|SP>], #8`
- **Fixed bits**: `Rm`=`11111`, `opcode`=`01`, `size`=`x0`
- **Bit Pattern**: `??????????0???1011111???????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  12 11   9   4  |
|-----------------------------------|
| 0   Q   0011011 0   1   Rm  xx1 S   size Rn  Rt  |
```

### Variant: `Post-index (ST4_asisdlsop_HX4_r4h)` (16-bit, register offset)
- **Condition**: `Rm != 11111 && opcode == 011 && size == x0`
- **Assembly**: `ST4  { <Vt>.H, <Vt2>.H, <Vt3>.H, <Vt4>.H }[<index>], [<Xn|SP>], <Xm>`
- **Fixed bits**: `Rm`=`NNNNN`, `opcode`=`01`, `size`=`x0`
- **Bit Pattern**: `??????????0???10????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  12 11   9   4  |
|-----------------------------------|
| 0   Q   0011011 0   1   Rm  xx1 S   size Rn  Rt  |
```

### Variant: `Post-index (ST4_asisdlsop_S4_i4s)` (32-bit, immediate offset)
- **Condition**: `Rm == 11111 && opcode == 101 && size == 00`
- **Assembly**: `ST4  { <Vt>.S, <Vt2>.S, <Vt3>.S, <Vt4>.S }[<index>], [<Xn|SP>], #16`
- **Fixed bits**: `Rm`=`11111`, `opcode`=`10`, `size`=`00`
- **Bit Pattern**: `??????????00??0111111???????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  12 11   9   4  |
|-----------------------------------|
| 0   Q   0011011 0   1   Rm  xx1 S   size Rn  Rt  |
```

### Variant: `Post-index (ST4_asisdlsop_SX4_r4s)` (32-bit, register offset)
- **Condition**: `Rm != 11111 && opcode == 101 && size == 00`
- **Assembly**: `ST4  { <Vt>.S, <Vt2>.S, <Vt3>.S, <Vt4>.S }[<index>], [<Xn|SP>], <Xm>`
- **Fixed bits**: `Rm`=`NNNNN`, `opcode`=`10`, `size`=`00`
- **Bit Pattern**: `??????????00??01????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  12 11   9   4  |
|-----------------------------------|
| 0   Q   0011011 0   1   Rm  xx1 S   size Rn  Rt  |
```

### Variant: `Post-index (ST4_asisdlsop_D4_i4d)` (64-bit, immediate offset)
- **Condition**: `Rm == 11111 && opcode == 101 && S == 0 && size == 01`
- **Assembly**: `ST4  { <Vt>.D, <Vt2>.D, <Vt3>.D, <Vt4>.D }[<index>], [<Xn|SP>], #32`
- **Fixed bits**: `Rm`=`11111`, `opcode`=`10`, `S`=`0`, `size`=`01`
- **Bit Pattern**: `??????????100?0111111???????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  12 11   9   4  |
|-----------------------------------|
| 0   Q   0011011 0   1   Rm  xx1 S   size Rn  Rt  |
```

### Variant: `Post-index (ST4_asisdlsop_DX4_r4d)` (64-bit, register offset)
- **Condition**: `Rm != 11111 && opcode == 101 && S == 0 && size == 01`
- **Assembly**: `ST4  { <Vt>.D, <Vt2>.D, <Vt3>.D, <Vt4>.D }[<index>], [<Xn|SP>], <Xm>`
- **Fixed bits**: `Rm`=`NNNNN`, `opcode`=`10`, `S`=`0`, `size`=`01`
- **Bit Pattern**: `??????????100?01????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  12 11   9   4  |
|-----------------------------------|
| 0   Q   0011011 0   1   Rm  xx1 S   size Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vt>` | `register (128-bit)` | `Rt` | Is the name of the first or only SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<Vt2>` | `register (128-bit)` | `Rt` | Is the name of the second SIMD&FP register to be transferred, encoded as "Rt" plus 1 modulo 32. |
| `<Vt3>` | `register (128-bit)` | `Rt` | Is the name of the third SIMD&FP register to be transferred, encoded as "Rt" plus 2 modulo 32. |
| `<Vt4>` | `register (128-bit)` | `Rt` | Is the name of the fourth SIMD&FP register to be transferred, encoded as "Rt" plus 3 modulo 32. |
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
- source: `st4_advsimd_sngl.xml`
</details>