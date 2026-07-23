## CBcc_regs
_ARM A64 Instruction_

**Title**: CB<cc> (register) -- A64 | **Class**: `general` | **XML ID**: `CBcc_regs`

**Architecture**: `FEAT_CMPBR` (ARMv9.6)

**Summary**: Compare registers and branch

**Description**:
This instruction compares the values in two registers, and conditionally
branches to a label at a PC-relative offset if the condition is true.
It provides a hint that this is not a subroutine call or return.
This instruction does not affect the condition flags.

### Variant: `Branch (CBGT_32_regs)` (32-bit greater than)
- **Condition**: `sf == 0 && cc == 000`
- **Assembly**: `CBGT  <Wt>, <Wm>, <label>`
- **Fixed bits**: `sf`=`0`, `cc`=`000`
- **Bit Pattern**: `?????????????????????000???????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30  23  20  15  13   4  |
|-----------------------|
| sf  1110100 cc  Rm  00  imm9 Rt  |
```

#### Decode (A64.control.compbranch_regs.CBGT_32_regs)

```
if !IsFeatureImplemented(FEAT_CMPBR) then EndOfDecode(Decode_UNDEF);
constant integer datasize = 32 << UInt(sf);
constant integer t = UInt(Rt);
constant integer m = UInt(Rm);
constant bits(64) offset = SignExtend(imm9:'00', 64);
CmpOp op;
boolean unsigned;

case cc of
    when '000' op = Cmp_GT; unsigned = FALSE;
    when '001' op = Cmp_GE; unsigned = FALSE;
    when '010' op = Cmp_GT; unsigned = TRUE;
    when '011' op = Cmp_GE; unsigned = TRUE;
    when '110' op = Cmp_EQ; unsigned = TRUE;
    when '111' op = Cmp_NE; unsigned = TRUE;
    otherwise EndOfDecode(Decode_UNDEF);
```

#### Execute (A64.control.compbranch_regs.CBGT_32_regs)

```
constant bits(datasize) operand1 = X[t, datasize];
constant bits(datasize) operand2 = X[m, datasize];
constant boolean branch_conditional = TRUE;

boolean cond;
constant integer value1 = Int(operand1, unsigned);
constant integer value2 = Int(operand2, unsigned);
case op of
    when Cmp_EQ cond = value1 == value2;
    when Cmp_NE cond = value1 != value2;
    when Cmp_GE cond = value1 >= value2;
    when Cmp_LT cond = value1 <  value2;
    when Cmp_GT cond = value1 >  value2;
    when Cmp_LE cond = value1 <= value2;

if cond then
    BranchTo(PC64 + offset, BranchType_DIR, branch_conditional);
else
    BranchNotTaken(BranchType_DIR, branch_conditional);
```

