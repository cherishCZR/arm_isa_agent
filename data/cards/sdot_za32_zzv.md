## SDOT
_ARM A64 Instruction_

**Title**: SDOT (2-way, multiple and single vector) -- A64 | **Class**: `mortlach2` | **XML ID**: `sdot_za32_zzv`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Multi-vector signed integer dot-product by vector

**Description**:
This instruction computes the dot product of two signed
16-bit integer values held in each 32-bit element of the two or four first source
vectors and two signed 16-bit integer values in the corresponding 32-bit element of the second source vector. The widened dot product result is destructively added to
the corresponding 32-bit element of the ZA single-vector groups.

The single-vector
group within each half of or each quarter of the ZA array is selected by the sum
of the vector select register and offset, modulo half or quarter the number of ZA array vectors.

The vector group symbol, VGx2 or VGx4, indicates that
the ZA operand consists of two or four ZA single-vector
groups
respectively. The vector group symbol is preferred
for disassembly, but optional in assembler source code.

This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `Two ZA single-vectors`
- **Assembly**: `SDOT  ZA.S[<Wv>, <offs>{, VGx2}], { <Zn1>.H-<Zn2>.H }, <Zm>.H`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21  19  15 14  12   9   4  3  2  |
|--------------------------------------------|
| 1   10  0000 10  1   10  Zm  0   Rv  101 Zn  0   1   off3 |
```

#### Decode (A64.sme.mortlach_multi_array_1a.mortlach_multi2_z_za_2way_dot_sm.sdot_za32_zzv_2x1)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer esize = 32;
constant integer n = UInt(Zn);
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off3);
constant integer nreg = 2;
```

#### Execute (A64.sme.mortlach_multi_array_1a.mortlach_multi2_z_za_2way_dot_sm.sdot_za32_zzv_2x1)

```
CheckStreamingSVEAndZAEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant integer vectors = VL DIV 8;
constant integer vstride = vectors DIV nreg;
constant bits(32) vbase = X[v, 32];
integer vec = (UInt(vbase) + offset) MOD vstride;
bits(VL) result;

for r = 0 to nreg-1
    constant bits(VL) operand1 = Z[(n+r) MOD 32, VL];
    constant bits(VL) operand2 = Z[m, VL];
    constant bits(VL) operand3 = ZAvector[vec, VL];
    for e = 0 to elements-1
        bits(esize) sum = Elem[operand3, e, esize];
        for i = 0 to 1
            constant integer element1 = SInt(Elem[operand1, 2 * e + i, esize DIV 2]);
            constant integer element2 = SInt(Elem[operand2, 2 * e + i, esize DIV 2]);
            sum = sum + element1 * element2;
        Elem[result, e, esize] = sum;
    ZAvector[vec, VL] = result;
    vec = vec + vstride;
```

### Variant: `Four ZA single-vectors`
- **Assembly**: `SDOT  ZA.S[<Wv>, <offs>{, VGx4}], { <Zn1>.H-<Zn4>.H }, <Zm>.H`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21  19  15 14  12   9   4  3  2  |
|--------------------------------------------|
| 1   10  0000 10  1   11  Zm  0   Rv  101 Zn  0   1   off3 |
```

#### Decode (A64.sme.mortlach_multi_array_1b.mortlach_multi4_z_za_2way_dot_sm.sdot_za32_zzv_4x1)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer esize = 32;
constant integer n = UInt(Zn);
constant integer m = UInt('0':Zm);
constant integer offset = UInt(off3);
constant integer nreg = 4;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wv>` | `register (32-bit)` | `Rv` | Is the 32-bit name of the vector select register W8-W11, encoded in the "Rv" field. |
| `<offs>` | `unknown` | `off3` | Is the vector select offset, in the range 0 to 7, encoded in the "off3" field. |
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first scalable vector register of the first source multi-vector group, encoded as "Zn". |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the first source multi-vector group, encoded as "Zn" plus 1 modulo 32. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register Z0-Z15, encoded in the "Zm" field. |
| `<Zn4>` | `register (128-bit)` | `Zn` | Is the name of the fourth scalable vector register of the first source multi-vector group, encoded as "Zn" plus 3 modulo 32. |

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
- source: `sdot_za32_zzv.xml`
</details>