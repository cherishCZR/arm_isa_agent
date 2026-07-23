## MSR
_ARM A64 Instruction_

**Title**: MSR (immediate) -- A64 | **Class**: `system` | **XML ID**: `MSR_imm`

**Summary**: Move immediate value to special register

**Description**:
This instruction moves an immediate value to
selected bits of the PSTATE. For more information, see
Process state, PSTATE.

The bits that can be written by this instruction are:

If FEAT_MTE is implemented and FEAT_MTE2
is not implemented, it is IMPLEMENTATION DEFINED
whether writes to PSTATE.TCO by this instruction are ignored.

### Variant: `System`
- **Condition**: `!(op1 == '000' && op2 IN {'00x', '010'})`
- **Assembly**: `MSR  <pstatefield>, #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  18  15  11   7   4  |
|--------------------------|
| 110 101 0100000 op1 0100 CRm op2 11111 |
```

#### Decode (A64.control.pstate.MSR_SI_pstate)

```
if op1 == '000' && op2 == '000' then SEE "CFINV";
if op1 == '000' && op2 == '001' then SEE "XAFLAG";
if op1 == '000' && op2 == '010' then SEE "AXFLAG";

bits(2) min_EL;
boolean need_secure = FALSE;

case op1 of
    when '00x'
        min_EL = EL1;
    when '010'
        min_EL = EL1;
    when '011'
        min_EL = EL0;
    when '100'
        min_EL = EL2;
    when '101'
        if !IsFeatureImplemented(FEAT_VHE) then EndOfDecode(Decode_UNDEF);
        min_EL = EL2;
    when '110'
        min_EL = EL3;
    when '111'
        min_EL = EL1;
        need_secure = TRUE;

constant bits(4) operand = CRm;
PSTATEField field;
case op1:op2 of
    when '000 011'
        if !IsFeatureImplemented(FEAT_UAO) then EndOfDecode(Decode_UNDEF);
        field = PSTATEField_UAO;
    when '000 100'
        if !IsFeatureImplemented(FEAT_PAN) then EndOfDecode(Decode_UNDEF);
        field = PSTATEField_PAN;
    when '000 101' field = PSTATEField_SP;
    when '001 000'
        case CRm of
            when '000x'
                if !IsFeatureImplemented(FEAT_NMI) then EndOfDecode(Decode_UNDEF);
                field = PSTATEField_ALLINT;
            when '001x'
                if !IsFeatureImplemented(FEAT_EBEP) then EndOfDecode(Decode_UNDEF);
                field = PSTATEField_PM;
            otherwise
                EndOfDecode(Decode_UNDEF);
    when '011 010'
        if !IsFeatureImplemented(FEAT_DIT) then EndOfDecode(Decode_UNDEF);
        field = PSTATEField_DIT;
    when '011 011'
        case CRm of
            when '001x'
                if !IsFeatureImplemented(FEAT_SME) then EndOfDecode(Decode_UNDEF);
                field = PSTATEField_SVCRSM;
            when '010x'
                if !IsFeatureImplemented(FEAT_SME) then EndOfDecode(Decode_UNDEF);
                field = PSTATEField_SVCRZA;
            when '011x'
                if !IsFeatureImplemented(FEAT_SME) then EndOfDecode(Decode_UNDEF);
                field = PSTATEField_SVCRSMZA;
            otherwise
                EndOfDecode(Decode_UNDEF);
    when '011 100'
        if !IsFeatureImplemented(FEAT_MTE) then EndOfDecode(Decode_UNDEF);
        field = PSTATEField_TCO;
    when '011 110' field = PSTATEField_DAIFSet;
    when '011 111' field = PSTATEField_DAIFClr;
    when '011 001'
        if !IsFeatureImplemented(FEAT_SSBS) then EndOfDecode(Decode_UNDEF);
        field = PSTATEField_SSBS;
    otherwise      EndOfDecode(Decode_UNDEF);
```

