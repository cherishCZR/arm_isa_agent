## XPAC
_ARM A64 Instruction_

**Title**: XPACD, XPACI, XPACLRI -- A64 | **Class**: `N/A` | **XML ID**: `XPAC`

**Architecture**: `FEAT_PAuth` (ARMv8.3)

**Summary**: Strip Pointer Authentication Code

**Description**:
This instruction removes the Pointer Authentication Code from an
address. The address is in the specified general-purpose register
for XPACI and XPACD, and is in LR for XPACLRI.

The XPACD instruction is used for data addresses, and
XPACI and XPACLRI are used for instruction addresses.

### Variant: `Integer (XPACD_64Z_dp_1src)` (XPACD)
- **Condition**: `D == 1`
- **Assembly**: `XPACD  <Xd>`
- **Fixed bits**: `D`=`1`
- **Bit Pattern**: `??????????1?????????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  10  9   4  |
|-----------------------------|
| 1   1   0   11010110 00001 01000 D   11111 Rd  |
```

#### Decode (A64.dpreg.dp_1src.XPACD_64Z_dp_1src)

```
if !IsFeatureImplemented(FEAT_PAuth) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant boolean data = (D == '1');
```

#### Execute (A64.dpreg.dp_1src.XPACD_64Z_dp_1src)

```
X[d, 64] = Strip(X[d, 64], data);
```

### Variant: `Integer (XPACI_64Z_dp_1src)` (XPACI)
- **Condition**: `D == 0`
- **Assembly**: `XPACI  <Xd>`
- **Fixed bits**: `D`=`0`
- **Bit Pattern**: `??????????0?????????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  10  9   4  |
|-----------------------------|
| 1   1   0   11010110 00001 01000 D   11111 Rd  |
```

### Variant: `System`
- **Assembly**: `XPACLRI`
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  11   7   4  |
|--------------------|
| 110 101 01000000110010 0000 111 11111 |
```

#### Decode (A64.control.hints.XPACLRI_HI_hints)

```
if !IsFeatureImplemented(FEAT_PAuth) then EndOfDecode(Decode_NOP);
constant integer d = 30;
constant boolean data = FALSE;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_PAuth)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `xpac.xml`
</details>