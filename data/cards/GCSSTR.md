## GCSSTR
_ARM A64 Instruction_

**Title**: GCSSTR -- A64 | **Class**: `general` | **XML ID**: `GCSSTR`

**Architecture**: `FEAT_GCS` (ARMv9.4)

**Summary**: Guarded Control Stack store register

**Description**:
This instruction stores a doubleword from
a register to memory. The address that is used for the store
is calculated from a base register.

### Variant: `Integer`
- **Assembly**: `GCSSTR  <Xt>, [<Xn|SP>]`
**Encoding Diagram (32-bit)**:

```text
| 31  27 26 25 24  14  11   9   4  |
|-----------------------------|
| 1101 1   0   0   1000111110 000 11  Rn  Rt  |
```

#### Decode (A64.ldst.ldst_gcs.GCSSTR_64_ldst_gcs)

```
if !IsFeatureImplemented(FEAT_GCS) then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
```

#### Execute (A64.ldst.ldst_gcs.GCSSTR_64_ldst_gcs)

```
bits(64) address;

constant bits(2) effective_el = PSTATE.EL;

if effective_el == PSTATE.EL then
    CheckGCSSTREnabled();

constant boolean privileged = effective_el != EL0;
constant AccessDescriptor accdesc = CreateAccDescGCS(MemOp_STORE, privileged);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

Mem[address, 8, accdesc] = X[t, 64];
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_GCS)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `gcsstr.xml`
</details>