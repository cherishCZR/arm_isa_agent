## ST1
_ARM A64 Instruction_

**Title**: ST1 (multiple structures) -- A64 | **Class**: `advsimd` | **XML ID**: `ST1_advsimd_mult`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Store multiple single-element structures from one, two, three, or four registers

**Description**:
This instruction stores elements to memory from one, two, three, or four
SIMD&FP registers, without interleaving. Every element of each register is stored.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `No offset (ST1_asisdlse_R1_1v)` (One register)
- **Condition**: `opcode == 0111`
- **Assembly**: `ST1  { <Vt>.<T> }, [<Xn|SP>]`
- **Fixed bits**: `opcode`=`011`
- **Bit Pattern**: `????????????1?10????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21  15  11   9   4  |
|-----------------------------|
| 0   Q   0011000 0   000000 xx1x size Rn  Rt  |
```

#### Decode (A64.ldst.asisdlse.ST1_asisdlse_R1_1v)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant integer m = integer UNKNOWN;
constant boolean wback = FALSE;
constant boolean nontemporal = FALSE;
constant boolean tagchecked = wback || n != 31;
```

#### Postdecode (A64.ldst.asisdlse.ST1_asisdlse_R1_1v)

```
constant integer datasize = 64 << UInt(Q);
constant integer esize = 8 << UInt(size);
constant integer elements = datasize DIV esize;

integer rpt;                // number of iterations
constant integer selem = 1; // structure elements

case opcode of
    when '0010' rpt = 4;    // LD/ST1 (4 registers)
    when '0110' rpt = 3;    // LD/ST1 (3 registers)
    when '1010' rpt = 2;    // LD/ST1 (2 registers)
    when '0111' rpt = 1;    // LD/ST1 (1 register)
    otherwise EndOfDecode(Decode_UNDEF);
```

#### Execute (A64.ldst.asisdlse.ST1_asisdlse_R1_1v)

```
CheckFPAdvSIMDEnabled64();

bits(64) address;
bits(64) eaddr;
bits(64) offs;
bits(datasize) rval;
integer tt;
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
for r = 0 to rpt-1
    for e = 0 to elements-1
        tt = (t + r) MOD 32;
        for s = 0 to selem-1
            rval = V[tt, datasize];
            eaddr = AddressIncrement(address, offs, accdesc);
            Mem[eaddr, ebytes, accdesc] = Elem[rval, e, esize];
            offs = offs + ebytes;
            tt = (tt + 1) MOD 32;
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
_1× ↩ DECODE_FALLBACK_

| Type | Condition |
|---|---|
| ↩ DECODE_FALLBACK | `matching encodings` |

### Variant: `No offset (ST1_asisdlse_R2_2v)` (Two registers)
- **Condition**: `opcode == 1010`
- **Assembly**: `ST1  { <Vt>.<T>, <Vt2>.<T> }, [<Xn|SP>]`
- **Fixed bits**: `opcode`=`100`
- **Bit Pattern**: `????????????0?01????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21  15  11   9   4  |
|-----------------------------|
| 0   Q   0011000 0   000000 xx1x size Rn  Rt  |
```

### Variant: `No offset (ST1_asisdlse_R3_3v)` (Three registers)
- **Condition**: `opcode == 0110`
- **Assembly**: `ST1  { <Vt>.<T>, <Vt2>.<T>, <Vt3>.<T> }, [<Xn|SP>]`
- **Fixed bits**: `opcode`=`010`
- **Bit Pattern**: `????????????0?10????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21  15  11   9   4  |
|-----------------------------|
| 0   Q   0011000 0   000000 xx1x size Rn  Rt  |
```

### Variant: `No offset (ST1_asisdlse_R4_4v)` (Four registers)
- **Condition**: `opcode == 0010`
- **Assembly**: `ST1  { <Vt>.<T>, <Vt2>.<T>, <Vt3>.<T>, <Vt4>.<T> }, [<Xn|SP>]`
- **Fixed bits**: `opcode`=`000`
- **Bit Pattern**: `????????????0?00????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21  15  11   9   4  |
|-----------------------------|
| 0   Q   0011000 0   000000 xx1x size Rn  Rt  |
```

### Variant: `Post-index (ST1_asisdlsep_I1_i1)` (One register, immediate offset)
- **Condition**: `Rm == 11111 && opcode == 0111`
- **Assembly**: `ST1  { <Vt>.<T> }, [<Xn|SP>], <imm>`
- **Fixed bits**: `Rm`=`11111`, `opcode`=`011`
- **Bit Pattern**: `????????????1?1011111???????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  11   9   4  |
|--------------------------------|
| 0   Q   0011001 0   0   Rm  xx1x size Rn  Rt  |
```

