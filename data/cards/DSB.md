## DSB
_ARM A64 Instruction_

**Title**: DSB -- A64 | **Class**: `system` | **XML ID**: `DSB`

**Architecture**: `FEAT_XS` (ARMv8.7)

**Summary**: Data synchronization barrier

**Description**:
This instruction is a memory barrier that ensures the completion
of memory accesses, see Data Synchronization Barrier.

### Variant: `Memory barrier`
- **Assembly**: `DSB  (<option>|#<imm>)`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7  6   4  |
|-----------------------|
| 110 101 01000000110011 CRm 1   00  11111 |
```

#### Decode (A64.control.barriers.DSB_BO_barriers)

```
boolean nXS = FALSE;

DSBAlias alias;
case CRm of
    when '0000' alias = DSBAlias_SSBB;
    when '0100' alias = DSBAlias_PSSBB;
    otherwise   alias = DSBAlias_DSB;

MBReqDomain domain;
case CRm<3:2> of
    when '00' domain = MBReqDomain_OuterShareable;
    when '01' domain = MBReqDomain_Nonshareable;
    when '10' domain = MBReqDomain_InnerShareable;
    when '11' domain = MBReqDomain_FullSystem;

MBReqTypes types;
case CRm<1:0> of
    when '00' types = MBReqTypes_All; domain = MBReqDomain_FullSystem;
    when '01' types = MBReqTypes_Reads;
    when '10' types = MBReqTypes_Writes;
    when '11' types = MBReqTypes_All;
```

#### Execute (A64.control.barriers.DSB_BO_barriers)

```
case alias of
    when DSBAlias_SSBB
        SpeculativeStoreBypassBarrierToVA();
    when DSBAlias_PSSBB
        SpeculativeStoreBypassBarrierToPA();
    when DSBAlias_DSB
        if IsFeatureImplemented(FEAT_TME) && TSTATE.depth > 0 then
            FailTransaction(TMFailure_ERR, FALSE);
        if !nXS && IsFeatureImplemented(FEAT_XS) then
            nXS = PSTATE.EL IN {EL0, EL1} && IsHCRXEL2Enabled() && HCRX_EL2.FnXS == '1';
        DataSynchronizationBarrier(domain, types, nXS);
    otherwise
        Unreachable();
```

### Variant: `Memory nXS barrier`
- **Assembly**: `DSB  <option>nXS`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   9   7   4  |
|-----------------------|
| 110 101 01000000110011 imm2 10  001 11111 |
```

#### Decode (A64.control.barriers.DSB_BOn_barriers)

```
if !IsFeatureImplemented(FEAT_XS) then EndOfDecode(Decode_UNDEF);
constant MBReqTypes types = MBReqTypes_All;
boolean nXS = TRUE;
constant DSBAlias alias = DSBAlias_DSB;
MBReqDomain domain;

case imm2 of
    when '00' domain = MBReqDomain_OuterShareable;
    when '01' domain = MBReqDomain_Nonshareable;
    when '10' domain = MBReqDomain_InnerShareable;
    when '11' domain = MBReqDomain_FullSystem;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_XS)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<option>` | `unknown` | `CRm` | For the "Memory barrier" variant: specifies the limitation on the barrier operation. Values are:                                       SY              |
| `<option>` | `unknown` | `imm2` | For the "Memory nXS barrier" variant: specifies the limitation on the barrier operation. Values are:                                       SY          |
| `<imm>` | `immediate` | `CRm` | Is a 4-bit unsigned immediate, in the range 0 to 15, encoded in the "CRm" field. |

**<option> Value Table**:

| bitfield | symbol |
|---|---|
| 0001 | OSHLD |
| 0010 | OSHST |
| 0011 | OSH |
| 0101 | NSHLD |
| 0110 | NSHST |
| 0111 | NSH |
| 1000 | RESERVED |
| 1001 | ISHLD |
| 1010 | ISHST |
| 1011 | ISH |
| 1100 | RESERVED |
| 1101 | LD |
| 1110 | ST |
| 1111 | SY |

**<option> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | OSH |
| 01 | NSH |
| 10 | ISH |
| 11 | SY |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `dsb.xml`
</details>