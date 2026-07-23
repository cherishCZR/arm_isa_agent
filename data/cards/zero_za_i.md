## ZERO
_ARM A64 Instruction_

**Title**: ZERO (tiles) -- A64 | **Class**: `mortlach` | **XML ID**: `zero_za_i`

**Architecture**: `FEAT_SME` (PROFILE_A)

**Summary**: Zero a list of 64-bit element ZA tiles

**Description**:
This instruction zeroes all bytes within each of the up to eight listed 64-bit element tiles
named ZA0.D to ZA7.D,
leaving the other 64-bit element tiles unmodified.

This instruction does not require the PE to be in Streaming SVE
mode, and it is expected that this instruction will not
experience a significant slowdown due to contention with other
PEs that are executing in Streaming SVE mode.

For programmer convenience an assembler must also accept the names
of 32-bit, 16-bit, and 8-bit element tiles which are converted
into the corresponding set of 64-bit element tiles.

In accordance with the architecturally defined mapping
between different element size tiles:

The preferred disassembly of this instruction uses the shortest list
of tile names that represent the encoded immediate mask.

For example:

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_0_or_1`

### Variant: `SME`
- **Assembly**: `ZERO  { {<mask>} }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  17   7  |
|--------------------|
| 1   10  0000 0000010 0000000000 imm8 |
```

#### Decode (A64.sme.mortlach_zero.mortlach_zero.zero_za_i_)

```
if !IsFeatureImplemented(FEAT_SME) then EndOfDecode(Decode_UNDEF);
constant bits(8) mask = imm8;
constant integer esize = 64;
```

#### Execute (A64.sme.mortlach_zero.mortlach_zero.zero_za_i_)

```
CheckSMEAndZAEnabled();
constant integer SVL = CurrentSVL;
constant integer dim = SVL DIV esize;
constant bits(dim*dim*esize) result = Zeros(dim*dim*esize);

if IsFeatureImplemented(FEAT_TME) && TSTATE.depth > 0 then
    FailTransaction(TMFailure_ERR, FALSE);

for i = 0 to 7
    if mask<i> == '1' then ZAtile[i, esize, dim*dim*esize] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<mask>` | `unknown` | `imm8` | Is the optional list of up to eight 64-bit element tile names separated by commas, encoded in the "imm8" field. |

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
- source: `zero_za_i.xml`
</details>