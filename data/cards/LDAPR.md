## LDAPR
_ARM A64 Instruction_

**Title**: LDAPR -- A64 | **Class**: `general` | **XML ID**: `LDAPR`

**Architecture**: `FEAT_LRCPC3` (ARMv8.9), `FEAT_LRCPC` (ARMv8.3)

**Summary**: Load-acquire RCpc register

**Description**:
This instruction derives an address from a base register
value, loads a 32-bit word or 64-bit doubleword from the derived
address in memory, and writes it to a register.

The instruction has memory ordering semantics as described in
Load-Acquire, Load-AcquirePC, and Store-Release,
except that:

This difference in memory ordering is not described in the pseudocode.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Post-index (LDAPR_32L_ldapstl_writeback)` (32-bit)
- **Condition**: `size == 10`
- **Assembly**: `LDAPR  <Wt>, [<Xn|SP>], #4`
- **Fixed bits**: `size`=`0`
- **Bit Pattern**: `??????????????????????????????0?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  22 21   9   4  |
|--------------------|
| 1x  0110011 1   000000000010 Rn  Rt  |
```

#### Decode (A64.ldst.ldapstl_writeback.LDAPR_32L_ldapstl_writeback)

```
if !IsFeatureImplemented(FEAT_LRCPC3) then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
boolean wback = TRUE;
constant integer regsize = if size == '11' then 64 else 32;
constant integer datasize = 8 << UInt(size);
constant integer offset = 1 << UInt(size);

constant boolean tagchecked = TRUE;

boolean wb_unknown = FALSE;

if n == t && n != 31 then
    constant Constraint c = ConstrainUnpredictable(Unpredictable_WBOVERLAPLD);
    assert c IN {Constraint_WBSUPPRESS, Constraint_UNKNOWN, Constraint_UNDEF, Constraint_NOP};
    case c of
        when Constraint_WBSUPPRESS wback = FALSE;        // writeback is suppressed
        when Constraint_UNKNOWN    wb_unknown = TRUE;    // writeback is UNKNOWN
        when Constraint_UNDEF      EndOfDecode(Decode_UNDEF);
        when Constraint_NOP        EndOfDecode(Decode_NOP);
```

#### Execute (A64.ldst.ldapstl_writeback.LDAPR_32L_ldapstl_writeback)

```
bits(64) address;
bits(datasize) data;
constant integer dbytes = datasize DIV 8;

constant AccessDescriptor accdesc = CreateAccDescLDAcqPC(tagchecked);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

data = Mem[address, dbytes, accdesc];
X[t, regsize] = ZeroExtend(data, regsize);
if wback then
    if wb_unknown then
        address = bits(64) UNKNOWN;
    else
        address = AddressAdd(address, offset, accdesc);
    if n == 31 then
        SP[64] = address;
    else
        X[n, 64] = address;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LRCPC3)` |

### Variant: `Post-index (LDAPR_64L_ldapstl_writeback)` (64-bit)
- **Condition**: `size == 11`
- **Assembly**: `LDAPR  <Xt>, [<Xn|SP>], #8`
- **Fixed bits**: `size`=`1`
- **Bit Pattern**: `??????????????????????????????1?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  22 21   9   4  |
|--------------------|
| 1x  0110011 1   000000000010 Rn  Rt  |
```

### Variant: `No offset (LDAPR_32L_memop)` (32-bit)
- **Condition**: `size == 10`
- **Assembly**: `LDAPR  <Wt>, [<Xn|SP> {, #0}]`
- **Fixed bits**: `size`=`0`
- **Bit Pattern**: `??????????????????????????????0?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  1   0   1   (1)(1)(1)(1)(1) 1   100 00  Rn  Rt  |
```

#### Decode (A64.ldst.memop.LDAPR_32L_memop)

```
if !IsFeatureImplemented(FEAT_LRCPC) then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant boolean wback = FALSE;
constant integer offset = 0;
constant boolean wb_unknown = FALSE;
constant integer elsize = 8 << UInt(size);
constant integer regsize = if elsize == 64 then 64 else 32;
constant integer datasize = elsize;
constant boolean tagchecked = n != 31;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LRCPC)` |

### Variant: `No offset (LDAPR_64L_memop)` (64-bit)
- **Condition**: `size == 11`
- **Assembly**: `LDAPR  <Xt>, [<Xn|SP> {, #0}]`
- **Fixed bits**: `size`=`1`
- **Bit Pattern**: `??????????????????????????????1?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  1   0   1   (1)(1)(1)(1)(1) 1   100 00  Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be loaded, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be loaded, encoded in the "Rt" field. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `ldapr.xml`
</details>