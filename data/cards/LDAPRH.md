## LDAPRH
_ARM A64 Instruction_

**Title**: LDAPRH -- A64 | **Class**: `general` | **XML ID**: `LDAPRH`

**Architecture**: `FEAT_LRCPC` (ARMv8.3)

**Summary**: Load-acquire RCpc register halfword

**Description**:
This instruction derives an address from a base
register value, loads a halfword from the derived address in memory,
zero-extends it and writes it to a register.

The instruction has memory ordering semantics as described in
Load-Acquire, Load-AcquirePC, and Store-Release,
except that:

This difference in memory ordering is not described in the pseudocode.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Integer`
- **Assembly**: `LDAPRH  <Wt>, [<Xn|SP> {, #0}]`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24 23 22 21 20  15 14  11   9   4  |
|-----------------------------------------------|
| 01  11  1   0   0   0   1   0   1   (1)(1)(1)(1)(1) 1   100 00  Rn  Rt  |
```

#### Decode (A64.ldst.memop.LDAPRH_32L_memop)

```
if !IsFeatureImplemented(FEAT_LRCPC) then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.memop.LDAPRH_32L_memop)

```
bits(64) address;
bits(16) data;

constant AccessDescriptor accdesc = CreateAccDescLDAcqPC(tagchecked);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

data = Mem[address, 2, accdesc];
X[t, 32] = ZeroExtend(data, 32);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LRCPC)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be loaded, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `ldaprh.xml`
</details>