## MOVA `[ALIAS]`
_ARM A64 Instruction_ (Alias of mova_z_p_rza.xml)

**Title**: MOV (tile to vector, single) -- A64 | **Class**: `mortlach` | **XML ID**: `mov_mova_z_p_rza`

**Architecture**: `FEAT_SME` (PROFILE_A)

**Summary**: Move ZA tile slice to vector register

**Description**:
This instruction operates on individual horizontal or vertical slices
within a named ZA tile of the specified element size.
The slice number within the tile is selected by
the sum of the slice index register and immediate offset,
modulo the number of such elements in a vector.
The immediate offset is in the range 0 to the number of elements in a 128-bit vector segment minus 1.
Inactive elements in the destination vector remain unmodified.

**Attributes**: Predicated; DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `8-bit`
- **Assembly**: `MOV  <Zd>.B, <Pg>/M, ZA0<HV>.B[<Ws>, <offs>]`
- **Alias of**: `MOVA  <Zd>.B, <Pg>/M, ZA0<HV>.B[<Ws>, <offs>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9  8   4  |
|-----------------------------------------------|
| 1   10  0000 0   00  000 0   1   0   V   Rs  Pg  0   off4 Zd  |
```

### Variant: `16-bit`
- **Assembly**: `MOV  <Zd>.H, <Pg>/M, <ZAn><HV>.H[<Ws>, <offs>]`
- **Alias of**: `MOVA  <Zd>.H, <Pg>/M, <ZAn><HV>.H[<Ws>, <offs>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9  8  7   4  |
|--------------------------------------------------|
| 1   10  0000 0   01  000 0   1   0   V   Rs  Pg  0   ZAn off3 Zd  |
```

### Variant: `32-bit`
- **Assembly**: `MOV  <Zd>.S, <Pg>/M, <ZAn><HV>.S[<Ws>, <offs>]`
- **Alias of**: `MOVA  <Zd>.S, <Pg>/M, <ZAn><HV>.S[<Ws>, <offs>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9  8   6   4  |
|--------------------------------------------------|
| 1   10  0000 0   10  000 0   1   0   V   Rs  Pg  0   ZAn off2 Zd  |
```

### Variant: `64-bit`
- **Assembly**: `MOV  <Zd>.D, <Pg>/M, <ZAn><HV>.D[<Ws>, <offs>]`
- **Alias of**: `MOVA  <Zd>.D, <Pg>/M, <ZAn><HV>.D[<Ws>, <offs>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9  8   5  4  |
|--------------------------------------------------|
| 1   10  0000 0   11  000 0   1   0   V   Rs  Pg  0   ZAn o1  Zd  |
```

### Variant: `128-bit`
- **Assembly**: `MOV  <Zd>.Q, <Pg>/M, <ZAn><HV>.Q[<Ws>, <offs>]`
- **Alias of**: `MOVA  <Zd>.Q, <Pg>/M, <ZAn><HV>.Q[<Ws>, <offs>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9  8   4  |
|-----------------------------------------------|
| 1   10  0000 0   11  000 0   1   1   V   Rs  Pg  0   ZAn Zd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<HV>` | `register (16-bit)` | `V` | Is the horizontal or vertical slice indicator, |
| `<Ws>` | `register (32-bit)` | `Rs` | Is the 32-bit name of the slice index register W12-W15, encoded in the "Rs" field. |
| `<offs>` | `unknown` | `off4` | For the "8-bit" variant: is the slice index offset, in the range 0 to 15, encoded in the "off4" field. |
| `<offs>` | `unknown` | `off3` | For the "16-bit" variant: is the slice index offset, in the range 0 to 7, encoded in the "off3" field. |
| `<offs>` | `unknown` | `off2` | For the "32-bit" variant: is the slice index offset, in the range 0 to 3, encoded in the "off2" field. |
| `<offs>` | `unknown` | `o1` | For the "64-bit" variant: is the slice index offset, in the range 0 to 1, encoded in the "o1" field. |
| `<offs>` | `unknown` | `` | For the "128-bit" variant: is the slice index offset, with implicit value 0. |
| `<ZAn>` | `register (128-bit)` | `ZAn` | For the "16-bit" variant: is the name of the ZA tile ZA0-ZA1 to be accessed, encoded in the "ZAn" field. |
| `<ZAn>` | `register (128-bit)` | `ZAn` | For the "32-bit" variant: is the name of the ZA tile ZA0-ZA3 to be accessed, encoded in the "ZAn" field. |
| `<ZAn>` | `register (128-bit)` | `ZAn` | For the "64-bit" variant: is the name of the ZA tile ZA0-ZA7 to be accessed, encoded in the "ZAn" field. |
| `<ZAn>` | `register (128-bit)` | `ZAn` | For the "128-bit" variant: is the name of the ZA tile ZA0-ZA15 to be accessed, encoded in the "ZAn" field. |

**<HV> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | H |
| 1 | V |

### Operational Notes

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its operand registers when its governing predicate register contains the same value for each execution.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its operand registers when its governing predicate register contains the same value for each execution.
                
                
                  The values of the NZCV flags.

---
<details><summary>Metadata</summary>

- alias_mnemonic: `MOV`
- isa: `A64`
- source: `mov_mova_z_p_rza.xml`
</details>