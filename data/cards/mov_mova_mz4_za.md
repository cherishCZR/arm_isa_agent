## MOVA `[ALIAS]`
_ARM A64 Instruction_ (Alias of mova_mz4_za.xml)

**Title**: MOV (tile to vector, four registers) -- A64 | **Class**: `mortlach2` | **XML ID**: `mov_mova_mz4_za`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Move four ZA tile slices to four vector registers

**Description**:
This instruction operates on four consecutive horizontal or
vertical slices within a named ZA tile of the specified element size.

The consecutive slice numbers within the tile are selected starting from the
sum of the slice index register and immediate offset, modulo the number of
such elements in a vector.
The immediate offset is a multiple of 4 in the range 0 to the number
of elements in a 128-bit vector segment minus 4.

This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `8-bit`
- **Assembly**: `MOV  { <Zd1>.B-<Zd4>.B }, ZA0<HV>.B[<Ws>, <offs1>:<offs4>]`
- **Alias of**: `MOVA  { <Zd1>.B-<Zd4>.B }, ZA0<HV>.B[<Ws>, <offs1>:<offs4>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9   7  6   4   1  |
|-----------------------------------------------------|
| 1   10  0000 0   00  000 1   1   0   V   Rs  001 00  0   off2 Zd  00  |
```

### Variant: `16-bit`
- **Assembly**: `MOV  { <Zd1>.H-<Zd4>.H }, <ZAn><HV>.H[<Ws>, <offs1>:<offs4>]`
- **Alias of**: `MOVA  { <Zd1>.H-<Zd4>.H }, <ZAn><HV>.H[<Ws>, <offs1>:<offs4>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9   7  6  5  4   1  |
|--------------------------------------------------------|
| 1   10  0000 0   01  000 1   1   0   V   Rs  001 00  0   ZAn o1  Zd  00  |
```

### Variant: `32-bit`
- **Assembly**: `MOV  { <Zd1>.S-<Zd4>.S }, <ZAn><HV>.S[<Ws>, <offs1>:<offs4>]`
- **Alias of**: `MOVA  { <Zd1>.S-<Zd4>.S }, <ZAn><HV>.S[<Ws>, <offs1>:<offs4>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9   7  6   4   1  |
|-----------------------------------------------------|
| 1   10  0000 0   10  000 1   1   0   V   Rs  001 00  0   ZAn Zd  00  |
```

### Variant: `64-bit`
- **Assembly**: `MOV  { <Zd1>.D-<Zd4>.D }, <ZAn><HV>.D[<Ws>, <offs1>:<offs4>]`
- **Alias of**: `MOVA  { <Zd1>.D-<Zd4>.D }, <ZAn><HV>.D[<Ws>, <offs1>:<offs4>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9   7   4   1  |
|--------------------------------------------------|
| 1   10  0000 0   11  000 1   1   0   V   Rs  001 00  ZAn Zd  00  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd1>` | `register (128-bit)` | `Zd` | Is the name of the first scalable vector register of the destination multi-vector group, encoded as "Zd" times 4. |
| `<Zd4>` | `register (128-bit)` | `Zd` | Is the name of the fourth scalable vector register of the destination multi-vector group, encoded as "Zd" times 4 plus 3. |
| `<HV>` | `register (16-bit)` | `V` | Is the horizontal or vertical slice indicator, |
| `<Ws>` | `register (32-bit)` | `Rs` | Is the 32-bit name of the slice index register W12-W15, encoded in the "Rs" field. |
| `<offs1>` | `unknown` | `off2` | For the "8-bit" variant: is the first slice index offset, encoded as "off2" field times 4. |
| `<offs1>` | `unknown` | `o1` | For the "16-bit" variant: is the first slice index offset, encoded as "o1" field times 4. |
| `<offs1>` | `unknown` | `` | For the "32-bit" and "64-bit" variants: is the first slice index offset, with implicit value 0. |
| `<offs4>` | `unknown` | `off2` | For the "8-bit" variant: is the fourth slice index offset, encoded as "off2" field times 4 plus 3. |
| `<offs4>` | `unknown` | `o1` | For the "16-bit" variant: is the fourth slice index offset, encoded as "o1" field times 4 plus 3. |
| `<offs4>` | `unknown` | `` | For the "32-bit" and "64-bit" variants: is the fourth slice index offset, with implicit value 3. |
| `<ZAn>` | `register (128-bit)` | `ZAn` | For the "16-bit" variant: is the name of the ZA tile ZA0-ZA1 to be accessed, encoded in the "ZAn" field. |
| `<ZAn>` | `register (128-bit)` | `ZAn` | For the "32-bit" variant: is the name of the ZA tile ZA0-ZA3 to be accessed, encoded in the "ZAn" field. |
| `<ZAn>` | `register (128-bit)` | `ZAn` | For the "64-bit" variant: is the name of the ZA tile ZA0-ZA7 to be accessed, encoded in the "ZAn" field. |

**<HV> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | H |
| 1 | V |

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

- alias_mnemonic: `MOV`
- isa: `A64`
- source: `mov_mova_mz4_za.xml`
</details>