## MRS
_ARM A64 Instruction_

**Title**: MRS -- A64 | **Class**: `system` | **XML ID**: `MRS`

**Summary**: Move System register to general-purpose register

**Description**:
This instruction allows the PE to read
an AArch64 System register into a general-purpose register.

### Variant: `System`
- **Assembly**: `MRS  <Xt>, (<systemreg>|S<op0>_<op1>_<Cn>_<Cm>_<op2>)`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  21 20 19 18  15  11   7   4  |
|-----------------------------------|
| 110 101 0100 1   1   o0  op1 CRn CRm op2 Rt  |
```

#### Decode (A64.control.systemmove.MRS_RS_systemmove)

```
constant integer t       = UInt(Rt);
constant bits(1) sys_L   = L;
constant bits(2) sys_op0 = '1' : o0;
constant bits(3) sys_op1 = op1;
constant bits(3) sys_op2 = op2;
constant bits(4) sys_crn = CRn;
constant bits(4) sys_crm = CRm;
```

#### Execute (A64.control.systemmove.MRS_RS_systemmove)

```
AArch64.CheckSystemAccess(sys_op0, sys_op1, sys_crn, sys_crm, sys_op2, t, sys_L);
AArch64.SysRegRead(sys_op0, sys_op1, sys_crn, sys_crm, sys_op2, t);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rt" field. |
| `<systemreg>` | `unknown` | `o0:op1:CRn:CRm:op2` | Is a System register name, encoded in "o0:op1:CRn:CRm:op2". The System register names are defined in 'AArch64 System Registers' in the System Register |
| `<op0>` | `register (32-bit)` | `o0` | Is an unsigned immediate, |
| `<op1>` | `unknown` | `op1` | Is a 3-bit unsigned immediate, in the range 0 to 7, encoded in the "op1" field. |
| `<Cn>` | `unknown` | `CRn` | Is a name 'Cn', with 'n' in the range 0 to 15, encoded in the "CRn" field. |
| `<Cm>` | `unknown` | `CRm` | Is a name 'Cm', with 'm' in the range 0 to 15, encoded in the "CRm" field. |
| `<op2>` | `unknown` | `op2` | Is a 3-bit unsigned immediate, in the range 0 to 7, encoded in the "op2" field. |

**<op0> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 2 |
| 1 | 3 |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `mrs.xml`
</details>