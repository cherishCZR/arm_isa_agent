## FTMOPA
_ARM A64 Instruction_

**Title**: FTMOPA (non-widening) -- A64 | **Class**: `mortlach2` | **XML ID**: `ftmopa_za_zzzi`

**Architecture**: `FEAT_SME_TMOP && FEAT_SME_F16F16` (FEAT_SME_TMOP && FEAT_SME_F16F16), `FEAT_SME_TMOP` (ARMv9.6)

**Summary**: Floating-point sparse outer product, accumulating

**Description**:
This instruction generates floating-point outer
product by multiplying the 1-in-2 selected elements from the
dense sub-matrices in the two first source vectors with the corresponding
elements of the compressed sparse sub-matrix in the second source vector
and accumulates the results to the destination ZA tile elements.

In case of the half-precision variant, the outer product is generated
by multiplying the selected 1-in-2 half-precision value from each overlapping
16-bit containers of the two SVLH×1 sub-matrices in
the first source vectors by the half-precision value from the corresponding 16-bit container of
the compressed 1×SVLH sub-matrix in the second source vector.
In case of the single-precision variant, the outer product is generated
by multiplying the selected 1-in-2 single-precision value from each overlapping
32-bit containers of the two SVLS×1 sub-matrices in
the first source vectors by the single-precision value from the corresponding 32-bit container of
the compressed 1×SVLS sub-matrix in the second source vector.

The 1-in-2 floating-point value in the first source vectors is selected by
2-bit controls in the indexed segment of the control vector register.
If the control bit corresponding to an element in the first source vectors is 0,
the element is discarded and does not contribute to the result. If both bits
of the 2-bit control corresponding to the elements of the first source vectors are 1,
only the element corresponding to the least significant bit is selected.

The instruction multiplies the selected elements of sub-matrices of floating-point
values held in the first source vectors by the corresponding elements of
sub-matrix of floating-point values in the second source vector. The resulting
outer product, SVLH×SVLH
in case of the half-precision variant or SVLS×SVLS in case of
the single-precision variant, is then destructively
added to the destination tile.
This is equivalent to performing a single multiply-accumulate to
each of the destination tile elements.

This instruction follows SME ZA-targeting floating-point behaviors.

This instruction is unpredicated.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `Half-precision`
- **Assembly**: `FTMOPA  <ZAda>.H, { <Zn1>.H-<Zn2>.H }, <Zm>.H, <Zk>[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  15 14 13 12 11   9   5   3  2  1  0 |
|--------------------------------------------------------|
| 1   00  0000 1   01  0   Zm  0   0   0   K   Zk  Zn  i2  1   0   0   ZAda |
```

#### Decode (A64.sme.mortlach2_ss_prod.mortlach_f16f16_1in2ss_prod.ftmopa_za_zzzi_h2x1)

```
if !IsFeatureImplemented(FEAT_SME_TMOP) || !IsFeatureImplemented(FEAT_SME_F16F16) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn:'0');
constant integer m = UInt(Zm);
constant integer k = UInt('1':K:'1':Zk);
constant integer index = UInt(i2);
constant integer da = UInt(ZAda);
constant integer esize = 16;
```

#### Execute (A64.sme.mortlach2_ss_prod.mortlach_f16f16_1in2ss_prod.ftmopa_za_zzzi_h2x1)

```
CheckStreamingSVEAndZAEnabled();
constant integer VL = CurrentVL;
constant integer dim = VL DIV esize;
constant integer csize = (VL * 2) DIV esize;
constant bits(VL) op2 = Z[m, VL];
constant bits(VL) op3 = Z[k, VL];
constant bits(csize) ctrl = Elem[op3, index, csize];
constant bits(dim*dim*esize) op4 = ZAtile[da, esize, dim*dim*esize];
bits(dim*dim*esize) result;

for row = 0 to dim-1
    for col = 0 to dim-1
        integer i = 0;
        bits(esize) elem1 = FPZero('0', esize);
        for r = 0 to 1
            constant bits(VL) op1 = Z[n+r, VL];
            if i < 1 && Elem[ctrl, 2*col + r, 1] == '1' then
                elem1 = Elem[op1, row, esize];
                i = i + 1;
        constant bits(esize) elem2 = Elem[op2, col, esize];
        constant bits(esize) sum   = Elem[op4, row*dim+col, esize];
        Elem[result, row*dim+col, esize] = FPMulAdd_ZA(sum, elem1, elem2, FPCR);
ZAtile[da, esize, dim*dim*esize] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME_TMOP) && IsFeatureImplemented(FEAT_SME_F16F16)` |

### Variant: `Single-precision`
- **Assembly**: `FTMOPA  <ZAda>.S, { <Zn1>.S-<Zn2>.S }, <Zm>.S, <Zk>[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  15 14 13 12 11   9   5   3  2  1  |
|-----------------------------------------------------|
| 1   00  0000 0   01  0   Zm  0   0   0   K   Zk  Zn  i2  0   0   ZAda |
```

#### Decode (A64.sme.mortlach2_ss_prod.mortlach_f32f32_1in2ss_prod.ftmopa_za_zzzi_s2x1)

```
if !IsFeatureImplemented(FEAT_SME_TMOP) then EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn:'0');
constant integer m = UInt(Zm);
constant integer k = UInt('1':K:'1':Zk);
constant integer index = UInt(i2);
constant integer da = UInt(ZAda);
constant integer esize = 32;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME_TMOP)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<ZAda>` | `register (128-bit)` | `ZAda` | For the "Half-precision" variant: is the name of the ZA tile ZA0-ZA1, encoded in the "ZAda" field. |
| `<ZAda>` | `register (128-bit)` | `ZAda` | For the "Single-precision" variant: is the name of the ZA tile ZA0-ZA3, encoded in the "ZAda" field. |
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first scalable vector register of the first source multi-vector group, encoded as "Zn" times 2. |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the first source multi-vector group, encoded as "Zn" times 2 plus 1. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |
| `<Zk>` | `register (128-bit)` | `K:Zk` | Is the name of the control vector register Z20-Z23 or Z28-Z31, encoded in the "K:Zk" fields. |
| `<index>` | `unknown` | `i2` | Is the control segment index, in the range 0 to 3, encoded in the "i2" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `ftmopa_za_zzzi.xml`
</details>