## FCVTX
_ARM A64 Instruction_

**Title**: FCVTX -- A64 | **Class**: `sve2` | **XML ID**: `fcvtx_z_p_z`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME), `FEAT_SVE2p2 || FEAT_SME2p2` (FEAT_SVE2p2 || FEAT_SME2p2)

**Summary**: Double-precision down convert to single-precision, rounding to odd (predicated)

**Description**:
Convert active double-precision elements from the source
vector to single-precision, rounding to Odd, and place
the results in the even-numbered 32-bit elements of the
destination vector, while setting the odd-numbered elements to
zero. 
Inactive elements in the destination vector register remain unmodified or
are set to zero, depending on whether merging or zeroing
predication is selected.

Rounding to Odd (aka Von Neumann rounding) permits a two-step
conversion from double-precision to half-precision without
incurring intermediate rounding errors.

**Attributes**: Predicated

### Variant: `Double-precision to single-precision, merging`
- **Assembly**: `FCVTX  <Zd>.S, <Pg>/M, <Zn>.D`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  17  15  12   9   4  |
|-----------------------------------|
| 011 0010 1   00  0   010 10  101 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_unary.sve_fp_2op_p_zd_b_0.fcvtx_z_p_z_d2s)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer s_esize = 64;
constant integer d_esize = 32;
constant boolean merging = TRUE;
```

#### Execute (A64.sve.sve_fp_unary.sve_fp_2op_p_zd_b_0.fcvtx_z_p_z_d2s)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand = if AnyActiveElement(mask, esize) then Z[n, VL] else Zeros(VL);
bits(VL) result = if merging then Z[d, VL] else Zeros(VL);

for e = 0 to elements-1
    if ActivePredicateElement(mask, e, esize) then
        constant bits(esize) element = Elem[operand, e, esize];
        constant bits(d_esize) res = FPConvertSVE(element<s_esize-1:0>, FPCR, FPRounding_ODD,
                                                  d_esize);
        Elem[result, e, esize] = ZeroExtend(res, esize);

Z[d, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |

### Variant: `Double-precision to single-precision, zeroing`
- **Assembly**: `FCVTX  <Zd>.S, <Pg>/Z, <Zn>.D`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18  15 14  12   9   4  |
|-----------------------------------|
| 011 0010 0   00  011 010 1   10  Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_zeroing_unary.sve_fp_z2op_p_zd_b_0.fcvtx_z_p_z_d2sz)

```
if !IsFeatureImplemented(FEAT_SVE2p2) && !IsFeatureImplemented(FEAT_SME2p2) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer s_esize = 64;
constant integer d_esize = 32;
constant boolean merging = FALSE;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2p2) \|\| IsFeatureImplemented(FEAT_SME2p2)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |

### Operational Notes

The merging variant of this instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and the merging variant of this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX can be predicated or unpredicated.
          
          
            A predicated MOVPRFX must use the same governing predicate register as the merging variant this instruction.
          
          
            A predicated MOVPRFX must use the larger of the destination element size and first source element size in the preferred disassembly of the merging variant of this instruction.
          
          
            The MOVPRFX must specify the same destination register as the merging variant of this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of the merging variant of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fcvtx_z_p_z.xml`
</details>