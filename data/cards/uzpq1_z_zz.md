## UZPQ1
_ARM A64 Instruction_

**Title**: UZPQ1 -- A64 | **Class**: `sve2` | **XML ID**: `uzpq1_z_zz`

**Architecture**: `FEAT_SVE2p1 || FEAT_SME2p1` (FEAT_SVE2p1 || FEAT_SME2p1)

**Summary**: Concatenate even elements within each pair of quadword vector segments

**Description**:
Concatenate adjacent even-numbered elements from the corresponding
128-bit vector segments of the first and second source vectors and
place in elements of the corresponding destination vector segment.
This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE2`
- **Assembly**: `UZPQ1  <Zd>.<T>, <Zn>.<T>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  12  10  9   4  |
|-----------------------------------|
| 010 0010 0   size 0   Zm  111 01  0   Zn  Zd  |
```

#### Decode (A64.sve.sve_perm_quads_b.sve_int_perm_binquads.uzpq1_z_zz_)

```
if !IsFeatureImplemented(FEAT_SVE2p1) && !IsFeatureImplemented(FEAT_SME2p1) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
constant integer part = 0;
```

#### Execute (A64.sve.sve_perm_quads_b.sve_int_perm_binquads.uzpq1_z_zz_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer segments = VL DIV 128;
constant integer elements = 128 DIV esize;
constant integer pairs = elements DIV 2;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result;

for s = 0 to segments-1
    constant integer soff = s * elements;
    for p = 0 to pairs-1
        Elem[result, soff + p, esize] = Elem[operand1, soff + 2 * p + part, esize];

    for p = 0 to pairs-1
        Elem[result, soff + pairs + p, esize] = Elem[operand2, soff + 2 * p + part, esize];

Z[d, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2p1) \|\| IsFeatureImplemented(FEAT_SME2p1)` |

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
- source: `uzpq1_z_zz.xml`
</details>