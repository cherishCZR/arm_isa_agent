## AUTDB
_ARM A64 Instruction_

**Title**: AUTDB, AUTDZB -- A64 | **Class**: `general` | **XML ID**: `AUTDB`

**Architecture**: `FEAT_PAuth` (ARMv8.3)

**Summary**: Authenticate data address, using key B

**Description**:
This instruction authenticates a data address, using a modifier and key B.

The address is in the general-purpose register that is specified by
<Xd>.

The modifier is:

If the authentication passes, the upper bits of the address are
restored to enable subsequent use of the address.
For information on behavior if the authentication fails, see
Faulting on pointer authentication.

### Variant: `Integer (AUTDB_64P_dp_1src)` (AUTDB)
- **Condition**: `Z == 0`
- **Assembly**: `AUTDB  <Xd>, <Xn|SP>`
- **Fixed bits**: `Z`=`0`
- **Bit Pattern**: `?????????????0??????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  13 12   9   4  |
|--------------------------------|
| 1   1   0   11010110 00001 00  Z   111 Rn  Rd  |
```

#### Decode (A64.dpreg.dp_1src.AUTDB_64P_dp_1src)

```
if !IsFeatureImplemented(FEAT_PAuth) then EndOfDecode(Decode_UNDEF);
if Z == '1' && Rn != '11111' then EndOfDecode(Decode_UNDEF);
constant boolean auth_combined = FALSE;

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);

constant boolean source_is_sp = Z == '0' && n == 31;
```

#### Execute (A64.dpreg.dp_1src.AUTDB_64P_dp_1src)

```
if source_is_sp then
    X[d, 64] = AuthDB(X[d, 64], SP[64], auth_combined);
else
    X[d, 64] = AuthDB(X[d, 64], X[n, 64], auth_combined);
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_PAuth)` |
| 🚫 ENCODING_UNDEF | `Z != '1' \|\| Rn == '11111'` |

### Variant: `Integer (AUTDZB_64Z_dp_1src)` (AUTDZB)
- **Condition**: `Z == 1 && Rn == 11111`
- **Assembly**: `AUTDZB  <Xd>`
- **Fixed bits**: `Z`=`1`, `Rn`=`11111`
- **Bit Pattern**: `?????11111???1??????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15  13 12   9   4  |
|--------------------------------|
| 1   1   0   11010110 00001 00  Z   111 Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose source register or stack pointer, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `autdb.xml`
</details>