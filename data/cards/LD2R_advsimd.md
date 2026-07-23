## LD2R
_ARM A64 Instruction_

**Title**: LD2R -- A64 | **Class**: `advsimd` | **XML ID**: `LD2R_advsimd`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Load single 2-element structure and replicate to all lanes of two registers

**Description**:
This instruction loads a 2-element structure from memory and replicates the
structure to all the lanes of the two SIMD&FP registers.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `No offset`
- **Assembly**: `LD2R  { <Vt>.<T>, <Vt2>.<T> }, [<Xn|SP>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  27 26 25 24  22 21 20  16 15  12 11   9   4  |
|--------------------------------------------------|
| 0   Q   00  1   1   0   10  1   1   0000 0   110 0   size Rn  Rt  |
```

#### Decode (A64.ldst.asisdlso.LD2R_asisdlso_R2)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant integer m = integer UNKNOWN;
constant boolean wback = FALSE;
constant boolean nontemporal = FALSE;
constant boolean tagchecked = wback || n != 31;
```

#### Postdecode (A64.ldst.asisdlso.LD2R_asisdlso_R2)

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

#### Execute (A64.ldst.asisdlso.LD2R_asisdlso_R2)

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

### Variant: `Post-index (LD2R_asisdlsop_R2_i)` (Immediate offset)
- **Condition**: `Rm == 11111`
- **Assembly**: `LD2R  { <Vt>.<T>, <Vt2>.<T> }, [<Xn|SP>], <imm>`
- **Fixed bits**: `Rm`=`11111`
- **Bit Pattern**: `????????????????11111???????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  12 11   9   4  |
|-----------------------------------|
| 0   Q   0011011 1   1   Rm  110 0   size Rn  Rt  |
```

#### Decode (A64.ldst.asisdlsop.LD2R_asisdlsop_R2_i)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant boolean wback = TRUE;
constant boolean nontemporal = FALSE;
constant boolean tagchecked = wback || n != 31;
```

### Variant: `Post-index (LD2R_asisdlsop_RX2_r)` (Register offset)
- **Condition**: `Rm != 11111`
- **Assembly**: `LD2R  { <Vt>.<T>, <Vt2>.<T> }, [<Xn|SP>], <Xm>`
- **Fixed bits**: `Rm`=`NNNNN`
- **Bit Pattern**: `????????????????????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  12 11   9   4  |
|-----------------------------------|
| 0   Q   0011011 1   1   Rm  110 0   size Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vt>` | `register (128-bit)` | `Rt` | Is the name of the first or only SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<T>` | `arrangement` | `size:Q` | Is an arrangement specifier, |
| `<Vt2>` | `register (128-bit)` | `Rt` | Is the name of the second SIMD&FP register to be transferred, encoded as "Rt" plus 1 modulo 32. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<imm>` | `immediate` | `size` | Is the post-index immediate offset, |
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
| 00 | #2 |
| 01 | #4 |
| 10 | #8 |
| 11 | #16 |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- as-structure-org: `to-all-lanes`
- isa: `A64`
- source: `ld2r_advsimd.xml`
</details>