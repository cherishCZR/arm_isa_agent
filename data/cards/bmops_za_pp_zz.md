## BMOPS
_ARM A64 Instruction_

**Title**: BMOPS -- A64 | **Class**: `mortlach2` | **XML ID**: `bmops_za_pp_zz`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Bitwise exclusive NOR population count outer product and subtract

**Description**:
This instruction works with 32-bit element ZA tile. This instruction
generates an outer product of the first source SVLS×1 vector
and the second source 1×SVLS vector. Each outer product
element is obtained as population count of the bitwise XNOR result
of the corresponding 32-bit elements of the first source vector and the
second source vector. Each source vector is independently predicated
by a corresponding governing predicate. When either source vector element
is inactive the corresponding destination tile element remains
unmodified. The resulting SVLS×SVLS product is then
destructively subtracted from the destination tile.

**Attributes**: Predicated; DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `SME2`
- **Assembly**: `BMOPS  <ZAda>.S, <Pn>/M, <Pm>/M, <Zn>.S, <Zm>.S`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  15  12   9   4  3   1  |
|-----------------------------------------|
| 1   00  0000 0   10  0   Zm  Pm  Pn  Zn  1   10  ZAda |
```

#### Decode (A64.sme.mortlach2_misc_prod.mortlach_bini32_prod.bmops_za_pp_zz_32)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer a = UInt(Pn);
constant integer b = UInt(Pm);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(ZAda);
```

#### Execute (A64.sme.mortlach2_misc_prod.mortlach_bini32_prod.bmops_za_pp_zz_32)

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

for row = 0 to dim-1
    constant bits(esize) element1 = Elem[operand1, row, esize];
    for col = 0 to dim-1
        constant bits(esize) element2 = Elem[operand2, col, esize];
        constant bits(esize) element3 = Elem[operand3, row*dim + col, esize];
        if (ActivePredicateElement(mask1, row, esize) &&
              ActivePredicateElement(mask2, col, esize)) then
            constant integer res = BitCount(NOT(element1 EOR element2));
            Elem[result, row*dim + col, esize] = element3 - res;
        else
            Elem[result, row*dim + col, esize] = element3;
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
- source: `bmops_za_pp_zz.xml`
</details>