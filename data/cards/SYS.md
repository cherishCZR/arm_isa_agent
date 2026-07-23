## SYS
_ARM A64 Instruction_

**Title**: SYS -- A64 | **Class**: `system` | **XML ID**: `SYS`

**Summary**: System instruction

**Description**:
For more information, see
Op0 equals 0b01, cache maintenance, TLB maintenance, and address translation instructions
for the encodings of System instructions.

### Variant: `System`
- **Assembly**: `SYS  #<op1>, <Cn>, <Cm>, #<op2>{, <Xt>}`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  21 20  18  15  11   7   4  |
|--------------------------------|
| 110 101 0100 0   01  op1 CRn CRm op2 Rt  |
```

#### Decode (A64.control.systeminstrs.SYS_CR_systeminstrs)

```
constant integer t       = UInt(Rt);
constant bits(1) sys_L   = L;
constant bits(2) sys_op0 = '01';
constant bits(3) sys_op1 = op1;
constant bits(3) sys_op2 = op2;
constant bits(4) sys_crn = CRn;
constant bits(4) sys_crm = CRm;
```

#### Execute (A64.control.systeminstrs.SYS_CR_systeminstrs)

```
AArch64.CheckSystemAccess(sys_op0, sys_op1, sys_crn, sys_crm, sys_op2, t, sys_L);
AArch64.SysInstr(sys_op0, sys_op1, sys_crn, sys_crm, sys_op2, t);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<op1>` | `unknown` | `op1` | Is a 3-bit unsigned immediate, in the range 0 to 7, encoded in the "op1" field. |
| `<Cn>` | `unknown` | `CRn` | Is a name 'Cn', with 'n' in the range 0 to 15, encoded in the "CRn" field. |
| `<Cm>` | `unknown` | `CRm` | Is a name 'Cm', with 'm' in the range 0 to 15, encoded in the "CRm" field. |
| `<op2>` | `unknown` | `op2` | Is a 3-bit unsigned immediate, in the range 0 to 7, encoded in the "op2" field. |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the optional general-purpose source register, defaulting to '11111', encoded in the "Rt" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sys.xml`
</details>