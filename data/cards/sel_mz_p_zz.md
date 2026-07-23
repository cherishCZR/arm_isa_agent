## SEL
_ARM A64 Instruction_

**Title**: SEL -- A64 | **Class**: `mortlach2` | **XML ID**: `sel_mz_p_zz`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Multi-vector conditionally select elements from two vectors

**Description**:
This instruction selects consecutive elements from the two or four first source vectors
where predicate elements are true, and places them in the corresponding elements of the
two or four destination vectors. The corresponding elements from the two or four second
source vectors are placed in the remaining elements of the destination vectors.

**Attributes**: Predicated; DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `Two registers`
- **Assembly**: `SEL  { <Zd1>.<T>-<Zd2>.<T> }, <PNg>, { <Zn1>.<T>-<Zn2>.<T> }, { <Zm1>.<T>-<Zm2>.<T> }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  16 15  12   9   5  4   0 |
|--------------------------------------------|
| 1   10  0000 1   size 1   Zm  0   100 PNg Zn  0   Zd  0   |
```

#### Decode (A64.sme.mortlach_multi_sve_1.mortlach_multi2_select_int.sel_mz_p_zz_2)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn:'0');
constant integer m = UInt(Zm:'0');
constant integer d = UInt(Zd:'0');
constant integer g = UInt('1':PNg);
constant integer nreg = 2;
```

#### Execute (A64.sme.mortlach_multi_sve_1.mortlach_multi2_select_int.sel_mz_p_zz_2)

```
CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
array [0..3] of bits(VL) results;
constant bits(PL) pred = P[g, PL];
constant bits(PL * nreg) mask = CounterToPredicate(pred<15:0>, PL * nreg);

for r = 0 to nreg-1
    constant bits(VL) operand1 = Z[n+r, VL];
    constant bits(VL) operand2 = Z[m+r, VL];
    for e = 0 to elements-1
        if ActivePredicateElement(mask, r * elements + e, esize) then
            Elem[results[r], e, esize] = Elem[operand1, e, esize];
        else
            Elem[results[r], e, esize] = Elem[operand2, e, esize];

for r = 0 to nreg-1
    Z[d+r, VL] = results[r];
```

### Variant: `Four registers`
- **Assembly**: `SEL  { <Zd1>.<T>-<Zd4>.<T> }, <PNg>, { <Zn1>.<T>-<Zn4>.<T> }, { <Zm1>.<T>-<Zm4>.<T> }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  17  15  12   9   6   4   1  |
|--------------------------------------------|
| 1   10  0000 1   size 1   Zm  01  100 PNg Zn  00  Zd  00  |
```

#### Decode (A64.sme.mortlach_multi_sve_1.mortlach_multi4_select_int.sel_mz_p_zz_4)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn:'00');
constant integer m = UInt(Zm:'00');
constant integer d = UInt(Zd:'00');
constant integer g = UInt('1':PNg);
constant integer nreg = 4;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd1>` | `register (128-bit)` | `Zd` | For the "Two registers" variant: is the name of the first scalable vector register of the destination multi-vector group, encoded as "Zd" times 2. |
| `<Zd1>` | `register (128-bit)` | `Zd` | For the "Four registers" variant: is the name of the first scalable vector register of the destination multi-vector group, encoded as "Zd" times 4. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Zd2>` | `register (128-bit)` | `Zd` | Is the name of the second scalable vector register of the destination multi-vector group, encoded as "Zd" times 2 plus 1. |
| `<PNg>` | `unknown` | `PNg` | Is the name of the governing scalable predicate register PN8-PN15, with predicate-as-counter encoding, encoded in the "PNg" field. |
| `<Zn1>` | `register (128-bit)` | `Zn` | For the "Two registers" variant: is the name of the first scalable vector register of the first source multi-vector group, encoded as "Zn" times 2. |
| `<Zn1>` | `register (128-bit)` | `Zn` | For the "Four registers" variant: is the name of the first scalable vector register of the first source multi-vector group, encoded as "Zn" times 4. |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the first source multi-vector group, encoded as "Zn" times 2 plus 1. |
| `<Zm1>` | `register (128-bit)` | `Zm` | For the "Two registers" variant: is the name of the first scalable vector register of the second source multi-vector group, encoded as "Zm" times 2. |
| `<Zm1>` | `register (128-bit)` | `Zm` | For the "Four registers" variant: is the name of the first scalable vector register of the second source multi-vector group, encoded as "Zm" times 4. |
| `<Zm2>` | `register (128-bit)` | `Zm` | Is the name of the second scalable vector register of the second source multi-vector group, encoded as "Zm" times 2 plus 1. |
| `<Zd4>` | `register (128-bit)` | `Zd` | Is the name of the fourth scalable vector register of the destination multi-vector group, encoded as "Zd" times 4 plus 3. |
| `<Zn4>` | `register (128-bit)` | `Zn` | Is the name of the fourth scalable vector register of the first source multi-vector group, encoded as "Zn" times 4 plus 3. |
| `<Zm4>` | `register (128-bit)` | `Zm` | Is the name of the fourth scalable vector register of the second source multi-vector group, encoded as "Zm" times 4 plus 3. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2)` |

### Operational Notes

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its operand registers when its governing predicate register contains the same value for each execution.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its operand registers when its governing predicate register contains the same value for each execution.
                
                
                  The values of the NZCV flags.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sel_mz_p_zz.xml`
</details>