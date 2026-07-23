## MOVA `[ALIAS]`
_ARM A64 Instruction_ (Alias of mova_mz2_za.xml)

**Title**: MOV (tile to vector, two registers) -- A64 | **Class**: `mortlach2` | **XML ID**: `mov_mova_mz2_za`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Move two ZA tile slices to two vector registers

**Description**:
This instruction operates on two consecutive horizontal or
vertical slices within a named ZA tile of the specified element size.

The consecutive slice numbers within the tile are selected starting from the
sum of the slice index register and immediate offset, modulo the number of
such elements in a vector.
The immediate offset is a multiple of 2 in the range 0 to the number
of elements in a 128-bit vector segment minus 2.

This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `8-bit`
- **Assembly**: `MOV  { <Zd1>.B-<Zd2>.B }, ZA0<HV>.B[<Ws>, <offs1>:<offs2>]`
- **Alias of**: `MOVA  { <Zd1>.B-<Zd2>.B }, ZA0<HV>.B[<Ws>, <offs1>:<offs2>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9   7   4   0 |
|--------------------------------------------------|
| 1   10  0000 0   00  000 1   1   0   V   Rs  000 00  off3 Zd  0   |
```

### Variant: `16-bit`
- **Assembly**: `MOV  { <Zd1>.H-<Zd2>.H }, <ZAn><HV>.H[<Ws>, <offs1>:<offs2>]`
- **Alias of**: `MOVA  { <Zd1>.H-<Zd2>.H }, <ZAn><HV>.H[<Ws>, <offs1>:<offs2>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9   7  6   4   0 |
|-----------------------------------------------------|
| 1   10  0000 0   01  000 1   1   0   V   Rs  000 00  ZAn off2 Zd  0   |
```

### Variant: `32-bit`
- **Assembly**: `MOV  { <Zd1>.S-<Zd2>.S }, <ZAn><HV>.S[<Ws>, <offs1>:<offs2>]`
- **Alias of**: `MOVA  { <Zd1>.S-<Zd2>.S }, <ZAn><HV>.S[<Ws>, <offs1>:<offs2>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9   7   5  4   0 |
|-----------------------------------------------------|
| 1   10  0000 0   10  000 1   1   0   V   Rs  000 00  ZAn o1  Zd  0   |
```

### Variant: `64-bit`
- **Assembly**: `MOV  { <Zd1>.D-<Zd2>.D }, <ZAn><HV>.D[<Ws>, <offs1>:<offs2>]`
- **Alias of**: `MOVA  { <Zd1>.D-<Zd2>.D }, <ZAn><HV>.D[<Ws>, <offs1>:<offs2>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9   7   4   0 |
|--------------------------------------------------|
| 1   10  0000 0   11  000 1   1   0   V   Rs  000 00  ZAn Zd  0   |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd1>` | `register (128-bit)` | `Zd` | Is the name of the first scalable vector register of the destination multi-vector group, encoded as "Zd" times 2. |
| `<Zd2>` | `register (128-bit)` | `Zd` | Is the name of the second scalable vector register of the destination multi-vector group, encoded as "Zd" times 2 plus 1. |
| `<HV>` | `register (16-bit)` | `V` | Is the horizontal or vertical slice indicator, |
| `<Ws>` | `register (32-bit)` | `Rs` | Is the 32-bit name of the slice index register W12-W15, encoded in the "Rs" field. |
| `<offs1>` | `unknown` | `off3` | For the "8-bit" variant: is the first slice index offset, encoded as "off3" field times 2. |
| `<offs1>` | `unknown` | `off2` | For the "16-bit" variant: is the first slice index offset, encoded as "off2" field times 2. |
| `<offs1>` | `unknown` | `o1` | For the "32-bit" variant: is the first slice index offset, encoded as "o1" field times 2. |
| `<offs1>` | `unknown` | `` | For the "64-bit" variant: is the first slice index offset, with implicit value 0. |
| `<offs2>` | `unknown` | `off3` | For the "8-bit" variant: is the second slice index offset, encoded as "off3" field times 2 plus 1. |
| `<offs2>` | `unknown` | `off2` | For the "16-bit" variant: is the second slice index offset, encoded as "off2" field times 2 plus 1. |
| `<offs2>` | `unknown` | `o1` | For the "32-bit" variant: is the second slice index offset, encoded as "o1" field times 2 plus 1. |
| `<offs2>` | `unknown` | `` | For the "64-bit" variant: is the second slice index offset, with implicit value 1. |
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
- source: `mov_mova_mz2_za.xml`
</details>