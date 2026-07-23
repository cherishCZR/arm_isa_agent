## LD2
_ARM A64 Instruction_

**Title**: LD2 (multiple structures) -- A64 | **Class**: `advsimd` | **XML ID**: `LD2_advsimd_mult`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Load multiple 2-element structures to two registers

**Description**:
This instruction loads multiple 2-element structures
from memory and writes the result to the two SIMD&FP registers,
with de-interleaving.

For an example of de-interleaving, see LD3 (multiple structures).

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `No offset`
- **Assembly**: `LD2  { <Vt>.<T>, <Vt2>.<T> }, [<Xn|SP>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  27 26 25 24  22 21  15  11   9   4  |
|-----------------------------------------|
| 0   Q   00  1   1   0   00  1   000000 1000 size Rn  Rt  |
```

#### Decode (A64.ldst.asisdlse.LD2_asisdlse_R2)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant integer m = integer UNKNOWN;
constant boolean wback = FALSE;
constant boolean nontemporal = FALSE;
constant boolean tagchecked = wback || n != 31;
```

#### Postdecode (A64.ldst.asisdlse.LD2_asisdlse_R2)

```
constant integer datasize = 64 << UInt(Q);
constant integer esize = 8 << UInt(size);
constant integer elements = datasize DIV esize;

constant integer rpt = 1;
constant integer selem = 2;

// .1D format only permitted with LD1 & ST1
if size:Q == '110' && selem != 1 then EndOfDecode(Decode_UNDEF);
```

#### Execute (A64.ldst.asisdlse.LD2_asisdlse_R2)

```
CheckFPAdvSIMDEnabled64();

bits(64) address;
bits(64) eaddr;
bits(64) offs;
bits(datasize) rval;
integer tt;
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
for r = 0 to rpt-1
    for e = 0 to elements-1
        tt = (t + r) MOD 32;
        for s = 0 to selem-1
            rval = V[tt, datasize];
            eaddr = AddressIncrement(address, offs, accdesc);
            Elem[rval, e, esize] = Mem[eaddr, ebytes, accdesc];
            V[tt, datasize] = rval;
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
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `size:Q != '110' \|\| selem == 1` |

### Variant: `Post-index (LD2_asisdlsep_I2_i)` (Immediate offset)
- **Condition**: `Rm == 11111`
- **Assembly**: `LD2  { <Vt>.<T>, <Vt2>.<T> }, [<Xn|SP>], <imm>`
- **Fixed bits**: `Rm`=`11111`
- **Bit Pattern**: `????????????????11111???????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  11   9   4  |
|--------------------------------|
| 0   Q   0011001 1   0   Rm  1000 size Rn  Rt  |
```

#### Decode (A64.ldst.asisdlsep.LD2_asisdlsep_I2_i)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant boolean wback = TRUE;
constant boolean nontemporal = FALSE;
constant boolean tagchecked = wback || n != 31;
```

### Variant: `Post-index (LD2_asisdlsep_R2_r)` (Register offset)
- **Condition**: `Rm != 11111`
- **Assembly**: `LD2  { <Vt>.<T>, <Vt2>.<T> }, [<Xn|SP>], <Xm>`
- **Fixed bits**: `Rm`=`NNNNN`
- **Bit Pattern**: `????????????????????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15  11   9   4  |
|--------------------------------|
| 0   Q   0011001 1   0   Rm  1000 size Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vt>` | `register (128-bit)` | `Rt` | Is the name of the first or only SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<T>` | `arrangement` | `size:Q` | Is an arrangement specifier, |
| `<Vt2>` | `register (128-bit)` | `Rt` | Is the name of the second SIMD&FP register to be transferred, encoded as "Rt" plus 1 modulo 32. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<imm>` | `immediate` | `Q` | Is the post-index immediate offset, |
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
| 0 | RESERVED |
| 1 | 2D |

**<imm> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | #16 |
| 1 | #32 |

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
- source: `ld2_advsimd_mult.xml`
</details>