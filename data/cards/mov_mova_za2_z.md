## MOVA `[ALIAS]`
_ARM A64 Instruction_ (Alias of mova_za2_z.xml)

**Title**: MOV (vector to tile, two registers) -- A64 | **Class**: `mortlach2` | **XML ID**: `mov_mova_za2_z`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Move two vector registers to two ZA tile slices

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
- **Assembly**: `MOV  ZA0<HV>.B[<Ws>, <offs1>:<offs2>], { <Zn1>.B-<Zn2>.B }`
- **Alias of**: `MOVA  ZA0<HV>.B[<Ws>, <offs1>:<offs2>], { <Zn1>.B-<Zn2>.B }`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9   5  4  3  2  |
|-----------------------------------------------------|
| 1   10  0000 0   00  000 1   0   0   V   Rs  000 Zn  0   0   0   off3 |
```

### Variant: `16-bit`
- **Assembly**: `MOV  <ZAd><HV>.H[<Ws>, <offs1>:<offs2>], { <Zn1>.H-<Zn2>.H }`
- **Alias of**: `MOVA  <ZAd><HV>.H[<Ws>, <offs1>:<offs2>], { <Zn1>.H-<Zn2>.H }`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9   5  4  3  2  1  |
|--------------------------------------------------------|
| 1   10  0000 0   01  000 1   0   0   V   Rs  000 Zn  0   0   0   ZAd off2 |
```

### Variant: `32-bit`
- **Assembly**: `MOV  <ZAd><HV>.S[<Ws>, <offs1>:<offs2>], { <Zn1>.S-<Zn2>.S }`
- **Alias of**: `MOVA  <ZAd><HV>.S[<Ws>, <offs1>:<offs2>], { <Zn1>.S-<Zn2>.S }`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9   5  4  3  2   0 |
|--------------------------------------------------------|
| 1   10  0000 0   10  000 1   0   0   V   Rs  000 Zn  0   0   0   ZAd o1  |
```

### Variant: `64-bit`
- **Assembly**: `MOV  <ZAd><HV>.D[<Ws>, <offs1>:<offs2>], { <Zn1>.D-<Zn2>.D }`
- **Alias of**: `MOVA  <ZAd><HV>.D[<Ws>, <offs1>:<offs2>], { <Zn1>.D-<Zn2>.D }`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9   5  4  3  2  |
|-----------------------------------------------------|
| 1   10  0000 0   11  000 1   0   0   V   Rs  000 Zn  0   0   0   ZAd |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
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
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first scalable vector register of the source multi-vector group, encoded as "Zn" times 2. |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the source multi-vector group, encoded as "Zn" times 2 plus 1. |
| `<ZAd>` | `register (128-bit)` | `ZAd` | For the "16-bit" variant: is the name of the ZA tile ZA0-ZA1 to be accessed, encoded in the "ZAd" field. |
| `<ZAd>` | `register (128-bit)` | `ZAd` | For the "32-bit" variant: is the name of the ZA tile ZA0-ZA3 to be accessed, encoded in the "ZAd" field. |
| `<ZAd>` | `register (128-bit)` | `ZAd` | For the "64-bit" variant: is the name of the ZA tile ZA0-ZA7 to be accessed, encoded in the "ZAd" field. |

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
- source: `mov_mova_za2_z.xml`
</details>