#### Execute (A64.control.pstate.MSR_SI_pstate)

```
AArch64.CheckSystemAccess('00', op1, '0100', CRm, op2, 31, '0');
if UInt(PSTATE.EL) < UInt(min_EL) then UNDEFINED;
if need_secure && CurrentSecurityState() != SS_Secure then UNDEFINED;

case field of
    when PSTATEField_SSBS
        PSTATE.SSBS = operand<0>;
    when PSTATEField_SP
        PSTATE.SP = operand<0>;
    when PSTATEField_DAIFSet
        AArch64.CheckDAIFAccess(PSTATEField_DAIFSet);
        PSTATE.D = PSTATE.D OR operand<3>;
        PSTATE.A = PSTATE.A OR operand<2>;
        PSTATE.I = PSTATE.I OR operand<1>;
        PSTATE.F = PSTATE.F OR operand<0>;
    when PSTATEField_DAIFClr
        AArch64.CheckDAIFAccess(PSTATEField_DAIFClr);
        PSTATE.D = PSTATE.D AND NOT(operand<3>);
        PSTATE.A = PSTATE.A AND NOT(operand<2>);
        PSTATE.I = PSTATE.I AND NOT(operand<1>);
        PSTATE.F = PSTATE.F AND NOT(operand<0>);
    when PSTATEField_PAN
        PSTATE.PAN = operand<0>;
    when PSTATEField_UAO
        PSTATE.UAO = operand<0>;
    when PSTATEField_DIT
        PSTATE.DIT = operand<0>;
    when PSTATEField_TCO
        PSTATE.TCO = operand<0>;
    when PSTATEField_ALLINT
        if (PSTATE.EL == EL1 && IsHCRXEL2Enabled() &&
              HCRX_EL2.TALLINT == '1' && operand<0> == '1') then
            AArch64.SystemAccessTrap(EL2, 0x18);
        PSTATE.ALLINT = operand<0>;
    when PSTATEField_SVCRSM
        CheckSMEAccess();
        SetPSTATE_SM(operand<0>);
    when PSTATEField_SVCRZA
        CheckSMEAccess();
        SetPSTATE_ZA(operand<0>);
    when PSTATEField_SVCRSMZA
        CheckSMEAccess();
        SetPSTATE_SM(operand<0>);
        SetPSTATE_ZA(operand<0>);
    when PSTATEField_PM
        PSTATE.PM = operand<0>;
```

#### Constraints
_1× ↩ DECODE_FALLBACK / 9× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_VHE)` |
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_UAO)` |
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_PAN)` |
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_NMI)` |
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_EBEP)` |
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_DIT)` |
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME)` |
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_MTE)` |
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SSBS)` |
| ↩ DECODE_FALLBACK | `matching encodings` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<pstatefield>` | `unknown` | `CRm:op1:op2` | Is a PSTATE field name. For the MSR instruction, this is |
| `<imm>` | `immediate` | `CRm:op1:op2` | Is a 4-bit unsigned immediate, in the range 0 to 15, encoded in the "CRm" field. Restricted to the range 0 to 1, encoded in "CRm<0>", when <pstatefiel |

**<pstatefield> Value Table**:

| bitfield | symbol |
|---|---|
| 011 |  |
| 100 |  |
| 101 |  |
| 11x |  |
| 000 |  |
| 001 |  |
| 01x |  |
| 1xx |  |
| xxx |  |
| 000 |  |
| 001 |  |
| 010 |  |
| 011 |  |
| 100 |  |
| 101 |  |
| 110 |  |
| 111 |  |
| xxx |  |
| 000 |  |
| 011 |  |
| 000 |  |
| 011 |  |
| 011 |  |
| 000 |  |
| 011 |  |

---
<details><summary>Metadata</summary>

- isa: `A64`
- msr-sysreg-target: `whole-register`
- source: `msr_imm.xml`
</details>