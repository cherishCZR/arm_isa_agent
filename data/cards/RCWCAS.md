## RCWCAS
_ARM A64 Instruction_

**Title**: RCWCAS, RCWCASA, RCWCASAL, RCWCASL -- A64 | **Class**: `general` | **XML ID**: `RCWCAS`

**Architecture**: `FEAT_THE` (ARMv8.9)

**Summary**: Read check write compare and swap doubleword in memory

**Description**:
This instruction reads a 64-bit doubleword
from memory, and compares it against the value held in a register. If the comparison
is equal, the value in a second register is conditionally written to memory.
Storing back to memory is conditional on RCW Checks. If the compare fails or the RCW Checks fail,
the architecture permits writing the value read from the location to memory.
If the write is performed, the read and the write occur atomically such that no other
modification of the memory location can take place between the read and the write.
This instruction updates the condition flags based on the result of the update of
memory.

### Variant: `Integer (RCWCAS_C64_rcwcomswap)` (RCWCAS)
- **Condition**: `A == 0 && R == 0`
- **Assembly**: `RCWCAS  <Xs>, <Xt>, [<Xn|SP>]`
- **Fixed bits**: `A`=`0`, `R`=`0`
- **Bit Pattern**: `??????????????????????00????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15   9   4  |
|--------------------------------|
| 0   0   011001 A   R   1   Rs  000010 Rn  Rt  |
```

#### Decode (A64.ldst.rcwcomswap.RCWCAS_C64_rcwcomswap)

```
if !IsFeatureImplemented(FEAT_THE) then EndOfDecode(Decode_UNDEF);
constant integer s = UInt(Rs);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant boolean soft = FALSE;

constant boolean acquire = A == '1';
constant boolean release = R == '1';
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.rcwcomswap.RCWCAS_C64_rcwcomswap)

```
if IsD128Enabled(PSTATE.EL) then UNDEFINED;
bits(64) address;
constant bits(64) newdata = X[t, 64];
constant bits(64) compdata = X[s, 64];
bits(64) readdata;
bits(4) nzcv;

constant AccessDescriptor accdesc = CreateAccDescRCW(MemAtomicOp_CAS, soft, acquire, release,
                                                     tagchecked);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

(nzcv, readdata) = MemAtomicRCW(address, compdata, newdata, accdesc);

PSTATE.<N,Z,C,V> = nzcv;
X[s, 64] = readdata;   // Return the old value when s!=31
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_THE)` |

### Variant: `Integer (RCWCASA_C64_rcwcomswap)` (RCWCASA)
- **Condition**: `A == 1 && R == 0`
- **Assembly**: `RCWCASA  <Xs>, <Xt>, [<Xn|SP>]`
- **Fixed bits**: `A`=`1`, `R`=`0`
- **Bit Pattern**: `??????????????????????01????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15   9   4  |
|--------------------------------|
| 0   0   011001 A   R   1   Rs  000010 Rn  Rt  |
```

### Variant: `Integer (RCWCASAL_C64_rcwcomswap)` (RCWCASAL)
- **Condition**: `A == 1 && R == 1`
- **Assembly**: `RCWCASAL  <Xs>, <Xt>, [<Xn|SP>]`
- **Fixed bits**: `A`=`1`, `R`=`1`
- **Bit Pattern**: `??????????????????????11????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15   9   4  |
|--------------------------------|
| 0   0   011001 A   R   1   Rs  000010 Rn  Rt  |
```

### Variant: `Integer (RCWCASL_C64_rcwcomswap)` (RCWCASL)
- **Condition**: `A == 0 && R == 1`
- **Assembly**: `RCWCASL  <Xs>, <Xt>, [<Xn|SP>]`
- **Fixed bits**: `A`=`0`, `R`=`1`
- **Bit Pattern**: `??????????????????????10????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15   9   4  |
|--------------------------------|
| 0   0   011001 A   R   1   Rs  000010 Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xs>` | `register (64-bit)` | `Rs` | Is the 64-bit name of the general-purpose register to be compared and loaded, encoded in the "Rs" field. |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be conditionally stored, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `rcwcas.xml`
</details>