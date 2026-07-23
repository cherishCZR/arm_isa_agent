## SUB
_ARM A64 Instruction_

**Title**: SUB (array results, multiple vectors) -- A64 | **Class**: `mortlach2` | **XML ID**: `sub_za_zzw`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Subtract multi-vector from multi-vector with ZA array vector results

**Description**:
This instruction subtracts all corresponding elements of the two or four second
source vectors from
first source vectors and places
the results in the corresponding elements of the ZA single-vector groups.

The single-vector
group within each half of or each quarter of the ZA array is selected by the sum
of the vector select register and offset, modulo half or quarter the number of ZA array vectors.

The vector group symbol, VGx2 or VGx4, indicates that
the ZA operand consists of two or four ZA single-vector
groups
respectively. The vector group symbol is preferred
for disassembly, but optional in assembler source code.

This instruction is unpredicated.

ID_AA64SMFR0_EL1.I16I64 indicates whether the 64-bit integer variant is implemented.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `Two ZA single-vectors`
- **Assembly**: `SUB  ZA.<T>[<Wv>, <offs>{, VGx2}], { <Zn1>.<T>-<Zn2>.<T> }, { <Zm1>.<T>-<Zm2>.<T> }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21 20  16  14  12   9   5  4  3  2  |
|-----------------------------------------------|
| 1   10  0000 11  sz  1   Zm  00  Rv  110 Zn  0   1   1   off3 |
```

#### Decode (A64.sme.mortlach_multi_array_2a.mortlach_multi2_zz_za_int_mm.sub_za_zzw_2x2)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
if sz == '1' && !IsFeatureImplemented(FEAT_SME_I16I64) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer esize = 32 << UInt(sz);
constant integer n = UInt(Zn:'0');
constant integer m = UInt(Zm:'0');
constant integer offset = UInt(off3);
constant integer nreg = 2;
```

#### Execute (A64.sme.mortlach_multi_array_2a.mortlach_multi2_zz_za_int_mm.sub_za_zzw_2x2)

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
    constant bits(VL) operand1 = Z[n+r, VL];
    constant bits(VL) operand2 = Z[m+r, VL];
    for e = 0 to elements-1
        constant bits(esize) element1 = Elem[operand1, e, esize];
        constant bits(esize) element2 = Elem[operand2, e, esize];
        Elem[result, e, esize] = element1 - element2;
    ZAvector[vec, VL] = result;
    vec = vec + vstride;
```

### Variant: `Four ZA single-vectors`
- **Assembly**: `SUB  ZA.<T>[<Wv>, <offs>{, VGx4}], { <Zn1>.<T>-<Zn4>.<T> }, { <Zm1>.<T>-<Zm4>.<T> }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21 20  17 16  14  12   9   6   4  3  2  |
|--------------------------------------------------|
| 1   10  0000 11  sz  1   Zm  0   10  Rv  110 Zn  00  1   1   off3 |
```

#### Decode (A64.sme.mortlach_multi_array_2b.mortlach_multi4_zz_za_int_mm.sub_za_zzw_4x4)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
if sz == '1' && !IsFeatureImplemented(FEAT_SME_I16I64) then EndOfDecode(Decode_UNDEF);
constant integer v = UInt('010':Rv);
constant integer esize = 32 << UInt(sz);
constant integer n = UInt(Zn:'00');
constant integer m = UInt(Zm:'00');
constant integer offset = UInt(off3);
constant integer nreg = 4;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<T>` | `unknown` | `sz` | Is the size specifier, |
| `<Wv>` | `register (32-bit)` | `Rv` | Is the 32-bit name of the vector select register W8-W11, encoded in the "Rv" field. |
| `<offs>` | `unknown` | `off3` | Is the vector select offset, in the range 0 to 7, encoded in the "off3" field. |
| `<Zn1>` | `register (128-bit)` | `Zn` | For the "Two ZA single-vectors" variant: is the name of the first scalable vector register of the first source multi-vector group, encoded as "Zn" tim |
| `<Zn1>` | `register (128-bit)` | `Zn` | For the "Four ZA single-vectors" variant: is the name of the first scalable vector register of the first source multi-vector group, encoded as "Zn" ti |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the first source multi-vector group, encoded as "Zn" times 2 plus 1. |
| `<Zm1>` | `register (128-bit)` | `Zm` | For the "Two ZA single-vectors" variant: is the name of the first scalable vector register of the second source multi-vector group, encoded as "Zm" ti |
| `<Zm1>` | `register (128-bit)` | `Zm` | For the "Four ZA single-vectors" variant: is the name of the first scalable vector register of the second source multi-vector group, encoded as "Zm" t |
| `<Zm2>` | `register (128-bit)` | `Zm` | Is the name of the second scalable vector register of the second source multi-vector group, encoded as "Zm" times 2 plus 1. |
| `<Zn4>` | `register (128-bit)` | `Zn` | Is the name of the fourth scalable vector register of the first source multi-vector group, encoded as "Zn" times 4 plus 3. |
| `<Zm4>` | `register (128-bit)` | `Zm` | Is the name of the fourth scalable vector register of the second source multi-vector group, encoded as "Zm" times 4 plus 3. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | S |
| 1 | D |

### Encoding Constraints
_2× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2)` |
| 🔒 FEATURE_GATE | `sz != '1' \|\| IsFeatureImplemented(FEAT_SME_I16I64)` |

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
- source: `sub_za_zzw.xml`
</details>