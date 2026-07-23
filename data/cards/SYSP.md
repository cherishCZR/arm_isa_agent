## SYSP
_ARM A64 Instruction_

**Title**: SYSP -- A64 | **Class**: `system` | **XML ID**: `SYSP`

**Architecture**: `FEAT_SYSINSTR128` (ARMv9.4)

**Summary**: 128-bit system instruction

**Description**:
128-bit system instruction.

### Variant: `System`
- **Assembly**: `SYSP  #<op1>, <Cn>, <Cm>, #<op2>{, <Xt1>, <Xt2>}`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  21 20  18  15  11   7   4  |
|--------------------------------|
| 110 101 0101 0   01  op1 CRn CRm op2 Rt  |
```

#### Decode (A64.control.syspairinstrs.SYSP_CR_syspairinstrs)

```
if !IsFeatureImplemented(FEAT_SYSINSTR128) then EndOfDecode(Decode_UNDEF);
if Rt<0> == '1' && Rt != '11111' then EndOfDecode(Decode_UNDEF);

constant integer t       = UInt(Rt);
constant integer t2      = if t == 31 then 31 else t + 1;
constant bits(1) sys_L   = L;
constant bits(2) sys_op0 = '01';
constant bits(3) sys_op1 = op1;
constant bits(3) sys_op2 = op2;
constant bits(4) sys_crn = CRn;
constant bits(4) sys_crm = CRm;
```

#### Execute (A64.control.syspairinstrs.SYSP_CR_syspairinstrs)

```
AArch64.CheckSystemAccess(sys_op0, sys_op1, sys_crn, sys_crm, sys_op2, t, sys_L);
AArch64.SysInstr128(sys_op0, sys_op1, sys_crn, sys_crm, sys_op2, t, t2);
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SYSINSTR128)` |
| 🚫 ENCODING_UNDEF | `Rt<0> != '1' \|\| Rt == '11111'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<op1>` | `unknown` | `op1` | Is a 3-bit unsigned immediate, in the range 0 to 6, encoded in the "op1" field. |
| `<Cn>` | `unknown` | `CRn` | Is a name 'Cn', with 'n' in the range 8 to 9, encoded in the "CRn" field. |
| `<Cm>` | `unknown` | `CRm` | Is a name 'Cm', with 'm' in the range 0 to 7, encoded in the "CRm" field. |
| `<op2>` | `unknown` | `op2` | Is a 3-bit unsigned immediate, in the range 0 to 7, encoded in the "op2" field. |
| `<Xt1>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the first optional general-purpose source register, defaulting to '11111', encoded in the "Rt" field. |
| `<Xt2>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the second optional general-purpose source register, defaulting to '11111', encoded as "Rt" +1. Defaults to '11111' if "Rt" = '1 |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sysp.xml`
</details>