## UVDOT
_ARM A64 Instruction_

**Title**: UVDOT (4-way) -- A64 | **Class**: `mortlach2` | **XML ID**: `uvdot_za_zzi`

**Architecture**: `FEAT_SME2` (ARMv9.3), `FEAT_SME2 && FEAT_SME_I16I64` (FEAT_SME2 && FEAT_SME_I16I64)

**Summary**: Multi-vector unsigned integer vertical dot-product by indexed element

**Description**:
This instruction computes the
vertical dot product of the corresponding four unsigned 8-bit or 16-bit integer values held in the
four first source vectors and four unsigned 8-bit or 16-bit integer values in
the corresponding indexed 32-bit or 64-bit element of the second source vector. The widened dot product
results are destructively added to the corresponding 32-bit or 64-bit element of the ZA single-vector groups.

The groups within the second source vector are specified using an immediate element index
which selects the same group position within each 128-bit vector segment. The index
range is from 0 to one less than the number of groups per 128-bit segment.

The single-vector group within each quarter
of the ZA array is selected by the sum of the vector select register and offset, modulo
quarter the number of ZA array vectors.

The vector group symbol VGx4 indicates that the ZA operand consists
of four ZA single-vector groups. The vector group symbol is preferred
for disassembly, but optional in assembler source code.

This instruction is unpredicated.

ID_AA64SMFR0_EL1.I16I64 indicates whether the 16-bit integer variant is implemented.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `8-bit to 32-bit`
- **Assembly**: `UVDOT  ZA.S[<Wv>, <offs>{, VGx4}], { <Zn1>.B-<Zn4>.B }, <Zm>.B[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  19  15 14  12 11   9   6  5  4  3  2  |
|-----------------------------------------------------|
| 1   10  0000 1   01  01  Zm  1   Rv  0   i2  Zn  0   1   1   0   off3 |
```

#### Decode (A64.sme.mortlach_multi_indexed_3.mortlach_multi4_zza_idx_s.uvdot_za_zzi_s4xi)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer esize = 32;
constant integer n = UInt(Zn:'00');
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off3);
constant integer index = UInt(i2);
```

#### Execute (A64.sme.mortlach_multi_indexed_3.mortlach_multi4_zza_idx_s.uvdot_za_zzi_s4xi)

```
CheckStreamingSVEAndZAEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant integer vectors = VL DIV 8;
constant integer vstride = vectors DIV 4;
constant integer eltspersegment = 128 DIV esize;
constant bits(32) vbase = X[v, 32];
integer vec = (UInt(vbase) + offset) MOD vstride;
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result;

for r = 0 to 3
    constant bits(VL) operand3 = ZAvector[vec, VL];
    for e = 0 to elements-1
        constant integer segmentbase = e - (e MOD eltspersegment);
        constant integer s = segmentbase + index;
        bits(esize) sum = Elem[operand3, e, esize];
        for i = 0 to 3
            constant bits(VL) operand1 = Z[n+i, VL];
            constant integer element1 = UInt(Elem[operand1, 4 * e + r, esize DIV 4]);
            constant integer element2 = UInt(Elem[operand2, 4 * s + i, esize DIV 4]);
            sum = sum + element1 * element2;
        Elem[result, e, esize] = sum;
    ZAvector[vec, VL] = result;
    vec = vec + vstride;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2)` |

### Variant: `16-bit to 64-bit`
- **Assembly**: `UVDOT  ZA.D[<Wv>, <offs>{, VGx4}], { <Zn1>.H-<Zn4>.H }, <Zm>.H[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  19  15 14  12 11 10  9   6   4  3  2  |
|-----------------------------------------------------|
| 1   10  0000 1   11  01  Zm  1   Rv  0   1   i1  Zn  00  1   1   off3 |
```

#### Decode (A64.sme.mortlach_multi_indexed_3.mortlach_multi4_zza_idx_d.uvdot_za_zzi_d4xi)

```
if !(IsFeatureImplemented(FEAT_SME2) && IsFeatureImplemented(FEAT_SME_I16I64)) then
    EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer esize = 64;
constant integer n = UInt(Zn:'00');
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off3);
constant integer index = UInt(i1);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `!IsFeatureImplemented(FEAT_SME2) \|\| !IsFeatureImplemented(FEAT_SME_I16I64)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wv>` | `register (32-bit)` | `Rv` | Is the 32-bit name of the vector select register W8-W11, encoded in the "Rv" field. |
| `<offs>` | `unknown` | `off3` | Is the vector select offset, in the range 0 to 7, encoded in the "off3" field. |
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first scalable vector register of the first source multi-vector group, encoded as "Zn" times 4. |
| `<Zn4>` | `register (128-bit)` | `Zn` | Is the name of the fourth scalable vector register of the first source multi-vector group, encoded as "Zn" times 4 plus 3. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register Z0-Z15, encoded in the "Zm" field. |
| `<index>` | `unknown` | `i2` | For the "8-bit to 32-bit" variant: is the immediate index of a 32-bit group of four 8-bit values within each 128-bit vector segment, in the range 0 to |
| `<index>` | `unknown` | `i1` | For the "16-bit to 64-bit" variant: is the immediate index of a 64-bit group of four 16-bit values within each 128-bit vector segment, in the range 0  |

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
- source: `uvdot_za_zzi.xml`
</details>