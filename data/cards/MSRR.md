## MSRR
_ARM A64 Instruction_

**Title**: MSRR -- A64 | **Class**: `system` | **XML ID**: `MSRR`

**Architecture**: `FEAT_SYSREG128` (ARMv9.4)

**Summary**: Move two adjacent general-purpose registers to System register

**Description**:
This instruction allows the PE
to write an AArch64 128-bit System register from two adjacent 64-bit general-purpose
registers.

### Variant: `System`
- **Assembly**: `MSRR  (<systemreg>|S<op0>_<op1>_<Cn>_<Cm>_<op2>), <Xt>, <Xt+1>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  21 20 19 18  15  11   7   4  |
|-----------------------------------|
| 110 101 0101 0   1   o0  op1 CRn CRm op2 Rt  |
```

#### Decode (A64.control.systemmovepr.MSRR_SR_systemmovepr)

```
if !IsFeatureImplemented(FEAT_SYSREG128) then EndOfDecode(Decode_UNDEF);
if Rt<0> == '1' then EndOfDecode(Decode_UNDEF);

constant integer t       = UInt(Rt);
constant integer t2      = UInt(Rt+1);
constant bits(1) sys_L   = L;
constant bits(2) sys_op0 = '1' : o0;
constant bits(3) sys_op1 = op1;
constant bits(3) sys_op2 = op2;
constant bits(4) sys_crn = CRn;
constant bits(4) sys_crm = CRm;
```

#### Execute (A64.control.systemmovepr.MSRR_SR_systemmovepr)

```
AArch64.CheckSystemAccess(sys_op0, sys_op1, sys_crn, sys_crm, sys_op2, t, sys_L);
AArch64.SysRegWrite128(sys_op0, sys_op1, sys_crn, sys_crm, sys_op2, t, t2);
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SYSREG128)` |
| 🚫 ENCODING_UNDEF | `Rt<0> != '1'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<systemreg>` | `unknown` | `o0:op1:CRn:CRm:op2` | Is a System register name, encoded in "o0:op1:CRn:CRm:op2". |
| `<op0>` | `register (32-bit)` | `o0` | Is an unsigned immediate, |
| `<op1>` | `unknown` | `op1` | Is a 3-bit unsigned immediate, in the range 0 to 7, encoded in the "op1" field. |
| `<Cn>` | `unknown` | `CRn` | Is a name 'Cn', with 'n' in the range 0 to 15, encoded in the "CRn" field. |
| `<Cm>` | `unknown` | `CRm` | Is a name 'Cm', with 'm' in the range 0 to 15, encoded in the "CRm" field. |
| `<op2>` | `unknown` | `op2` | Is a 3-bit unsigned immediate, in the range 0 to 7, encoded in the "op2" field. |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the first general-purpose source register, encoded in the "Rt" field. |
| `<Xt+1>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the second  general-purpose source register, encoded as "Rt" +1. |

**<op0> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 2 |
| 1 | 3 |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `msrr.xml`
</details>