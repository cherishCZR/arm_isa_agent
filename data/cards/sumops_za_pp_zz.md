## SUMOPS
_ARM A64 Instruction_

**Title**: SUMOPS -- A64 | **Class**: `mortlach` | **XML ID**: `sumops_za_pp_zz`

**Architecture**: `FEAT_SME` (PROFILE_A), `FEAT_SME_I16I64` (ARMv9.2)

**Summary**: Signed by unsigned integer sum of outer products and subtract

**Description**:
The 8-bit integer variant works with a 32-bit element ZA tile.

The 16-bit integer variant works with a 64-bit element ZA tile.

This instruction multiplies the sub-matrix in the first source vector by the
sub-matrix in the second source vector.
In case of the 8-bit integer variant, the first source holds SVLS×4
sub-matrix of signed 8-bit integer values, and the second source holds
4×SVLS sub-matrix of unsigned 8-bit integer values.
In case of the 16-bit integer variant, the first source holds SVLD×4
sub-matrix of signed 16-bit integer values, and the second source holds
4×SVLD sub-matrix of unsigned 16-bit integer values.

Each source vector is independently predicated by a corresponding
governing predicate.
When an 8-bit source element in case of 8-bit integer variant or
a 16-bit source element in case of 16-bit integer variant
is Inactive, it is treated as having the value 0.

The resulting SVLS×SVLS widened 32-bit integer or
SVLD×SVLD widened 64-bit integer sum of outer products
is then destructively subtracted from the 32-bit integer or 64-bit integer
destination tile, respectively for 8-bit integer and 16-bit integer
instruction variants.
This is equivalent to performing a 4-way dot product and subtract from
each of the destination tile elements.

In case of the 8-bit integer variant, each 32-bit container of the first source
vector holds 4 consecutive column elements of each row of a SVLS×4
sub-matrix, and each 32-bit container of the second source vector holds
4 consecutive row elements of each column of a 4×SVLS sub-matrix.
In case of the 16-bit integer variant, each 64-bit container of the first source
vector holds 4 consecutive column elements of each row of a SVLD×4
sub-matrix, and each 64-bit container of the second source vector holds
4 consecutive row elements of each column of a 4×SVLD sub-matrix.

ID_AA64SMFR0_EL1.I16I64 indicates whether the 16-bit integer variant is implemented.

**Attributes**: Predicated; DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `32-bit`
- **Assembly**: `SUMOPS  <ZAda>.S, <Pn>/M, <Pm>/M, <Zn>.B, <Zm>.B`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  15  12   9   4  3  2  1  |
|--------------------------------------------|
| 1   01  0000 0   10  1   Zm  Pm  Pn  Zn  1   0   0   ZAda |
```

#### Decode (A64.sme.mortlach_32bit_int_prod.mortlach_i8i32_prod.sumops_za_pp_zz_32)

```
if !IsFeatureImplemented(FEAT_SME) then EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer a = UInt(Pn);
constant integer b = UInt(Pm);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(ZAda);
constant boolean op1_unsigned = FALSE;
constant boolean op2_unsigned = TRUE;
```

#### Execute (A64.sme.mortlach_32bit_int_prod.mortlach_i8i32_prod.sumops_za_pp_zz_32)

```
CheckStreamingSVEAndZAEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer dim = VL DIV esize;
constant bits(PL) mask1 = P[a, PL];
constant bits(PL) mask2 = P[b, PL];
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
constant bits(dim*dim*esize) operand3 = ZAtile[da, esize, dim*dim*esize];
bits(dim*dim*esize) result;
integer  prod;

for row = 0 to dim-1
    for col = 0 to dim-1
        bits(esize) sum = Elem[operand3, row*dim+col, esize];
        for k = 0 to 3
            if (ActivePredicateElement(mask1, 4*row + k, esize DIV 4) &&
                  ActivePredicateElement(mask2, 4*col + k, esize DIV 4)) then
                prod = (Int(Elem[operand1, 4*row + k, esize DIV 4], op1_unsigned) *
                        Int(Elem[operand2, 4*col + k, esize DIV 4], op2_unsigned));
                sum = sum - prod;
        Elem[result, row*dim+col, esize] = sum;

ZAtile[da, esize, dim*dim*esize] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME)` |

### Variant: `64-bit`
- **Assembly**: `SUMOPS  <ZAda>.D, <Pn>/M, <Pm>/M, <Zn>.H, <Zm>.H`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  24 23  21 20  15  12   9   4  3  2  |
|--------------------------------------------|
| 1   0   1   0000 0   11  1   Zm  Pm  Pn  Zn  1   0   ZAda |
```

#### Decode (A64.sme.mortlach_64bit_prod.mortlach_i16i64_prod.sumops_za_pp_zz_64)

```
if !IsFeatureImplemented(FEAT_SME_I16I64) then EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer a = UInt(Pn);
constant integer b = UInt(Pm);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(ZAda);
constant boolean op1_unsigned = FALSE;
constant boolean op2_unsigned = TRUE;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME_I16I64)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<ZAda>` | `register (128-bit)` | `ZAda` | For the "32-bit" variant: is the name of the ZA tile ZA0-ZA3, encoded in the "ZAda" field. |
| `<ZAda>` | `register (128-bit)` | `ZAda` | For the "64-bit" variant: is the name of the ZA tile ZA0-ZA7, encoded in the "ZAda" field. |
| `<Pn>` | `unknown` | `Pn` | Is the name of the first governing scalable predicate register P0-P7, encoded in the "Pn" field. |
| `<Pm>` | `unknown` | `Pm` | Is the name of the second governing scalable predicate register P0-P7, encoded in the "Pm" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

### Operational Notes

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its operand registers when its governing predicate registers contain the same value for each execution.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its operand registers when its governing predicate registers contain the same value for each execution.
                
                
                  The values of the NZCV flags.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sumops_za_pp_zz.xml`
</details>