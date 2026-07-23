## PMULLT
_ARM A64 Instruction_

**Title**: PMULLT -- A64 | **Class**: `sve2` | **XML ID**: `pmullt_z_zz`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME), `FEAT_SVE_PMULL128` (ARMv9.0)

**Summary**: Polynomial multiply long (top)

**Description**:
Polynomial multiply over [0, 1] the corresponding odd-numbered elements of the first and
second source vectors, and place the results in the overlapping double-width
elements of the destination vector.
This instruction is unpredicated.

ID_AA64ZFR0_EL1.AES indicates whether the 128-bit element variant
is implemented.
The 128-bit element variant is legal when executed in Streaming SVE mode if one of the following is true:

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `16-bit or 64-bit elements`
- **Assembly**: `PMULLT  <Zd>.<T>, <Zn>.<Tb>, <Zm>.<Tb>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15 14  12 11 10  9   4  |
|-----------------------------------------|
| 010 0010 1   ?   0   Zm  0   11  0   1   1   Zn  Zd  |
```

#### Decode (A64.sve.sve_intx_cons_widening.sve_intx_cons_mul_long.pmullt_z_zz_)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size<0> == '0' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_intx_cons_widening.sve_intx_cons_mul_long.pmullt_z_zz_)

```
if esize == 128 then
    if IsFeatureImplemented(FEAT_SSVE_AES) then
        CheckSVEEnabled();
    else
        CheckNonStreamingSVEEnabled();
else
    CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result;

for e = 0 to elements-1
    constant bits(esize DIV 2) element1 = Elem[operand1, 2*e + 1, esize DIV 2];
    constant bits(esize DIV 2) element2 = Elem[operand2, 2*e + 1, esize DIV 2];
    Elem[result, e, esize] = PolynomialMult(element1, element2);

Z[d, VL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |
| 🚫 ENCODING_UNDEF | `size<0> != '0'` |

### Variant: `128-bit element`
- **Assembly**: `PMULLT  <Zd>.Q, <Zn>.D, <Zm>.D`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15 14  12 11 10  9   4  |
|-----------------------------------------|
| 010 0010 1   00  0   Zm  0   11  0   1   1   Zn  Zd  |
```

#### Decode (A64.sve.sve_intx_cons_widening.sve_intx_cons_mul_long.pmullt_z_zz_q)

```
if !IsFeatureImplemented(FEAT_SVE_PMULL128) then EndOfDecode(Decode_UNDEF);
constant integer esize = 128;
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE_PMULL128)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Tb>` | `unknown` | `size` | Is the size specifier, |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 01 | H |
| 1x | D |

**<Tb> Value Table**:

| bitfield | symbol |
|---|---|
| 01 | B |
| 1x | S |

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
- source: `pmullt_z_zz.xml`
</details>