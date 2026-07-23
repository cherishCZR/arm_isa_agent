## CBBcc_regs
_ARM A64 Instruction_

**Title**: CBB<cc> -- A64 | **Class**: `general` | **XML ID**: `CBBcc_regs`

**Architecture**: `FEAT_CMPBR` (ARMv9.6)

**Summary**: Compare bytes and branch

**Description**:
This instruction compares the byte values in two registers, and conditionally
branches to a label at a PC-relative offset if the condition is true.
It provides a hint that this is not a subroutine call or return.
This instruction does not affect the condition flags.

### Variant: `Branch (CBBGT_8_regs)` (Greater than)
- **Condition**: `cc == 000`
- **Assembly**: `CBBGT  <Wt>, <Wm>, <label>`
- **Fixed bits**: `cc`=`000`
- **Bit Pattern**: `?????????????????????000????????`
**Encoding Diagram (32-bit)**:

```text
| 31  23  20  15 14 13   4  |
|-----------------------|
| 01110100 cc  Rm  1   0   imm9 Rt  |
```

#### Decode (A64.control.compbranch_regs2.CBBGT_8_regs)

```
if !IsFeatureImplemented(FEAT_CMPBR) then EndOfDecode(Decode_UNDEF);
constant integer datasize = 8 << UInt(H);
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

#### Execute (A64.control.compbranch_regs2.CBBGT_8_regs)

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

### Variant: `Branch (CBBGE_8_regs)` (Greater than or equal)
- **Condition**: `cc == 001`
- **Assembly**: `CBBGE  <Wt>, <Wm>, <label>`
- **Fixed bits**: `cc`=`001`
- **Bit Pattern**: `?????????????????????100????????`
**Encoding Diagram (32-bit)**:

```text
| 31  23  20  15 14 13   4  |
|-----------------------|
| 01110100 cc  Rm  1   0   imm9 Rt  |
```

### Variant: `Branch (CBBHI_8_regs)` (Higher)
- **Condition**: `cc == 010`
- **Assembly**: `CBBHI  <Wt>, <Wm>, <label>`
- **Fixed bits**: `cc`=`010`
- **Bit Pattern**: `?????????????????????010????????`
**Encoding Diagram (32-bit)**:

```text
| 31  23  20  15 14 13   4  |
|-----------------------|
| 01110100 cc  Rm  1   0   imm9 Rt  |
```

### Variant: `Branch (CBBHS_8_regs)` (Higher or same)
- **Condition**: `cc == 011`
- **Assembly**: `CBBHS  <Wt>, <Wm>, <label>`
- **Fixed bits**: `cc`=`011`
- **Bit Pattern**: `?????????????????????110????????`
**Encoding Diagram (32-bit)**:

```text
| 31  23  20  15 14 13   4  |
|-----------------------|
| 01110100 cc  Rm  1   0   imm9 Rt  |
```

### Variant: `Branch (CBBEQ_8_regs)` (Equal)
- **Condition**: `cc == 110`
- **Assembly**: `CBBEQ  <Wt>, <Wm>, <label>`
- **Fixed bits**: `cc`=`110`
- **Bit Pattern**: `?????????????????????011????????`
**Encoding Diagram (32-bit)**:

```text
| 31  23  20  15 14 13   4  |
|-----------------------|
| 01110100 cc  Rm  1   0   imm9 Rt  |
```

### Variant: `Branch (CBBNE_8_regs)` (Not equal)
- **Condition**: `cc == 111`
- **Assembly**: `CBBNE  <Wt>, <Wm>, <label>`
- **Fixed bits**: `cc`=`111`
- **Bit Pattern**: `?????????????????????111????????`
**Encoding Diagram (32-bit)**:

```text
| 31  23  20  15 14 13   4  |
|-----------------------|
| 01110100 cc  Rm  1   0   imm9 Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be tested, encoded in the "Rt" field. |
| `<Wm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the second general-purpose source register, encoded in the "Rm" field. |
| `<label>` | `label` | `imm9` | Is the program label to be conditionally branched to. Its offset from the address of this instruction, in the range -1024 to 1020, is encoded as "imm9 |

---
<details><summary>Metadata</summary>

- datatype: `8`
- isa: `A64`
- source: `cbbcc_regs.xml`
</details>