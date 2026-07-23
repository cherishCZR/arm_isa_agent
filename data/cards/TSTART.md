## TSTART
_ARM A64 Instruction_

**Title**: TSTART -- A64 | **Class**: `system` | **XML ID**: `TSTART`

**Architecture**: `FEAT_TME` (ARMv9.0)

**Summary**: Start transaction

**Description**:
This instruction starts a new transaction. If the transaction started
successfully, the destination register is set to zero. If the transaction
failed or was canceled, then all state modifications that were performed
transactionally are discarded and the destination register is written with a
nonzero value that encodes the cause of the failure.

### Variant: `System`
- **Assembly**: `TSTART  <Xt>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  18  15  11   7   4  |
|--------------------------|
| 110 101 0100100 011 0011 0000 011 Rt  |
```

#### Decode (A64.control.systemresult.TSTART_BR_systemresult)

```
if !IsFeatureImplemented(FEAT_TME) then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
```

#### Execute (A64.control.systemresult.TSTART_BR_systemresult)

```
if !IsTMEEnabled() then UNDEFINED;

boolean IsEL1Regime;
bit tme;
bit tmt;
case PSTATE.EL of
    when EL0
        IsEL1Regime = S1TranslationRegime() == EL1;
        if IsEL1Regime then
            tme = SCTLR_EL1.TME0;
            tmt = SCTLR_EL1.TMT0;
        else
            tme = SCTLR_EL2.TME0;
            tmt = SCTLR_EL2.TMT0;
    when EL1
        tme = SCTLR_EL1.TME;
        tmt = SCTLR_EL1.TMT;
    when EL2
        tme = SCTLR_EL2.TME;
        tmt = SCTLR_EL2.TMT;
    when EL3
        tme = SCTLR_EL3.TME;
        tmt = SCTLR_EL3.TMT;
    otherwise
        Unreachable();

constant boolean enable  = tme == '1';
constant boolean trivial = tmt == '1';

if !enable then
    TransactionStartTrap(t);
elsif trivial then
    TSTATE.nPC = NextInstrAddr(64);
    TSTATE.Rt = t;
    FailTransaction(TMFailure_TRIVIAL, FALSE);
elsif IsFeatureImplemented(FEAT_SME) && PSTATE.SM == '1' then
    FailTransaction(TMFailure_ERR, FALSE);
elsif TSTATE.depth == 255 then
    FailTransaction(TMFailure_NEST, FALSE);
elsif TSTATE.depth == 0 then
    TSTATE.nPC = NextInstrAddr(64);
    TSTATE.Rt = t;
    ClearExclusiveLocal(ProcessorID());
    TakeTransactionCheckpoint();
    StartTrackingTransactionalReadsWrites();

TSTATE.depth = TSTATE.depth + 1;
X[t, 64] = Zeros(64);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_TME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rt" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `tstart.xml`
</details>