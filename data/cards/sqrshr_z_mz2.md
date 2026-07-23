## SQRSHR
_ARM A64 Instruction_

**Title**: SQRSHR (two registers) -- A64 | **Class**: `mortlach2` | **XML ID**: `sqrshr_z_mz2`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Multi-vector signed saturating rounding shift right narrow by immediate

**Description**:
This instruction shifts right by an immediate value the signed integer value in each element of the
two source vectors, and places the 
 rounded results in the half-width destination
elements. Each result element is saturated to the half-width
N-bit element's signed integer range -2(N-1)
to (2(N-1))-1. The immediate shift amount is an unsigned value in the
range 1 to 16.

This instruction is unpredicated.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `SME2`
- **Assembly**: `SQRSHR  <Zd>.H, { <Zn1>.S-<Zn2>.S }, #<const>`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20 19  15  12   9   5  4  |
|-----------------------------------------|
| 1   10  0000 1   11  1   0   imm4 110 101 Zn  0   Zd  |
```

#### Decode (A64.sme.mortlach_multi_sve_3.mortlach_multi2_qrshr.sqrshr_z_mz2_)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer esize = 16;
constant integer n = UInt(Zn:'0');
constant integer d = UInt(Zd);
constant integer shift = esize - UInt(imm4);
```

#### Execute (A64.sme.mortlach_multi_sve_3.mortlach_multi2_qrshr.sqrshr_z_mz2_)

```
CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV (2 * esize);
bits(VL) result;

for r = 0 to 1
    constant bits(VL) operand = Z[n+r, VL];
    for e = 0 to elements-1
        constant bits(2 * esize) element = Elem[operand, e, 2 * esize];
        constant integer res = (SInt(element) + (1 << (shift-1))) >> shift;
        Elem[result, r*elements + e, esize] = SignedSat(res, esize);

Z[d, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first scalable vector register of the source multi-vector group, encoded as "Zn" times 2. |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the source multi-vector group, encoded as "Zn" times 2 plus 1. |
| `<const>` | `unknown` | `imm4` | Is the immediate shift amount, in the range 1 to 16, encoded in the "imm4" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sqrshr_z_mz2.xml`
</details>