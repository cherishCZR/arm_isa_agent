## ADDHA
_ARM A64 Instruction_

**Title**: ADDHA -- A64 | **Class**: `mortlach` | **XML ID**: `addha_za_pp_z`

**Architecture**: `FEAT_SME` (PROFILE_A), `FEAT_SME_I16I64` (ARMv9.2)

**Summary**: Add horizontally vector elements to ZA tile

**Description**:
This instruction adds each element of the source vector to the corresponding
active element of each horizontal slice of a ZA tile.
The tile elements are predicated by a pair of governing predicates.
An element of a horizontal slice is considered active if its
corresponding element in the second governing predicate is TRUE
and the element corresponding to its horizontal slice number
in the first governing predicate is TRUE.
Inactive elements in the destination tile remain unmodified.

ID_AA64SMFR0_EL1.I16I64 indicates whether the 64-bit integer variant is implemented.

**Attributes**: Predicated; DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `32-bit`
- **Assembly**: `ADDHA  <ZAda>.S, <Pn>/M, <Pm>/M, <Zn>.S`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23 22 21  18  16 15  12   9   4  3  2  1  |
|--------------------------------------------------|
| 1   10  0000 0   1   0   010 00  0   Pm  Pn  Zn  0   0   0   ZAda |
```

#### Decode (A64.sme.mortlach_hvadd.mortlach_addhv.addha_za_pp_z_32)

```
if !IsFeatureImplemented(FEAT_SME) then EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer a = UInt(Pn);
constant integer b = UInt(Pm);
constant integer n = UInt(Zn);
constant integer da = UInt(ZAda);
```

#### Execute (A64.sme.mortlach_hvadd.mortlach_addhv.addha_za_pp_z_32)

```
CheckStreamingSVEAndZAEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer dim = VL DIV esize;
constant bits(PL) mask1 = P[a, PL];
constant bits(PL) mask2 = P[b, PL];
constant bits(VL) operand_src = Z[n, VL];
constant bits(dim*dim*esize) operand_acc = ZAtile[da, esize, dim*dim*esize];
bits(dim*dim*esize) result;

for col = 0 to dim-1
    constant bits(esize) element = Elem[operand_src, col, esize];
    for row = 0 to dim-1
        bits(esize) res = Elem[operand_acc, row*dim+col, esize];
        if (ActivePredicateElement(mask1, row, esize) &&
              ActivePredicateElement(mask2, col, esize)) then
            res = res + element;
        Elem[result, row*dim+col, esize] = res;

ZAtile[da, esize, dim*dim*esize] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME)` |

### Variant: `64-bit`
- **Assembly**: `ADDHA  <ZAda>.D, <Pn>/M, <Pm>/M, <Zn>.D`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23 22 21  18  16 15  12   9   4  3  2  |
|-----------------------------------------------|
| 1   10  0000 0   1   1   010 00  0   Pm  Pn  Zn  0   0   ZAda |
```

#### Decode (A64.sme.mortlach_hvadd.mortlach_addhv.addha_za_pp_z_64)

```
if !IsFeatureImplemented(FEAT_SME_I16I64) then EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer a = UInt(Pn);
constant integer b = UInt(Pm);
constant integer n = UInt(Zn);
constant integer da = UInt(ZAda);
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
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |

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
- source: `addha_za_pp_z.xml`
</details>