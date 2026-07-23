## PTRUE
_ARM A64 Instruction_

**Title**: PTRUE (predicate as counter) -- A64 | **Class**: `sve2` | **XML ID**: `ptrue_pn_i`

**Architecture**: `FEAT_SME2 || FEAT_SVE2p1` (FEAT_SME2 || FEAT_SVE2p1)

**Summary**: Initialise predicate-as-counter to all active

**Description**:
Set the destination predicate as all-active elements, using
the predicate-as-counter encoding.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_or_SVE2p1`

### Variant: `SVE2`
- **Assembly**: `PTRUE  <PNd>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  13  10   4  3  2  |
|--------------------------------------|
| 001 0010 1   size 1   00000 01  111 000000 1   0   PNd |
```

#### Decode (A64.sve.sve_while_pn.sve_int_pn_ptrue.ptrue_pn_i_)

```
if !IsFeatureImplemented(FEAT_SME2) && !IsFeatureImplemented(FEAT_SVE2p1) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer d = UInt('1':PNd);
```

#### Execute (A64.sve.sve_while_pn.sve_int_pn_ptrue.ptrue_pn_i_)

```
if IsFeatureImplemented(FEAT_SVE2p1) then CheckSVEEnabled(); else CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) result = EncodePredCount(esize, elements, elements, FALSE, PL);
P[d, PL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2) \|\| IsFeatureImplemented(FEAT_SVE2p1)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<PNd>` | `unknown` | `PNd` | Is the name of the destination scalable predicate register PN8-PN15, with predicate-as-counter encoding, encoded in the "PNd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |

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
- source: `ptrue_pn_i.xml`
</details>