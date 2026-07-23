## HISTSEG
_ARM A64 Instruction_

**Title**: HISTSEG -- A64 | **Class**: `sve2` | **XML ID**: `histseg_z_zz`

**Architecture**: `FEAT_SVE2` (ARMv9.0)

**Summary**: Count matching elements in vector segments

**Description**:
This instruction compares each 8-bit byte element of the first source vector with
all of the elements in the corresponding 128-bit
segment of the second source vector and places the
count of matching elements in the corresponding element
of the destination vector. This instruction is unpredicated.

This instruction is illegal when executed in Streaming SVE mode, unless FEAT_SME_FA64 is implemented and enabled.

**Attributes**: SM Policy: `SM_0_only`

### Variant: `SVE2`
- **Assembly**: `HISTSEG  <Zd>.B, <Zn>.B, <Zm>.B`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  12   9   4  |
|--------------------------------|
| 010 0010 1   size 1   Zm  101 000 Zn  Zd  |
```

#### Decode (A64.sve.sve_intx_histseg_lut.sve_intx_histseg.histseg_z_zz_)

```
if !IsFeatureImplemented(FEAT_SVE2) then EndOfDecode(Decode_UNDEF);
if size != '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8;
constant integer d = UInt(Zd);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
```

#### Execute (A64.sve.sve_intx_histseg_lut.sve_intx_histseg.histseg_z_zz_)

```
CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer segments = VL DIV 128;
constant integer eltspersegment = 128 DIV esize;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result;

for b = 0 to segments-1
    for s = 0 to eltspersegment-1
        integer count = 0;
        constant integer e = eltspersegment * b + s;
        constant bits(esize) element1 = Elem[operand1, e, esize];
        for i = 0 to eltspersegment-1
            constant integer e2 = eltspersegment * b + i;
            constant bits(esize) element2 = Elem[operand2, e2, esize];
            if element1 == element2 then
                count = count + 1;
        Elem[result, e, esize] = count<esize-1:0>;

Z[d, VL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2)` |
| 🚫 ENCODING_UNDEF | `size == '00'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `histseg_z_zz.xml`
</details>