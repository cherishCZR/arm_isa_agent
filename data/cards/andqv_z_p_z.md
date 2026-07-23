## ANDQV
_ARM A64 Instruction_

**Title**: ANDQV -- A64 | **Class**: `sve2` | **XML ID**: `andqv_z_p_z`

**Architecture**: `FEAT_SVE2p1 || FEAT_SME2p1` (FEAT_SVE2p1 || FEAT_SME2p1)

**Summary**: Bitwise AND reduction of quadword vector segments

**Description**:
Bitwise AND of the same element numbers from each 128-bit source vector segment,
placing each result into the corresponding element number of the
128-bit SIMD&FP destination register.
Inactive elements in the source vector are treated as all ones.

**Attributes**: Predicated; DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE2`
- **Assembly**: `ANDQV  <Vd>.<T>, <Pg>, <Zn>.<Tb>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  17  15  12   9   4  |
|-----------------------------------|
| 000 0010 0   size 0   111 10  001 Pg  Zn  Vd  |
```

#### Decode (A64.sve.sve_int_pred_red.sve_int_reduce_2q.andqv_z_p_z_)

```
if !IsFeatureImplemented(FEAT_SVE2p1) && !IsFeatureImplemented(FEAT_SME2p1) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Vd);
```

#### Execute (A64.sve.sve_int_pred_red.sve_int_reduce_2q.andqv_z_p_z_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer segments = VL DIV 128;
constant integer elempersegment = 128 DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand = if AnyActiveElement(mask, esize) then Z[n, VL] else Zeros(VL);
bits(128) result = Zeros(128);
bits(128) stmp = Zeros(128);

bits(esize) dtmp;

for e = 0 to elempersegment-1
    dtmp = Ones(esize);
    for s = 0 to segments-1
        if ActivePredicateElement(mask, s * elempersegment + e, esize) then
            stmp = Elem[operand, s, 128];
            dtmp = dtmp AND Elem[stmp, e, esize];
    Elem[result, e, esize] = dtmp<esize-1:0>;

V[d, 128] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2p1) \|\| IsFeatureImplemented(FEAT_SME2p1)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Vd` | Is the name of the destination SIMD&FP register, encoded in the "Vd" field. |
| `<T>` | `unknown` | `size` | Is an arrangement specifier, |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |
| `<Tb>` | `unknown` | `size` | Is the size specifier, |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | 16B |
| 01 | 8H |
| 10 | 4S |
| 11 | 2D |

**<Tb> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

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
- source: `andqv_z_p_z.xml`
</details>