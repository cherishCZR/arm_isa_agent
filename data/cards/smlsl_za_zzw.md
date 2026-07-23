## SMLSL
_ARM A64 Instruction_

**Title**: SMLSL (multiple vectors) -- A64 | **Class**: `mortlach2` | **XML ID**: `smlsl_za_zzw`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Multi-vector signed integer multiply-subtract long

**Description**:
This instruction multiplies each signed 16-bit element
in the two or four first source
vectors with each signed 16-bit element in the
two or four second source vectors, widens each product
to 32 bits, and destructively subtracts these values from
the corresponding 32-bit elements of the
ZA double-vector groups.

The double-vector
group within each half of or each quarter of the ZA array is selected by the sum
of the vector select register and offset range, modulo half or quarter the number of ZA array vectors.

The vector group symbol, VGx2 or VGx4, indicates that
the ZA operand consists of two or four ZA double-vector
groups
respectively. The vector group symbol is preferred
for disassembly, but optional in assembler source code.

This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `Two ZA double-vectors`
- **Assembly**: `SMLSL  ZA.S[<Wv>, <offs1>:<offs2>{, VGx2}], { <Zn1>.H-<Zn2>.H }, { <Zm1>.H-<Zm2>.H }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21 20  16  14  12   9   5  4  3  2  1  |
|--------------------------------------------------|
| 1   10  0000 11  1   1   Zm  00  Rv  010 Zn  0   0   1   0   off2 |
```

#### Decode (A64.sme.mortlach_multi_array_2a.mortlach_multi2_zz_za_mla_long_mm.smlsl_za_zzw_2x2)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer v = UInt('010':Rv);
constant integer n = UInt(Zn:'0');
constant integer m = UInt(Zm:'0');
constant integer offset = UInt(off2:'0');
constant integer nreg = 2;
```

#### Execute (A64.sme.mortlach_multi_array_2a.mortlach_multi2_zz_za_mla_long_mm.smlsl_za_zzw_2x2)

```
CheckStreamingSVEAndZAEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant integer vectors = VL DIV 8;
constant integer vstride = vectors DIV nreg;
constant bits(32) vbase = X[v, 32];
integer vec = (UInt(vbase) + offset) MOD vstride;
bits(VL) result;
vec = vec - (vec MOD 2);

for r = 0 to nreg-1
    constant bits(VL) operand1 = Z[n+r, VL];
    constant bits(VL) operand2 = Z[m+r, VL];
    for i = 0 to 1
        constant bits(VL) operand3 = ZAvector[vec + i, VL];
        for e = 0 to elements-1
            constant integer element1 = SInt(Elem[operand1, 2 * e + i, esize DIV 2]);
            constant integer element2 = SInt(Elem[operand2, 2 * e + i, esize DIV 2]);
            constant bits(esize) product = (element1 * element2)<esize-1:0>;
            Elem[result, e, esize] = Elem[operand3, e, esize] - product;
        ZAvector[vec + i, VL] = result;
    vec = vec + vstride;
```

### Variant: `Four ZA double-vectors`
- **Assembly**: `SMLSL  ZA.S[<Wv>, <offs1>:<offs2>{, VGx4}], { <Zn1>.H-<Zn4>.H }, { <Zm1>.H-<Zm4>.H }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21 20  17 16  14  12   9   6   4  3  2  1  |
|-----------------------------------------------------|
| 1   10  0000 11  1   1   Zm  0   10  Rv  010 Zn  00  0   1   0   off2 |
```

#### Decode (A64.sme.mortlach_multi_array_2b.mortlach_multi4_zz_za_mla_long_mm.smlsl_za_zzw_4x4)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer v = UInt('010':Rv);
constant integer n = UInt(Zn:'00');
constant integer m = UInt(Zm:'00');
constant integer offset = UInt(off2:'0');
constant integer nreg = 4;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wv>` | `register (32-bit)` | `Rv` | Is the 32-bit name of the vector select register W8-W11, encoded in the "Rv" field. |
| `<offs1>` | `unknown` | `off2` | Is the first vector select offset, encoded as "off2" field times 2. |
| `<offs2>` | `unknown` | `off2` | Is the second vector select offset, encoded as "off2" field times 2 plus 1. |
| `<Zn1>` | `register (128-bit)` | `Zn` | For the "Two ZA double-vectors" variant: is the name of the first scalable vector register of the first source multi-vector group, encoded as "Zn" tim |
| `<Zn1>` | `register (128-bit)` | `Zn` | For the "Four ZA double-vectors" variant: is the name of the first scalable vector register of the first source multi-vector group, encoded as "Zn" ti |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the first source multi-vector group, encoded as "Zn" times 2 plus 1. |
| `<Zm1>` | `register (128-bit)` | `Zm` | For the "Two ZA double-vectors" variant: is the name of the first scalable vector register of the second source multi-vector group, encoded as "Zm" ti |
| `<Zm1>` | `register (128-bit)` | `Zm` | For the "Four ZA double-vectors" variant: is the name of the first scalable vector register of the second source multi-vector group, encoded as "Zm" t |
| `<Zm2>` | `register (128-bit)` | `Zm` | Is the name of the second scalable vector register of the second source multi-vector group, encoded as "Zm" times 2 plus 1. |
| `<Zn4>` | `register (128-bit)` | `Zn` | Is the name of the fourth scalable vector register of the first source multi-vector group, encoded as "Zn" times 4 plus 3. |
| `<Zm4>` | `register (128-bit)` | `Zm` | Is the name of the fourth scalable vector register of the second source multi-vector group, encoded as "Zm" times 4 plus 3. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2)` |

### Operational Notes

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `smlsl_za_zzw.xml`
</details>