## SQRDMULH
_ARM A64 Instruction_

**Title**: SQRDMULH (vectors) -- A64 | **Class**: `sve2` | **XML ID**: `sqrdmulh_z_zz`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: Signed saturating rounding doubling multiply high (unpredicated)

**Description**:
Multiply then double the corresponding signed elements of the first and second
source vectors, and place the most significant rounded half
of the result in the corresponding elements of the destination vector.
Each result element is saturated to the
 N-bit element's
signed integer range -2(N-1)  to (2(N-1))-1. This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE2`
- **Assembly**: `SQRDMULH  <Zd>.<T>, <Zn>.<T>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  12  10  9   4  |
|-----------------------------------|
| 000 0010 0   size 1   Zm  011 10  1   Zn  Zd  |
```

#### Decode (A64.sve.sve_int_unpred_arit_b.sve_int_sqdmulh.sqrdmulh_z_zz_)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_int_unpred_arit_b.sve_int_sqdmulh.sqrdmulh_z_zz_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result;

for e = 0 to elements-1
    constant integer element1 = SInt(Elem[operand1, e, esize]);
    constant integer element2 = SInt(Elem[operand2, e, esize]);
    constant integer res = 2 * element1 * element2;
    Elem[result, e, esize] = SignedSat((res + (1 << (esize - 1))) >> esize, esize);

Z[d, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

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
- source: `sqrdmulh_z_zz.xml`
</details>