#### Constraints
_1× ↩ DECODE_FALLBACK / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_CMPBR)` |
| ↩ DECODE_FALLBACK | `matching encodings` |

### Variant: `Branch (CBGE_32_regs)` (32-bit greater than or equal)
- **Condition**: `sf == 0 && cc == 001`
- **Assembly**: `CBGE  <Wt>, <Wm>, <label>`
- **Fixed bits**: `sf`=`0`, `cc`=`001`
- **Bit Pattern**: `?????????????????????100???????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30  23  20  15  13   4  |
|-----------------------|
| sf  1110100 cc  Rm  00  imm9 Rt  |
```

### Variant: `Branch (CBHI_32_regs)` (32-bit higher)
- **Condition**: `sf == 0 && cc == 010`
- **Assembly**: `CBHI  <Wt>, <Wm>, <label>`
- **Fixed bits**: `sf`=`0`, `cc`=`010`
- **Bit Pattern**: `?????????????????????010???????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30  23  20  15  13   4  |
|-----------------------|
| sf  1110100 cc  Rm  00  imm9 Rt  |
```

### Variant: `Branch (CBHS_32_regs)` (32-bit higher or same)
- **Condition**: `sf == 0 && cc == 011`
- **Assembly**: `CBHS  <Wt>, <Wm>, <label>`
- **Fixed bits**: `sf`=`0`, `cc`=`011`
- **Bit Pattern**: `?????????????????????110???????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30  23  20  15  13   4  |
|-----------------------|
| sf  1110100 cc  Rm  00  imm9 Rt  |
```

### Variant: `Branch (CBEQ_32_regs)` (32-bit equal)
- **Condition**: `sf == 0 && cc == 110`
- **Assembly**: `CBEQ  <Wt>, <Wm>, <label>`
- **Fixed bits**: `sf`=`0`, `cc`=`110`
- **Bit Pattern**: `?????????????????????011???????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30  23  20  15  13   4  |
|-----------------------|
| sf  1110100 cc  Rm  00  imm9 Rt  |
```

### Variant: `Branch (CBNE_32_regs)` (32-bit not equal)
- **Condition**: `sf == 0 && cc == 111`
- **Assembly**: `CBNE  <Wt>, <Wm>, <label>`
- **Fixed bits**: `sf`=`0`, `cc`=`111`
- **Bit Pattern**: `?????????????????????111???????0`
**Encoding Diagram (32-bit)**:

```text
| 31 30  23  20  15  13   4  |
|-----------------------|
| sf  1110100 cc  Rm  00  imm9 Rt  |
```

### Variant: `Branch (CBGT_64_regs)` (64-bit greater than)
- **Condition**: `sf == 1 && cc == 000`
- **Assembly**: `CBGT  <Xt>, <Xm>, <label>`
- **Fixed bits**: `sf`=`1`, `cc`=`000`
- **Bit Pattern**: `?????????????????????000???????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30  23  20  15  13   4  |
|-----------------------|
| sf  1110100 cc  Rm  00  imm9 Rt  |
```

### Variant: `Branch (CBGE_64_regs)` (64-bit greater than or equal)
- **Condition**: `sf == 1 && cc == 001`
- **Assembly**: `CBGE  <Xt>, <Xm>, <label>`
- **Fixed bits**: `sf`=`1`, `cc`=`001`
- **Bit Pattern**: `?????????????????????100???????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30  23  20  15  13   4  |
|-----------------------|
| sf  1110100 cc  Rm  00  imm9 Rt  |
```

### Variant: `Branch (CBHI_64_regs)` (64-bit higher)
- **Condition**: `sf == 1 && cc == 010`
- **Assembly**: `CBHI  <Xt>, <Xm>, <label>`
- **Fixed bits**: `sf`=`1`, `cc`=`010`
- **Bit Pattern**: `?????????????????????010???????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30  23  20  15  13   4  |
|-----------------------|
| sf  1110100 cc  Rm  00  imm9 Rt  |
```

### Variant: `Branch (CBHS_64_regs)` (64-bit higher or same)
- **Condition**: `sf == 1 && cc == 011`
- **Assembly**: `CBHS  <Xt>, <Xm>, <label>`
- **Fixed bits**: `sf`=`1`, `cc`=`011`
- **Bit Pattern**: `?????????????????????110???????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30  23  20  15  13   4  |
|-----------------------|
| sf  1110100 cc  Rm  00  imm9 Rt  |
```

### Variant: `Branch (CBEQ_64_regs)` (64-bit equal)
- **Condition**: `sf == 1 && cc == 110`
- **Assembly**: `CBEQ  <Xt>, <Xm>, <label>`
- **Fixed bits**: `sf`=`1`, `cc`=`110`
- **Bit Pattern**: `?????????????????????011???????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30  23  20  15  13   4  |
|-----------------------|
| sf  1110100 cc  Rm  00  imm9 Rt  |
```

### Variant: `Branch (CBNE_64_regs)` (64-bit not equal)
- **Condition**: `sf == 1 && cc == 111`
- **Assembly**: `CBNE  <Xt>, <Xm>, <label>`
- **Fixed bits**: `sf`=`1`, `cc`=`111`
- **Bit Pattern**: `?????????????????????111???????1`
**Encoding Diagram (32-bit)**:

```text
| 31 30  23  20  15  13   4  |
|-----------------------|
| sf  1110100 cc  Rm  00  imm9 Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be tested, encoded in the "Rt" field. |
| `<Wm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the second general-purpose source register, encoded in the "Rm" field. |
| `<label>` | `label` | `imm9` | Is the program label to be conditionally branched to. Its offset from the address of this instruction, in the range -1024 to 1020, is encoded as "imm9 |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be tested, encoded in the "Rt" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the second general-purpose source register, encoded in the "Rm" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `cbcc_regs.xml`
</details>