#### Decode (A64.ldst.asisdlsep.ST1_asisdlsep_I1_i1)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant boolean wback = TRUE;
constant boolean nontemporal = FALSE;
constant boolean tagchecked = wback || n != 31;
```

### Variant: `Post-index (ST1_asisdlsep_R1_r1)` (One register, register offset)
- **Condition**: `Rm != 11111 && opcode == 0111`
- **Assembly**: `ST1  { <Vt>.<T> }, [<Xn|SP>], <Xm>`
- **Fixed bits**: `Rm`=`NNNNN`, `opcode`=`011`
- **Bit Pattern**: `????????????1?10????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  11   9   4  |
|--------------------------------|
| 0   Q   0011001 0   0   Rm  xx1x size Rn  Rt  |
```

### Variant: `Post-index (ST1_asisdlsep_I2_i2)` (Two registers, immediate offset)
- **Condition**: `Rm == 11111 && opcode == 1010`
- **Assembly**: `ST1  { <Vt>.<T>, <Vt2>.<T> }, [<Xn|SP>], <imm>`
- **Fixed bits**: `Rm`=`11111`, `opcode`=`100`
- **Bit Pattern**: `????????????0?0111111???????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  11   9   4  |
|--------------------------------|
| 0   Q   0011001 0   0   Rm  xx1x size Rn  Rt  |
```

### Variant: `Post-index (ST1_asisdlsep_R2_r2)` (Two registers, register offset)
- **Condition**: `Rm != 11111 && opcode == 1010`
- **Assembly**: `ST1  { <Vt>.<T>, <Vt2>.<T> }, [<Xn|SP>], <Xm>`
- **Fixed bits**: `Rm`=`NNNNN`, `opcode`=`100`
- **Bit Pattern**: `????????????0?01????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  11   9   4  |
|--------------------------------|
| 0   Q   0011001 0   0   Rm  xx1x size Rn  Rt  |
```

### Variant: `Post-index (ST1_asisdlsep_I3_i3)` (Three registers, immediate offset)
- **Condition**: `Rm == 11111 && opcode == 0110`
- **Assembly**: `ST1  { <Vt>.<T>, <Vt2>.<T>, <Vt3>.<T> }, [<Xn|SP>], <imm>`
- **Fixed bits**: `Rm`=`11111`, `opcode`=`010`
- **Bit Pattern**: `????????????0?1011111???????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  11   9   4  |
|--------------------------------|
| 0   Q   0011001 0   0   Rm  xx1x size Rn  Rt  |
```

### Variant: `Post-index (ST1_asisdlsep_R3_r3)` (Three registers, register offset)
- **Condition**: `Rm != 11111 && opcode == 0110`
- **Assembly**: `ST1  { <Vt>.<T>, <Vt2>.<T>, <Vt3>.<T> }, [<Xn|SP>], <Xm>`
- **Fixed bits**: `Rm`=`NNNNN`, `opcode`=`010`
- **Bit Pattern**: `????????????0?10????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  11   9   4  |
|--------------------------------|
| 0   Q   0011001 0   0   Rm  xx1x size Rn  Rt  |
```

### Variant: `Post-index (ST1_asisdlsep_I4_i4)` (Four registers, immediate offset)
- **Condition**: `Rm == 11111 && opcode == 0010`
- **Assembly**: `ST1  { <Vt>.<T>, <Vt2>.<T>, <Vt3>.<T>, <Vt4>.<T> }, [<Xn|SP>], <imm>`
- **Fixed bits**: `Rm`=`11111`, `opcode`=`000`
- **Bit Pattern**: `????????????0?0011111???????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  11   9   4  |
|--------------------------------|
| 0   Q   0011001 0   0   Rm  xx1x size Rn  Rt  |
```

### Variant: `Post-index (ST1_asisdlsep_R4_r4)` (Four registers, register offset)
- **Condition**: `Rm != 11111 && opcode == 0010`
- **Assembly**: `ST1  { <Vt>.<T>, <Vt2>.<T>, <Vt3>.<T>, <Vt4>.<T> }, [<Xn|SP>], <Xm>`
- **Fixed bits**: `Rm`=`NNNNN`, `opcode`=`000`
- **Bit Pattern**: `????????????0?00????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  11   9   4  |
|--------------------------------|
| 0   Q   0011001 0   0   Rm  xx1x size Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vt>` | `register (128-bit)` | `Rt` | Is the name of the first or only SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<T>` | `arrangement` | `size:Q` | Is an arrangement specifier, |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<Vt2>` | `register (128-bit)` | `Rt` | Is the name of the second SIMD&FP register to be transferred, encoded as "Rt" plus 1 modulo 32. |
| `<Vt3>` | `register (128-bit)` | `Rt` | Is the name of the third SIMD&FP register to be transferred, encoded as "Rt" plus 2 modulo 32. |
| `<Vt4>` | `register (128-bit)` | `Rt` | Is the name of the fourth SIMD&FP register to be transferred, encoded as "Rt" plus 3 modulo 32. |
| `<imm>` | `immediate` | `Q` | For the "One register, immediate offset" variant: is the post-index immediate offset, |
| `<imm>` | `immediate` | `Q` | For the "Two registers, immediate offset" variant: is the post-index immediate offset, |
| `<imm>` | `immediate` | `Q` | For the "Three registers, immediate offset" variant: is the post-index immediate offset, |
| `<imm>` | `immediate` | `Q` | For the "Four registers, immediate offset" variant: is the post-index immediate offset, |
| `<Xm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the general-purpose post-index register, excluding XZR, encoded in the "Rm" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 8B |
| 1 | 16B |
| 0 | 4H |
| 1 | 8H |
| 0 | 2S |
| 1 | 4S |
| 0 | 1D |
| 1 | 2D |

**<imm> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | #8 |
| 1 | #16 |

**<imm> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | #16 |
| 1 | #32 |

**<imm> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | #24 |
| 1 | #48 |

**<imm> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | #32 |
| 1 | #64 |

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
- source: `st1_advsimd_mult.xml`
</details>