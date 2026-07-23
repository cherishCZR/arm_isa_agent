## UMOPS
_ARM A64 Instruction_

**Title**: UMOPS (2-way) -- A64 | **Class**: `mortlach2` | **XML ID**: `umops_za32_pp_zz`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Unsigned integer sum of outer products and subtract

**Description**:
This instruction works with a 32-bit element ZA tile.

This instruction multiplies the sub-matrix in the first source vector by the
sub-matrix in the second source vector.
The first source holds SVLS×2
sub-matrix of unsigned 16-bit integer values, and the second source holds
2×SVLS sub-matrix of unsigned 16-bit integer values.

Each source vector is independently predicated by a corresponding
governing predicate.
When a 16-bit source element is inactive, it is treated as having the value 0.

The resulting SVLS×SVLS widened 32-bit integer sum of outer products
is then destructively subtracted from the 32-bit integer
destination tile.
This is equivalent to performing a 2-way dot product and subtract from
each of the destination tile elements.

Each 32-bit container of the first source
vector holds 2 consecutive column elements of each row of a SVLS×2
sub-matrix, and each 32-bit container of the second source vector holds
2 consecutive row elements of each column of a 2×SVLS sub-matrix.

**Attributes**: Predicated; DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `SME2`
- **Assembly**: `UMOPS  <ZAda>.S, <Pn>/M, <Pm>/M, <Zn>.H, <Zm>.H`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  15  12   9   4  3  2  1  |
|--------------------------------------------|
| 1   01  0000 1   10  0   Zm  Pm  Pn  Zn  1   1   0   ZAda |
```

#### Decode (A64.sme.mortlach_32bit_int_prod.mortlach_i16i32_prod.umops_za32_pp_zz_16)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer a = UInt(Pn);
constant integer b = UInt(Pm);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(ZAda);
constant boolean unsigned = TRUE;
```

#### Execute (A64.sme.mortlach_32bit_int_prod.mortlach_i16i32_prod.umops_za32_pp_zz_16)

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
        for k = 0 to 1
            if (ActivePredicateElement(mask1, 2*row + k, esize DIV 2) &&
                  ActivePredicateElement(mask2, 2*col + k, esize DIV 2)) then
                prod = (Int(Elem[operand1, 2*row + k, esize DIV 2], unsigned) *
                        Int(Elem[operand2, 2*col + k, esize DIV 2], unsigned));
                sum = sum - prod;
        Elem[result, row*dim+col, esize] = sum;

ZAtile[da, esize, dim*dim*esize] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<ZAda>` | `register (128-bit)` | `ZAda` | Is the name of the ZA tile ZA0-ZA3, encoded in the "ZAda" field. |
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
- source: `umops_za32_pp_zz.xml`
</details>