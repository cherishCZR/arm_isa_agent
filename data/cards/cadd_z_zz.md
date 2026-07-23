## CADD
_ARM A64 Instruction_

**Title**: CADD -- A64 | **Class**: `sve2` | **XML ID**: `cadd_z_zz`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: Complex integer add with rotate

**Description**:
Add the real and imaginary components of the integral
complex numbers from the first source vector to the
complex numbers from the second source vector which have
first been rotated by 90 or 270 degrees in the direction
from the positive real axis towards the positive
imaginary axis, when considered in polar representation,
equivalent to multiplying the complex numbers in the
second source vector by ±j
beforehand. Destructively place the results in the
corresponding elements of the first source vector. This instruction is unpredicated.

Each complex number is represented in a vector register as an
even/odd pair of elements with the real part in the
even-numbered element and the imaginary part in the
odd-numbered element.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE2`
- **Assembly**: `CADD  <Zdn>.<T>, <Zdn>.<T>, <Zm>.<T>, <const>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  16 15  13  10  9   4  |
|--------------------------------------|
| 010 0010 1   size 0   0000 0   11  011 rot Zm  Zdn |
```

#### Decode (A64.sve.sve_intx_acc.sve_intx_cadd.cadd_z_zz_)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer m = UInt(Zm);
constant integer dn = UInt(Zdn);
constant boolean sub_i = (rot == '0');
constant boolean sub_r = (rot == '1');
```

#### Execute (A64.sve.sve_intx_acc.sve_intx_cadd.cadd_z_zz_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer pairs = VL DIV (2 * esize);
constant bits(VL) operand1 = Z[dn, VL];
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result;

for p = 0 to pairs-1
    integer acc_r  = SInt(Elem[operand1, 2 * p + 0, esize]);
    integer acc_i  = SInt(Elem[operand1, 2 * p + 1, esize]);
    constant integer elt2_r = SInt(Elem[operand2, 2 * p + 0, esize]);
    constant integer elt2_i = SInt(Elem[operand2, 2 * p + 1, esize]);
    if sub_i then
        acc_r = acc_r - elt2_i;
        acc_i = acc_i + elt2_r;
    if sub_r then
        acc_r = acc_r + elt2_i;
        acc_i = acc_i - elt2_r;

    Elem[result, 2 * p + 0, esize] = acc_r<esize-1:0>;
    Elem[result, 2 * p + 1, esize] = acc_i<esize-1:0>;

Z[dn, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zdn>` | `register (128-bit)` | `Zdn` | Is the name of the first source and destination scalable vector register, encoded in the "Zdn" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |
| `<const>` | `unknown` | `rot` | Is the const specifier, |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

**<const> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | #90 |
| 1 | #270 |

### Operational Notes

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.
                
              
            
          
        
        This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX must be unpredicated.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `cadd_z_zz.xml`
</details>