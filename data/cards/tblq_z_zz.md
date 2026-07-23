## TBLQ
_ARM A64 Instruction_

**Title**: TBLQ -- A64 | **Class**: `sve2` | **XML ID**: `tblq_z_zz`

**Architecture**: `FEAT_SVE2p1 || FEAT_SME2p1` (FEAT_SVE2p1 || FEAT_SME2p1)

**Summary**: Programmable table lookup within each quadword vector segment (zeroing)

**Description**:
For each 128-bit destination vector segment,
reads each element of the corresponding second source (index) vector segment
and uses its value to select an indexed element from the corresponding
first source (table) vector segment. The indexed table element is placed
in the element of the destination vector that corresponds to the
index vector element. If an index value is greater than or equal to the
number of elements in a 128-bit vector segment
then it places zero in the corresponding destination vector element.
This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE2`
- **Assembly**: `TBLQ  <Zd>.<T>, { <Zn>.<T> }, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  12   9   4  |
|--------------------------------|
| 010 0010 0   size 0   Zm  111 110 Zn  Zd  |
```

#### Decode (A64.sve.sve_perm_quads_b.sve_int_perm_binquads.tblq_z_zz_)

```
if !IsFeatureImplemented(FEAT_SVE2p1) && !IsFeatureImplemented(FEAT_SME2p1) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_perm_quads_b.sve_int_perm_binquads.tblq_z_zz_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer segments = VL DIV 128;
constant integer elements = 128 DIV esize;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result;

for s = 0 to segments-1
    for e = 0 to elements-1
        constant integer idx = UInt(Elem[operand2, s * elements + e, esize]);
        if idx < elements then
            Elem[result, s * elements + e, esize] = Elem[operand1, s * elements + idx, esize];
        else
            Elem[result, s * elements + e, esize] = Zeros(esize);

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
- source: `tblq_z_zz.xml`
</details>