## RCWSWP
_ARM A64 Instruction_

**Title**: RCWSWP, RCWSWPA, RCWSWPAL, RCWSWPL -- A64 | **Class**: `general` | **XML ID**: `RCWSWP`

**Architecture**: `FEAT_THE` (ARMv8.9)

**Summary**: Read check write swap doubleword in memory

**Description**:
This instruction atomically loads
a 64-bit doubleword from a memory location, and conditionally stores the value
held in a register back to the same memory location. Storing back to memory
is conditional on RCW Checks. The value initially
loaded from memory is returned in the destination register.
This instruction updates the condition flags based on the result of the update
of memory.

### Variant: `Integer (RCWSWP_64_memop)` (RCWSWP)
- **Condition**: `A == 0 && R == 0`
- **Assembly**: `RCWSWP  <Xs>, <Xt>, [<Xn|SP>]`
- **Fixed bits**: `A`=`0`, `R`=`0`
- **Bit Pattern**: `??????????????????????00????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  26 25  23 22 21 20  15 14  11   9   4  |
|--------------------------------------------|
| 0   0   111 0   00  A   R   1   Rs  1   010 00  Rn  Rt  |
```

#### Decode (A64.ldst.memop.RCWSWP_64_memop)

```
if !IsFeatureImplemented(FEAT_THE) then EndOfDecode(Decode_UNDEF);
constant integer s = UInt(Rs);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant boolean soft = FALSE;

constant boolean acquire = A == '1' && Rt != '11111';
constant boolean release = R == '1';
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.memop.RCWSWP_64_memop)

```
if IsD128Enabled(PSTATE.EL) then UNDEFINED;
bits(64) address;
constant bits(64) newdata = X[s, 64];
bits(64) readdata;
bits(4) nzcv;

constant AccessDescriptor accdesc = CreateAccDescRCW(MemAtomicOp_SWP, soft, acquire, release,
                                                     tagchecked);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

constant bits(64) compdata = bits(64) UNKNOWN;    // Irrelevant when not executing CAS
(nzcv, readdata) = MemAtomicRCW(address, compdata, newdata, accdesc);

PSTATE.<N,Z,C,V> = nzcv;
X[t, 64] = readdata;   // Return the old value when t!=31
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_THE)` |

### Variant: `Integer (RCWSWPA_64_memop)` (RCWSWPA)
- **Condition**: `A == 1 && R == 0`
- **Assembly**: `RCWSWPA  <Xs>, <Xt>, [<Xn|SP>]`
- **Fixed bits**: `A`=`1`, `R`=`0`
- **Bit Pattern**: `??????????????????????01????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  26 25  23 22 21 20  15 14  11   9   4  |
|--------------------------------------------|
| 0   0   111 0   00  A   R   1   Rs  1   010 00  Rn  Rt  |
```

### Variant: `Integer (RCWSWPAL_64_memop)` (RCWSWPAL)
- **Condition**: `A == 1 && R == 1`
- **Assembly**: `RCWSWPAL  <Xs>, <Xt>, [<Xn|SP>]`
- **Fixed bits**: `A`=`1`, `R`=`1`
- **Bit Pattern**: `??????????????????????11????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  26 25  23 22 21 20  15 14  11   9   4  |
|--------------------------------------------|
| 0   0   111 0   00  A   R   1   Rs  1   010 00  Rn  Rt  |
```

### Variant: `Integer (RCWSWPL_64_memop)` (RCWSWPL)
- **Condition**: `A == 0 && R == 1`
- **Assembly**: `RCWSWPL  <Xs>, <Xt>, [<Xn|SP>]`
- **Fixed bits**: `A`=`0`, `R`=`1`
- **Bit Pattern**: `??????????????????????10????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  26 25  23 22 21 20  15 14  11   9   4  |
|--------------------------------------------|
| 0   0   111 0   00  A   R   1   Rs  1   010 00  Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xs>` | `register (64-bit)` | `Rs` | Is the 64-bit name of the general-purpose register to be stored, encoded in the "Rs" field. |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be loaded, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `rcwswp.xml`
</details>