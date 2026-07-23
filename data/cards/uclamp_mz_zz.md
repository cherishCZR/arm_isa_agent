## UCLAMP
_ARM A64 Instruction_

**Title**: UCLAMP -- A64 | **Class**: `mortlach2` | **XML ID**: `uclamp_mz_zz`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Multi-vector unsigned clamp to minimum/maximum vector

**Description**:
This instruction clamps each unsigned element in the two or four destination vectors to between
the unsigned minimum value in the corresponding element of the first source vector and
the unsigned maximum value in the corresponding element of the second source vector and
destructively places the clamped results in the corresponding elements of the
two or four destination vectors.

This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `Two registers`
- **Assembly**: `UCLAMP  { <Zd1>.<T>-<Zd2>.<T> }, <Zn>.<T>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  15  12   9   4   0 |
|--------------------------------------|
| 1   10  0000 1   size 1   Zm  110 001 Zn  Zd  1   |
```

#### Decode (A64.sme.mortlach_multi_sve_3.mortlach_multi2_clamp_int.uclamp_mz_zz_2)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd:'0');
constant integer nreg = 2;
```

#### Execute (A64.sme.mortlach_multi_sve_3.mortlach_multi2_clamp_int.uclamp_mz_zz_2)

```
CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
array [0..3] of bits(VL) results;

for r = 0 to nreg-1
    constant bits(VL) operand1 = Z[n, VL];
    constant bits(VL) operand2 = Z[m, VL];
    constant bits(VL) operand3 = Z[d+r, VL];
    for e = 0 to elements-1
        constant integer element1 = UInt(Elem[operand1, e, esize]);
        constant integer element2 = UInt(Elem[operand2, e, esize]);
        constant integer element3 = UInt(Elem[operand3, e, esize]);
        constant integer res = Min(Max(element1, element3), element2);
        Elem[results[r], e, esize] = res<esize-1:0>;

for r = 0 to nreg-1
    Z[d+r, VL] = results[r];
```

### Variant: `Four registers`
- **Assembly**: `UCLAMP  { <Zd1>.<T>-<Zd4>.<T> }, <Zn>.<T>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  15  12   9   4   1  0 |
|-----------------------------------------|
| 1   10  0000 1   size 1   Zm  110 011 Zn  Zd  0   1   |
```

#### Decode (A64.sme.mortlach_multi_sve_3.mortlach_multi4_clamp_int.uclamp_mz_zz_4)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd:'00');
constant integer nreg = 4;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd1>` | `register (128-bit)` | `Zd` | For the "Two registers" variant: is the name of the first scalable vector register of the destination multi-vector group, encoded as "Zd" times 2. |
| `<Zd1>` | `register (128-bit)` | `Zd` | For the "Four registers" variant: is the name of the first scalable vector register of the destination multi-vector group, encoded as "Zd" times 4. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Zd2>` | `register (128-bit)` | `Zd` | Is the name of the second scalable vector register of the destination multi-vector group, encoded as "Zd" times 2 plus 1. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |
| `<Zd4>` | `register (128-bit)` | `Zd` | Is the name of the fourth scalable vector register of the destination multi-vector group, encoded as "Zd" times 4 plus 3. |

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
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `uclamp_mz_zz.xml`
</details>